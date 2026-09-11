"""Worker-mode database plumbing: declarative base + Durable Object session dependency.

Drop-in replacement for ``core/database.py``: rename over it when applying.

On Cloudflare Workers there is no engine: the schema lives in the SQLite
storage of the ``PreviewDatabase`` Durable Object (see ``worker.py``), which
also runs the FastAPI app. Before handling each request the object publishes
its ``ctx.storage.sql`` handle through a context variable, and ``get_db``
wraps that handle in a :class:`core.d1.D1Session` for the request.
"""

from contextvars import ContextVar, Token
from typing import Any, AsyncGenerator

from fastapi import Request
from sqlalchemy.orm import DeclarativeBase

from core.d1 import D1Session


class Base(DeclarativeBase):
    pass


_sql_storage: ContextVar[Any] = ContextVar("sql_storage")


def bind_sql_storage(sql_storage: Any) -> Token:
    """Publish the Durable Object's ``ctx.storage.sql`` handle for the current request context."""
    return _sql_storage.set(sql_storage)


def unbind_sql_storage(token: Token) -> None:
    """Undo :func:`bind_sql_storage` once the request has been handled."""
    _sql_storage.reset(token)


async def get_db(request: Request) -> AsyncGenerator[D1Session, None]:
    """FastAPI dependency yielding a Durable Object SQLite-backed session for this request."""
    session = D1Session(_sql_storage.get())
    try:
        yield session
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()
