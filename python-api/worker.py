"""Cloudflare Workers entry point — Durable Object (SQLite) edition.

Drop-in replacement for ``worker.py``: rename over it when applying.

The FastAPI app runs *inside* the ``PreviewBackend`` Durable Object so that
SQL executes synchronously against the object's private SQLite storage: no
database to provision, no per-query network hop, and the data lives exactly
as long as the preview script does. The stateless ``Default`` entrypoint only
forwards requests to this deployment's single object instance.

``workers`` and ``asgi`` are provided by the Workers Python runtime; this
module is only imported there, never by the test suite.
"""

from workers import DurableObject, WorkerEntrypoint  # type: ignore[import-not-found]

# One object per preview deployment. The name is constant because every
# deployment gets its own Durable Object namespace (the class is exported by
# this script), so there is nothing to disambiguate.
DB_OBJECT_NAME = "main"

_app = None


def _get_app():
    global _app
    if _app is None:
        from main import app

        _app = app
    return _app


class PreviewBackend(DurableObject):
    """Owns this deployment's SQLite database and serves the API on top of it."""

    def __init__(self, ctx, env):
        super().__init__(ctx, env)
        self._ensure_schema()

    def _ensure_schema(self) -> None:
        """Create any missing tables and indexes from the SQLAlchemy metadata.

        Runs synchronously in the constructor, so it completes before the
        object serves its first request. Idempotent: existing tables and their
        rows are left untouched, which is what preserves data across redeploys
        of the same deployment.
        """
        from sqlalchemy.schema import CreateIndex, CreateTable

        from core.d1 import DIALECT
        from core.database import Base

        _get_app()  # importing the app registers every feature model on Base.metadata
        sql = self.ctx.storage.sql
        for table in Base.metadata.sorted_tables:
            sql.exec(str(CreateTable(table, if_not_exists=True).compile(dialect=DIALECT)))
            for index in table.indexes:
                sql.exec(str(CreateIndex(index, if_not_exists=True).compile(dialect=DIALECT)))

    async def fetch(self, request):
        import asgi  # type: ignore[import-not-found]

        from core.database import bind_sql_storage, unbind_sql_storage

        token = bind_sql_storage(self.ctx.storage.sql)
        try:
            return await asgi.fetch(_get_app(), request, self.env)
        finally:
            unbind_sql_storage(token)


class Default(WorkerEntrypoint):
    async def fetch(self, request):
        return await self.env.BACKEND.getByName(DB_OBJECT_NAME).fetch(request)
