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
from features.tables.ingredient.models import IngredientModel
from features.tables.ingredient.schemas import IngredientCreate, IngredientUpdate, IngredientFilter
from features.tables.ingredient.repository import IngredientRepository
from features.tables.ingredient.service import IngredientService

class IngredientModelFactory(SQLAlchemyFactory[IngredientModel]):
    __model__ = IngredientModel
    __set_relationships__ = False
    __random_seed__ = 0



class IngredientCreateFactory(ModelFactory[IngredientCreate]):
    __model__ = IngredientCreate
    __random_seed__ = 0


class IngredientUpdateFactory(ModelFactory[IngredientUpdate]):
    __model__ = IngredientUpdate
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
    """Sample ingredient data for testing."""
    return IngredientCreateFactory.build().model_dump()

@pytest.fixture
def existing_ingredient(sample_data):
    """Sample Ingredient model instance for testing."""
    return IngredientModelFactory.build(id=1)

@pytest.fixture
def updated_ingredient_model():
    """Sample Ingredient model instance with changes for testing."""
    return IngredientModelFactory.build(id=7)

@pytest.fixture
def updated_ingredient():
    """Sample Ingredient model instance with changes for testing."""
    return IngredientUpdateFactory.build()
    


@pytest.fixture
def pagination_request():
    """Default pagination request for testing."""
    return PaginationRequest()


@pytest_asyncio.fixture
async def ingredient_repository(mock_session_async):
    """Create IngredientRepository instance with test session."""
    return IngredientRepository(mock_session_async)


@pytest.fixture
def multiple_ingredient():
    """Create multiple Ingredient instances for testing."""
    return [IngredientModelFactory.build(id=i + 1) for i in range(5)]
