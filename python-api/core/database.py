"""Worker-mode database plumbing: declarative base + D1 session dependency.

In the original service this module owned the SQLAlchemy async engine. On
Cloudflare Workers there is no engine: the schema is managed by D1
migrations and every request gets a :class:`core.d1.D1Session` bound to the
``DB`` binding that the Workers ASGI bridge exposes on the request scope.
"""

from typing import AsyncGenerator

from fastapi import Request
from sqlalchemy.orm import DeclarativeBase

from core.d1 import D1Session


class Base(DeclarativeBase):
    pass


async def get_db(request: Request) -> AsyncGenerator[D1Session, None]:
    """FastAPI dependency yielding a D1-backed session for this request."""
    session = D1Session(request.scope["env"].DB)
    try:
        yield session
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()
