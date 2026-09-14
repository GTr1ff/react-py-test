# ROSETIC:crud-guid

"""
Shared test fixtures and configuration for the test suite.
"""


import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock
from polyfactory.factories.pydantic_factory import ModelFactory
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory

import base64
import datetime

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from tests.conftest import get_test_time, get_test_date

from core.pagination import PaginationRequest
from features.tables.tasks.models import TaskModel
from features.tables.tasks.schemas import TaskCreate, TaskUpdate, TaskFilter
from features.tables.tasks.repository import TaskRepository
from features.tables.tasks.service import TaskService

class TaskModelFactory(SQLAlchemyFactory[TaskModel]):
    __model__ = TaskModel
    __set_relationships__ = False
    __random_seed__ = 0



class TaskCreateFactory(ModelFactory[TaskCreate]):
    __model__ = TaskCreate
    __random_seed__ = 0


class TaskUpdateFactory(ModelFactory[TaskUpdate]):
    __model__ = TaskUpdate
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
    """Sample task data for testing."""
    return TaskCreateFactory.build().model_dump()

@pytest.fixture
def existing_task(sample_data):
    """Sample Task model instance for testing."""
    return TaskModelFactory.build(task_id=1)

@pytest.fixture
def updated_task_model():
    """Sample Task model instance with changes for testing."""
    return TaskModelFactory.build(task_id=7)

@pytest.fixture
def updated_task():
    """Sample Task model instance with changes for testing."""
    return TaskUpdateFactory.build()
    


@pytest.fixture
def pagination_request():
    """Default pagination request for testing."""
    return PaginationRequest()


@pytest_asyncio.fixture
async def task_repository(mock_session_async):
    """Create TaskRepository instance with test session."""
    return TaskRepository(mock_session_async)


@pytest.fixture
def multiple_tasks():
    """Create multiple Task instances for testing."""
    return [TaskModelFactory.build(task_id=i + 1) for i in range(5)]
