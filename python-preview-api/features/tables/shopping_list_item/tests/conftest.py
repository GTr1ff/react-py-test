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
from features.tables.shopping_list_item.models import ShoppingListItemModel
from features.tables.shopping_list_item.schemas import ShoppingListItemCreate, ShoppingListItemUpdate, ShoppingListItemFilter
from features.tables.shopping_list_item.repository import ShoppingListItemRepository
from features.tables.shopping_list_item.service import ShoppingListItemService

class ShoppingListItemModelFactory(SQLAlchemyFactory[ShoppingListItemModel]):
    __model__ = ShoppingListItemModel
    __set_relationships__ = False
    __random_seed__ = 0



class ShoppingListItemCreateFactory(ModelFactory[ShoppingListItemCreate]):
    __model__ = ShoppingListItemCreate
    __random_seed__ = 0


class ShoppingListItemUpdateFactory(ModelFactory[ShoppingListItemUpdate]):
    __model__ = ShoppingListItemUpdate
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
    """Sample shopping_list_item data for testing."""
    return ShoppingListItemCreateFactory.build().model_dump()

@pytest.fixture
def existing_shopping_list_item(sample_data):
    """Sample ShoppingListItem model instance for testing."""
    return ShoppingListItemModelFactory.build(id=1)

@pytest.fixture
def updated_shopping_list_item_model():
    """Sample ShoppingListItem model instance with changes for testing."""
    return ShoppingListItemModelFactory.build(id=7)

@pytest.fixture
def updated_shopping_list_item():
    """Sample ShoppingListItem model instance with changes for testing."""
    return ShoppingListItemUpdateFactory.build()
    


@pytest.fixture
def pagination_request():
    """Default pagination request for testing."""
    return PaginationRequest()


@pytest_asyncio.fixture
async def shopping_list_item_repository(mock_session_async):
    """Create ShoppingListItemRepository instance with test session."""
    return ShoppingListItemRepository(mock_session_async)


@pytest.fixture
def multiple_shopping_list_item():
    """Create multiple ShoppingListItem instances for testing."""
    return [ShoppingListItemModelFactory.build(id=i + 1) for i in range(5)]
