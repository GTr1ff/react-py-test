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
from features.tables.category.models import CategoryModel
from features.tables.category.schemas import CategoryCreate, CategoryUpdate, CategoryFilter
from features.tables.category.repository import CategoryRepository
from features.tables.category.service import CategoryService

class CategoryModelFactory(SQLAlchemyFactory[CategoryModel]):
    __model__ = CategoryModel
    __set_relationships__ = False
    __random_seed__ = 0



class CategoryCreateFactory(ModelFactory[CategoryCreate]):
    __model__ = CategoryCreate
    __random_seed__ = 0


class CategoryUpdateFactory(ModelFactory[CategoryUpdate]):
    __model__ = CategoryUpdate
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
    """Sample category data for testing."""
    return CategoryCreateFactory.build().model_dump()

@pytest.fixture
def existing_category(sample_data):
    """Sample Category model instance for testing."""
    return CategoryModelFactory.build(id=1)

@pytest.fixture
def updated_category_model():
    """Sample Category model instance with changes for testing."""
    return CategoryModelFactory.build(id=7)

@pytest.fixture
def updated_category():
    """Sample Category model instance with changes for testing."""
    return CategoryUpdateFactory.build()
    


@pytest.fixture
def pagination_request():
    """Default pagination request for testing."""
    return PaginationRequest()


@pytest_asyncio.fixture
async def category_repository(mock_session_async):
    """Create CategoryRepository instance with test session."""
    return CategoryRepository(mock_session_async)


@pytest.fixture
def multiple_category():
    """Create multiple Category instances for testing."""
    return [CategoryModelFactory.build(id=i + 1) for i in range(5)]
