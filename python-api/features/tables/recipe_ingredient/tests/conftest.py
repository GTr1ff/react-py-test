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
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from tests.conftest import get_test_time, get_test_date

from core.pagination import PaginationRequest
from features.tables.recipe_ingredient.models import RecipeIngredientModel
from features.tables.recipe_ingredient.schemas import RecipeIngredientCreate, RecipeIngredientUpdate, RecipeIngredientFilter
from features.tables.recipe_ingredient.repository import RecipeIngredientRepository
from features.tables.recipe_ingredient.service import RecipeIngredientService

class RecipeIngredientModelFactory(SQLAlchemyFactory[RecipeIngredientModel]):
    __model__ = RecipeIngredientModel
    __set_relationships__ = False
    __random_seed__ = 0



class RecipeIngredientCreateFactory(ModelFactory[RecipeIngredientCreate]):
    __model__ = RecipeIngredientCreate
    __random_seed__ = 0


class RecipeIngredientUpdateFactory(ModelFactory[RecipeIngredientUpdate]):
    __model__ = RecipeIngredientUpdate
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
    """Sample recipe_ingredient data for testing."""
    return RecipeIngredientCreateFactory.build().model_dump()

@pytest.fixture
def existing_recipe_ingredient(sample_data):
    """Sample RecipeIngredient model instance for testing."""
    return RecipeIngredientModelFactory.build(recipe_id=1)

@pytest.fixture
def updated_recipe_ingredient_model():
    """Sample RecipeIngredient model instance with changes for testing."""
    return RecipeIngredientModelFactory.build(recipe_id=7)

@pytest.fixture
def updated_recipe_ingredient():
    """Sample RecipeIngredient model instance with changes for testing."""
    return RecipeIngredientUpdateFactory.build()
    


@pytest.fixture
def pagination_request():
    """Default pagination request for testing."""
    return PaginationRequest()


@pytest_asyncio.fixture
async def recipe_ingredient_repository(mock_session_async):
    """Create RecipeIngredientRepository instance with test session."""
    return RecipeIngredientRepository(mock_session_async)


@pytest.fixture
def multiple_recipe_ingredient():
    """Create multiple RecipeIngredient instances for testing."""
    return [RecipeIngredientModelFactory.build(recipe_id=i + 1) for i in range(5)]
