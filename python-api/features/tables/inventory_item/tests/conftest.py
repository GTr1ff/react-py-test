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
from features.tables.inventory_item.models import InventoryItemModel
from features.tables.inventory_item.schemas import InventoryItemCreate, InventoryItemUpdate, InventoryItemFilter
from features.tables.inventory_item.repository import InventoryItemRepository
from features.tables.inventory_item.service import InventoryItemService

class InventoryItemModelFactory(SQLAlchemyFactory[InventoryItemModel]):
    __model__ = InventoryItemModel
    __set_relationships__ = False
    __random_seed__ = 0



class InventoryItemCreateFactory(ModelFactory[InventoryItemCreate]):
    __model__ = InventoryItemCreate
    __random_seed__ = 0


class InventoryItemUpdateFactory(ModelFactory[InventoryItemUpdate]):
    __model__ = InventoryItemUpdate
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
    """Sample inventory_item data for testing."""
    return InventoryItemCreateFactory.build().model_dump()

@pytest.fixture
def existing_inventory_item(sample_data):
    """Sample InventoryItem model instance for testing."""
    return InventoryItemModelFactory.build(id=1)

@pytest.fixture
def updated_inventory_item_model():
    """Sample InventoryItem model instance with changes for testing."""
    return InventoryItemModelFactory.build(id=7)

@pytest.fixture
def updated_inventory_item():
    """Sample InventoryItem model instance with changes for testing."""
    return InventoryItemUpdateFactory.build()
    


@pytest.fixture
def pagination_request():
    """Default pagination request for testing."""
    return PaginationRequest()


@pytest_asyncio.fixture
async def inventory_item_repository(mock_session_async):
    """Create InventoryItemRepository instance with test session."""
    return InventoryItemRepository(mock_session_async)


@pytest.fixture
def multiple_inventory_item():
    """Create multiple InventoryItem instances for testing."""
    return [InventoryItemModelFactory.build(id=i + 1) for i in range(5)]
