"""Cloudflare Workers entry point.

The FastAPI app runs *inside* the ``PreviewBackend`` Durable Object so that
SQL executes synchronously against the object's private SQLite storage
"""

from workers import DurableObject, WorkerEntrypoint # type: ignore[import-not-found]

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
        """Create any missing tables and indexes from the SQLAlchemy metadata."""
        from sqlalchemy.schema import CreateIndex, CreateTable

        from core.do_sqlite import DIALECT
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
