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
from features.tables.settings.models import SettingModel
from features.tables.settings.schemas import SettingCreate, SettingUpdate, SettingFilter
from features.tables.settings.repository import SettingRepository
from features.tables.settings.service import SettingService

class SettingModelFactory(SQLAlchemyFactory[SettingModel]):
    __model__ = SettingModel
    __set_relationships__ = False
    __random_seed__ = 0



class SettingCreateFactory(ModelFactory[SettingCreate]):
    __model__ = SettingCreate
    __random_seed__ = 0


class SettingUpdateFactory(ModelFactory[SettingUpdate]):
    __model__ = SettingUpdate
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
    """Sample setting data for testing."""
    return SettingCreateFactory.build().model_dump()

@pytest.fixture
def existing_setting(sample_data):
    """Sample Setting model instance for testing."""
    return SettingModelFactory.build(setting_id=1)

@pytest.fixture
def updated_setting_model():
    """Sample Setting model instance with changes for testing."""
    return SettingModelFactory.build(setting_id=7)

@pytest.fixture
def updated_setting():
    """Sample Setting model instance with changes for testing."""
    return SettingUpdateFactory.build()
    


@pytest.fixture
def pagination_request():
    """Default pagination request for testing."""
    return PaginationRequest()


@pytest_asyncio.fixture
async def setting_repository(mock_session_async):
    """Create SettingRepository instance with test session."""
    return SettingRepository(mock_session_async)


@pytest.fixture
def multiple_settings():
    """Create multiple Setting instances for testing."""
    return [SettingModelFactory.build(setting_id=i + 1) for i in range(5)]
