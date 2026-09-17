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
from features.tables.recipe.models import RecipeModel
from features.tables.recipe.schemas import RecipeCreate, RecipeUpdate, RecipeFilter
from features.tables.recipe.repository import RecipeRepository
from features.tables.recipe.service import RecipeService

class RecipeModelFactory(SQLAlchemyFactory[RecipeModel]):
    __model__ = RecipeModel
    __set_relationships__ = False
    __random_seed__ = 0



class RecipeCreateFactory(ModelFactory[RecipeCreate]):
    __model__ = RecipeCreate
    __random_seed__ = 0


class RecipeUpdateFactory(ModelFactory[RecipeUpdate]):
    __model__ = RecipeUpdate
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
    """Sample recipe data for testing."""
    return RecipeCreateFactory.build().model_dump()

@pytest.fixture
def existing_recipe(sample_data):
    """Sample Recipe model instance for testing."""
    return RecipeModelFactory.build(id=1)

@pytest.fixture
def updated_recipe_model():
    """Sample Recipe model instance with changes for testing."""
    return RecipeModelFactory.build(id=7)

@pytest.fixture
def updated_recipe():
    """Sample Recipe model instance with changes for testing."""
    return RecipeUpdateFactory.build()
    


@pytest.fixture
def pagination_request():
    """Default pagination request for testing."""
    return PaginationRequest()


@pytest_asyncio.fixture
async def recipe_repository(mock_session_async):
    """Create RecipeRepository instance with test session."""
    return RecipeRepository(mock_session_async)


@pytest.fixture
def multiple_recipe():
    """Create multiple Recipe instances for testing."""
    return [RecipeModelFactory.build(id=i + 1) for i in range(5)]
