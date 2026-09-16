"""Worker-mode database plumbing: declarative base + Durable Object session dependency.

On Cloudflare Workers there is no engine: the schema lives in the SQLite
storage of the ``PreviewDatabase`` Durable Object
"""

from contextvars import ContextVar, Token
from typing import Any
from collections.abc import AsyncGenerator
from sqlalchemy.orm import DeclarativeBase

from core.do_sqlite import DOSession


class Base(DeclarativeBase):
    pass


_sql_storage: ContextVar[Any] = ContextVar("sql_storage")


def bind_sql_storage(sql_storage: Any) -> Token:
    """Publish the Durable Object's ``ctx.storage.sql`` handle for the current request context."""
    return _sql_storage.set(sql_storage)


def unbind_sql_storage(token: Token) -> None:
    """Undo :func:`bind_sql_storage` once the request has been handled."""
    _sql_storage.reset(token)


async def get_db() -> AsyncGenerator[DOSession, None]:
    """FastAPI dependency yielding a Durable Object SQLite-backed session for this request."""
    session = DOSession(_sql_storage.get())
    try:
        yield session
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()
