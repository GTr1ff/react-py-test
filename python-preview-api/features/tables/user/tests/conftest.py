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
from features.tables.user.models import UserModel
from features.tables.user.schemas import UserCreate, UserUpdate, UserFilter
from features.tables.user.repository import UserRepository
from features.tables.user.service import UserService

class UserModelFactory(SQLAlchemyFactory[UserModel]):
    __model__ = UserModel
    __set_relationships__ = False
    __random_seed__ = 0



class UserCreateFactory(ModelFactory[UserCreate]):
    __model__ = UserCreate
    __random_seed__ = 0


class UserUpdateFactory(ModelFactory[UserUpdate]):
    __model__ = UserUpdate
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
    """Sample user data for testing."""
    return UserCreateFactory.build().model_dump()

@pytest.fixture
def existing_user(sample_data):
    """Sample User model instance for testing."""
    return UserModelFactory.build(id=1)

@pytest.fixture
def updated_user_model():
    """Sample User model instance with changes for testing."""
    return UserModelFactory.build(id=7)

@pytest.fixture
def updated_user():
    """Sample User model instance with changes for testing."""
    return UserUpdateFactory.build()
    


@pytest.fixture
def pagination_request():
    """Default pagination request for testing."""
    return PaginationRequest()


@pytest_asyncio.fixture
async def user_repository(mock_session_async):
    """Create UserRepository instance with test session."""
    return UserRepository(mock_session_async)


@pytest.fixture
def multiple_user():
    """Create multiple User instances for testing."""
    return [UserModelFactory.build(id=i + 1) for i in range(5)]
