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
from features.tables.user_preference.models import UserPreferenceModel
from features.tables.user_preference.schemas import UserPreferenceCreate, UserPreferenceUpdate, UserPreferenceFilter
from features.tables.user_preference.repository import UserPreferenceRepository
from features.tables.user_preference.service import UserPreferenceService

class UserPreferenceModelFactory(SQLAlchemyFactory[UserPreferenceModel]):
    __model__ = UserPreferenceModel
    __set_relationships__ = False
    __random_seed__ = 0



class UserPreferenceCreateFactory(ModelFactory[UserPreferenceCreate]):
    __model__ = UserPreferenceCreate
    __random_seed__ = 0


class UserPreferenceUpdateFactory(ModelFactory[UserPreferenceUpdate]):
    __model__ = UserPreferenceUpdate
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
    """Sample user_preference data for testing."""
    return UserPreferenceCreateFactory.build().model_dump()

@pytest.fixture
def existing_user_preference(sample_data):
    """Sample UserPreference model instance for testing."""
    return UserPreferenceModelFactory.build(id=1)

@pytest.fixture
def updated_user_preference_model():
    """Sample UserPreference model instance with changes for testing."""
    return UserPreferenceModelFactory.build(id=7)

@pytest.fixture
def updated_user_preference():
    """Sample UserPreference model instance with changes for testing."""
    return UserPreferenceUpdateFactory.build()
    


@pytest.fixture
def pagination_request():
    """Default pagination request for testing."""
    return PaginationRequest()


@pytest_asyncio.fixture
async def user_preference_repository(mock_session_async):
    """Create UserPreferenceRepository instance with test session."""
    return UserPreferenceRepository(mock_session_async)


@pytest.fixture
def multiple_user_preference():
    """Create multiple UserPreference instances for testing."""
    return [UserPreferenceModelFactory.build(id=i + 1) for i in range(5)]
