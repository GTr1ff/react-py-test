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
from features.tables.job_history.models import JobHistoryModel
from features.tables.job_history.schemas import JobHistoryCreate, JobHistoryUpdate, JobHistoryFilter
from features.tables.job_history.repository import JobHistoryRepository
from features.tables.job_history.service import JobHistoryService

class JobHistoryModelFactory(SQLAlchemyFactory[JobHistoryModel]):
    __model__ = JobHistoryModel
    __set_relationships__ = False
    __random_seed__ = 0



class JobHistoryCreateFactory(ModelFactory[JobHistoryCreate]):
    __model__ = JobHistoryCreate
    __random_seed__ = 0


class JobHistoryUpdateFactory(ModelFactory[JobHistoryUpdate]):
    __model__ = JobHistoryUpdate
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
    """Sample job_history data for testing."""
    return JobHistoryCreateFactory.build().model_dump()

@pytest.fixture
def existing_job_history(sample_data):
    """Sample JobHistory model instance for testing."""
    return JobHistoryModelFactory.build(job_history_id=1)

@pytest.fixture
def updated_job_history_model():
    """Sample JobHistory model instance with changes for testing."""
    return JobHistoryModelFactory.build(job_history_id=7)

@pytest.fixture
def updated_job_history():
    """Sample JobHistory model instance with changes for testing."""
    return JobHistoryUpdateFactory.build()
    


@pytest.fixture
def pagination_request():
    """Default pagination request for testing."""
    return PaginationRequest()


@pytest_asyncio.fixture
async def job_history_repository(mock_session_async):
    """Create JobHistoryRepository instance with test session."""
    return JobHistoryRepository(mock_session_async)


@pytest.fixture
def multiple_job_history():
    """Create multiple JobHistory instances for testing."""
    return [JobHistoryModelFactory.build(job_history_id=i + 1) for i in range(5)]
