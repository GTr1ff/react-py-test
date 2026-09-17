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
from features.tables.event_log.models import EventLogModel
from features.tables.event_log.schemas import EventLogCreate, EventLogUpdate, EventLogFilter
from features.tables.event_log.repository import EventLogRepository
from features.tables.event_log.service import EventLogService

class EventLogModelFactory(SQLAlchemyFactory[EventLogModel]):
    __model__ = EventLogModel
    __set_relationships__ = False
    __random_seed__ = 0



class EventLogCreateFactory(ModelFactory[EventLogCreate]):
    __model__ = EventLogCreate
    __random_seed__ = 0


class EventLogUpdateFactory(ModelFactory[EventLogUpdate]):
    __model__ = EventLogUpdate
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
    """Sample event_log data for testing."""
    return EventLogCreateFactory.build().model_dump()

@pytest.fixture
def existing_event_log(sample_data):
    """Sample EventLog model instance for testing."""
    return EventLogModelFactory.build(id=1)

@pytest.fixture
def updated_event_log_model():
    """Sample EventLog model instance with changes for testing."""
    return EventLogModelFactory.build(id=7)

@pytest.fixture
def updated_event_log():
    """Sample EventLog model instance with changes for testing."""
    return EventLogUpdateFactory.build()
    


@pytest.fixture
def pagination_request():
    """Default pagination request for testing."""
    return PaginationRequest()


@pytest_asyncio.fixture
async def event_log_repository(mock_session_async):
    """Create EventLogRepository instance with test session."""
    return EventLogRepository(mock_session_async)


@pytest.fixture
def multiple_event_log():
    """Create multiple EventLog instances for testing."""
    return [EventLogModelFactory.build(id=i + 1) for i in range(5)]
