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
from features.tables.notification.models import NotificationModel
from features.tables.notification.schemas import NotificationCreate, NotificationUpdate, NotificationFilter
from features.tables.notification.repository import NotificationRepository
from features.tables.notification.service import NotificationService

class NotificationModelFactory(SQLAlchemyFactory[NotificationModel]):
    __model__ = NotificationModel
    __set_relationships__ = False
    __random_seed__ = 0



class NotificationCreateFactory(ModelFactory[NotificationCreate]):
    __model__ = NotificationCreate
    __random_seed__ = 0


class NotificationUpdateFactory(ModelFactory[NotificationUpdate]):
    __model__ = NotificationUpdate
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
    """Sample notification data for testing."""
    return NotificationCreateFactory.build().model_dump()

@pytest.fixture
def existing_notification(sample_data):
    """Sample Notification model instance for testing."""
    return NotificationModelFactory.build(id=1)

@pytest.fixture
def updated_notification_model():
    """Sample Notification model instance with changes for testing."""
    return NotificationModelFactory.build(id=7)

@pytest.fixture
def updated_notification():
    """Sample Notification model instance with changes for testing."""
    return NotificationUpdateFactory.build()
    


@pytest.fixture
def pagination_request():
    """Default pagination request for testing."""
    return PaginationRequest()


@pytest_asyncio.fixture
async def notification_repository(mock_session_async):
    """Create NotificationRepository instance with test session."""
    return NotificationRepository(mock_session_async)


@pytest.fixture
def multiple_notification():
    """Create multiple Notification instances for testing."""
    return [NotificationModelFactory.build(id=i + 1) for i in range(5)]
