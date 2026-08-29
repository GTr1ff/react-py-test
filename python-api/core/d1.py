"""D1-backed data access for Cloudflare Python Workers.

The Workers Python runtime (Pyodide) does not ship ``greenlet``, so
SQLAlchemy's async engine cannot run there. Instead, SQLAlchemy is kept as
the SQL *compiler* (D1 is SQLite, so the SQLite dialect produces compatible
SQL) and execution happens through the D1 binding's FFI API
(``prepare(...).bind(...).run()``).

``D1Session`` implements the exact subset of the ``AsyncSession`` API used
by the feature repositories — ``execute``, ``scalar``, ``add``, ``commit``,
``refresh``, ``delete``, ``rollback``, ``close`` — so the repository,
service, router and schema layers stay unchanged.
"""

import json
import sys
from typing import Any, cast

from sqlalchemy import LargeBinary, delete, insert, inspect, select, update
from sqlalchemy.dialects import sqlite
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm import Mapper
from sqlalchemy.sql import ClauseElement
from sqlalchemy.sql.compiler import SQLCompiler

_IS_WORKERS_RUNTIME = sys.platform == "emscripten"


def _json_default(value: Any) -> Any:
    """Serialize container types the stdlib JSON encoder rejects (e.g. ``set``)."""
    if isinstance(value, (set, frozenset)):
        return list(value)
    raise TypeError(f"Object of type {type(value).__name__} is not JSON serializable")


# D1 is SQLite, so the SQLite dialect compiles compatible SQL and provides
# the bind/result processors (date/time <-> ISO strings, Decimal <-> float,
# bool <-> int, UUID <-> hex, JSON <-> text) that keep model types faithful.
DIALECT = sqlite.dialect(
    json_serializer=lambda value: json.dumps(value, default=_json_default),
)


def compile_statement(statement: ClauseElement) -> tuple[str, list[Any]]:
    """Compile a SQLAlchemy statement into SQLite SQL and positional parameters.

    Args:
        statement: Any SQLAlchemy Core / ORM statement (select, insert, ...).

    Returns:
        tuple[str, list[Any]]: The SQL string using ``?`` placeholders and the
        parameter values in positional order, with type bind processors
        (dates, Decimal, JSON, ...) already applied.
    """
    # compile() is typed as returning the abstract Compiled; for SQL
    # statements it is always an SQLCompiler, which carries the attributes
    # used below.
    compiled = cast(SQLCompiler, statement.compile(dialect=DIALECT))
    params = compiled.construct_params()
    # _bind_processors is the compiler's per-parameter type conversion map;
    # SQLAlchemy offers no public equivalent outside engine execution.
    processors = compiled._bind_processors
    values: list[Any] = []
    # positiontup is None only for non-positional paramstyles; the SQLite
    # dialect uses qmark, which is positional.
    for name in compiled.positiontup or ():
        value = params[name]
        processor = processors.get(name)
        values.append(processor(value) if processor is not None else value)
    return str(compiled), values


def _bind_value(value: Any) -> Any:
    """Convert one bound parameter into a value the D1 FFI accepts."""
    if _IS_WORKERS_RUNTIME:
        if value is None:
            from pyodide.ffi import jsnull

            # Python None crosses the FFI as JS `undefined`, which D1 rejects
            # (D1_TYPE_ERROR); jsnull crosses as the JS `null` D1 expects.
            return jsnull
        if isinstance(value, (bytes, bytearray)):
            from pyodide.ffi import to_js

            # D1 expects BLOB parameters as a JavaScript ArrayBuffer.
            return to_js(value).buffer
    return value


def _unwrap_null(value: Any) -> Any:
    """Map the FFI's JS-null singleton back to Python None."""
    if _IS_WORKERS_RUNTIME:
        from pyodide.ffi import jsnull

        if value is jsnull:
            return None
    return value


def _result_value(column: Any, value: Any) -> Any:
    """Convert one raw D1 column value back into the model's Python type."""
    value = _unwrap_null(value)
    # D1 returns BLOB columns as a JS array of byte values (a list after
    # to_py()); buffers can also surface as memoryview/bytearray.
    if isinstance(value, (memoryview, bytearray)) or (
        isinstance(value, list) and isinstance(column.type, LargeBinary)
    ):
        value = bytes(value)
    processor = column.type.result_processor(DIALECT, None)
    return processor(value) if processor is not None else value


