# ROSETIC:crud-guid

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
from features.tables.time_logs.models import TimeLogModel
from features.tables.time_logs.schemas import TimeLogCreate, TimeLogUpdate, TimeLogFilter
from features.tables.time_logs.repository import TimeLogRepository
from features.tables.time_logs.service import TimeLogService

class TimeLogModelFactory(SQLAlchemyFactory[TimeLogModel]):
    __model__ = TimeLogModel
    __set_relationships__ = False
    __random_seed__ = 0



class TimeLogCreateFactory(ModelFactory[TimeLogCreate]):
    __model__ = TimeLogCreate
    __random_seed__ = 0


class TimeLogUpdateFactory(ModelFactory[TimeLogUpdate]):
    __model__ = TimeLogUpdate
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
    """Sample time_log data for testing."""
    return TimeLogCreateFactory.build().model_dump()

@pytest.fixture
def existing_time_log(sample_data):
    """Sample TimeLog model instance for testing."""
    return TimeLogModelFactory.build(time_log_id=1)

@pytest.fixture
def updated_time_log_model():
    """Sample TimeLog model instance with changes for testing."""
    return TimeLogModelFactory.build(time_log_id=7)

@pytest.fixture
def updated_time_log():
    """Sample TimeLog model instance with changes for testing."""
    return TimeLogUpdateFactory.build()
    


@pytest.fixture
def pagination_request():
    """Default pagination request for testing."""
    return PaginationRequest()


@pytest_asyncio.fixture
async def time_log_repository(mock_session_async):
    """Create TimeLogRepository instance with test session."""
    return TimeLogRepository(mock_session_async)


@pytest.fixture
def multiple_time_logs():
    """Create multiple TimeLog instances for testing."""
    return [TimeLogModelFactory.build(time_log_id=i + 1) for i in range(5)]
