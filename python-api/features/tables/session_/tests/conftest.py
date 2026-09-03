# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c

"""
Shared test fixtures and configuration for the test suite.
"""


import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock
from polyfactory.factories.pydantic_factory import ModelFactory
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory


import datetime

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from tests.conftest import get_test_time, get_test_date

from core.pagination import PaginationRequest
from features.tables.session_.models import SessionModel
from features.tables.session_.schemas import SessionCreate, SessionUpdate, SessionFilter
from features.tables.session_.repository import SessionRepository
from features.tables.session_.service import SessionService

class SessionModelFactory(SQLAlchemyFactory[SessionModel]):
    __model__ = SessionModel
    __set_relationships__ = False
    __random_seed__ = 0



class SessionCreateFactory(ModelFactory[SessionCreate]):
    __model__ = SessionCreate
    __random_seed__ = 0


class SessionUpdateFactory(ModelFactory[SessionUpdate]):
    __model__ = SessionUpdate
    __random_seed__ = 0

@pytest.fixture
def mock_session_async():
    """Create a mock AsyncSession for unit testing."""
    session = AsyncMock(spec=AsyncSession)
    session.add = MagicMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.execute = AsyncMock()
    session.scalar = AsyncMock()
    session.delete = AsyncMock()
    return session

@pytest.fixture
def sample_data():
    """Sample session data for testing."""
    return SessionCreateFactory.build().model_dump()

@pytest.fixture
def existing_session(sample_data):
    """Sample Session model instance for testing."""
    return SessionModelFactory.build(id=1)

@pytest.fixture
def updated_session_model():
    """Sample Session model instance with changes for testing."""
    return SessionModelFactory.build(id=7)

@pytest.fixture
def updated_session():
    """Sample Session model instance with changes for testing."""
    return SessionUpdateFactory.build()
    


@pytest.fixture
def pagination_request():
    """Default pagination request for testing."""
    return PaginationRequest()


@pytest_asyncio.fixture
async def session_repository(mock_session_async):
    """Create SessionRepository instance with test session."""
    return SessionRepository(mock_session_async)


@pytest.fixture
def multiple_session():
    """Create multiple Session instances for testing."""
    return [SessionModelFactory.build(id=i + 1) for i in range(5)]