def _rows(d1_result: Any) -> list[dict[str, Any]]:
    """Extract result rows from a D1 result as plain Python dicts."""
    results = d1_result.results
    if hasattr(results, "to_py"):  # JsProxy in the Workers runtime
        results = results.to_py()
    return list(results)


def _translate_db_error(error: Exception, sql: str, params: list[Any]) -> Exception:
    """Map a D1/SQLite error onto the SQLAlchemy exception hierarchy.

    Keeps ``core.db_exception_handler.handle_db_exceptions_async`` (and its
    HTTP status mapping) working unchanged in the Worker.
    """
    if "constraint" in str(error).lower():
        return IntegrityError(sql, params, error)
    return OperationalError(sql, params, error)


def _select_entity(statement: ClauseElement) -> type | None:
    """Return the single mapped class a select() targets, if any."""
    descriptions = getattr(statement, "column_descriptions", None)
    if descriptions and len(descriptions) == 1:
        entity = descriptions[0].get("entity")
        if entity is not None and inspect(entity, raiseerr=False) is not None:
            return entity
    return None


def _primary_key(mapper: Mapper) -> tuple[str, Any]:
    """Return the (attribute key, Column) of the mapper's primary key."""
    column = mapper.primary_key[0]
    return mapper.get_property_by_column(column).key, column


class _ScalarResult:
    """Mimics ``ScalarResult`` for the calls repositories make on it."""

    def __init__(self, records: list[Any]):
        self._records = records

    def first(self) -> Any | None:
        return self._records[0] if self._records else None

    def all(self) -> list[Any]:
        return list(self._records)


class _Result:
    """Mimics ``Result`` for the ``.unique().scalars()`` chain repositories use."""

    def __init__(self, records: list[Any]):
        self._records = records

    def unique(self) -> "_Result":
        return self

    def scalars(self) -> _ScalarResult:
        return _ScalarResult(self._records)


class D1Session:
    """AsyncSession-compatible unit of work executing against a D1 binding.

    D1 has no interactive transactions: every statement auto-commits. The
    repositories already follow a commit-per-operation pattern, so ``add``/
    ``delete`` queue work that ``commit`` flushes, and attribute changes on
    loaded instances are detected by diffing against a snapshot taken at
    load time (mirroring the ORM's flush-on-commit behavior).
    """

    def __init__(self, d1_binding: Any):
        self._db = d1_binding
        self._pending_new: list[Any] = []
        self._pending_deleted: list[Any] = []
        self._tracked: dict[int, Any] = {}
        self._snapshots: dict[int, dict[str, Any]] = {}

    # ─── Query execution ──────────────────────────────────
    async def execute(self, statement: ClauseElement) -> _Result:
        """Execute a select() and return a Result-like object."""
        entity = _select_entity(statement)
        rows = await self._run(*compile_statement(statement))
        if entity is None:
            records: list[Any] = [_unwrap_null(next(iter(row.values()), None)) for row in rows]
        else:
            records = [self._hydrate(entity, row) for row in rows]
        return _Result(records)

    async def scalar(self, statement: ClauseElement) -> Any | None:
        """Execute a select() and return the first column of the first row."""
        rows = await self._run(*compile_statement(statement))
        if not rows:
            return None
        return _unwrap_null(next(iter(rows[0].values()), None))

    # ─── Unit-of-work operations ──────────────────────────────────
    def add(self, instance: Any) -> None:
        """Queue a model instance for INSERT on the next commit."""
        self._pending_new.append(instance)

    async def delete(self, instance: Any) -> None:
        """Queue a model instance for DELETE on the next commit."""
        self._pending_deleted.append(instance)

    async def commit(self) -> None:
        """Flush queued inserts/deletes and any tracked attribute changes."""
        for instance in self._pending_new:
            await self._insert(instance)
        self._pending_new = []

        for instance in list(self._tracked.values()):
            changes = self._pending_changes(instance)
            if changes:
                await self._update(instance, changes)
                self._track(instance)

        for instance in self._pending_deleted:
            await self._delete_row(instance)
            self._untrack(instance)
        self._pending_deleted = []

    async def refresh(self, instance: Any) -> None:
        """Reload the instance's attributes from the database by primary key."""
        cls = type(instance)
        mapper = inspect(cls)
        pk_attr, pk_column = _primary_key(mapper)
        statement = select(cls).where(pk_column == getattr(instance, pk_attr))
        rows = await self._run(*compile_statement(statement))
        if rows:
            self._apply_row(instance, rows[0])
        self._track(instance)

    async def rollback(self) -> None:
        """Discard queued (not yet committed) work."""
        self._pending_new.clear()
        self._pending_deleted.clear()

    async def close(self) -> None:
        """Release all tracked state."""
        self._pending_new.clear()
        self._pending_deleted.clear()
        self._tracked.clear()
        self._snapshots.clear()

    # ─── Internals ──────────────────────────────────
    async def _run(self, sql: str, params: list[Any]) -> list[dict[str, Any]]:
        statement = self._db.prepare(sql)
        if params:
            statement = statement.bind(*[_bind_value(value) for value in params])
        try:
            result = await statement.run()
        except Exception as error:
            raise _translate_db_error(error, sql, params) from error
        return _rows(result)

    async def _insert(self, instance: Any) -> None:
        cls = type(instance)
        mapper = inspect(cls)
        pk_attr, _ = _primary_key(mapper)
        values = {
            attr.key: instance.__dict__[attr.key]
            for attr in mapper.column_attrs
            if attr.key in instance.__dict__
        }
        if values.get(pk_attr) is None:
            values.pop(pk_attr, None)  # let SQLite assign the autoincrement key
        statement = insert(cls).values(**values).returning(*mapper.local_table.columns)
        rows = await self._run(*compile_statement(statement))
        if rows:
            self._apply_row(instance, rows[0])
        self._track(instance)

    async def _update(self, instance: Any, changes: dict[str, Any]) -> None:
        cls = type(instance)
        mapper = inspect(cls)
        pk_attr, pk_column = _primary_key(mapper)
        pk_value = self._snapshots[id(instance)][pk_attr]
        statement = update(cls).where(pk_column == pk_value).values(**changes)
        await self._run(*compile_statement(statement))

    async def _delete_row(self, instance: Any) -> None:
        cls = type(instance)
        mapper = inspect(cls)
        pk_attr, pk_column = _primary_key(mapper)
        statement = delete(cls).where(pk_column == getattr(instance, pk_attr))
        await self._run(*compile_statement(statement))

    def _hydrate(self, entity: type, row: dict[str, Any]) -> Any:
        mapper = inspect(entity)
        kwargs = {
            attr.key: _result_value(attr.columns[0], row[attr.columns[0].name])
            for attr in mapper.column_attrs
            if attr.columns[0].name in row
        }
        instance = entity(**kwargs)
        self._track(instance)
        return instance

    def _apply_row(self, instance: Any, row: dict[str, Any]) -> None:
        mapper = inspect(type(instance))
        for attr in mapper.column_attrs:
            column = attr.columns[0]
            if column.name in row:
                setattr(instance, attr.key, _result_value(column, row[column.name]))

    def _pending_changes(self, instance: Any) -> dict[str, Any]:
        snapshot = self._snapshots.get(id(instance), {})
        return {
            key: value
            for key, value in self._column_state(instance).items()
            if key not in snapshot or snapshot[key] != value
        }

    def _track(self, instance: Any) -> None:
        self._tracked[id(instance)] = instance
        self._snapshots[id(instance)] = self._column_state(instance)

    def _untrack(self, instance: Any) -> None:
        self._tracked.pop(id(instance), None)
        self._snapshots.pop(id(instance), None)

    @staticmethod
    def _column_state(instance: Any) -> dict[str, Any]:
        mapper = inspect(type(instance))
        return {attr.key: getattr(instance, attr.key) for attr in mapper.column_attrs}
