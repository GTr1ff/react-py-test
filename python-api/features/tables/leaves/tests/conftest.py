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
from features.tables.leaves.models import LeafModel
from features.tables.leaves.schemas import LeafCreate, LeafUpdate, LeafFilter
from features.tables.leaves.repository import LeafRepository
from features.tables.leaves.service import LeafService

class LeafModelFactory(SQLAlchemyFactory[LeafModel]):
    __model__ = LeafModel
    __set_relationships__ = False
    __random_seed__ = 0



class LeafCreateFactory(ModelFactory[LeafCreate]):
    __model__ = LeafCreate
    __random_seed__ = 0


class LeafUpdateFactory(ModelFactory[LeafUpdate]):
    __model__ = LeafUpdate
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
    """Sample leaf data for testing."""
    return LeafCreateFactory.build().model_dump()

@pytest.fixture
def existing_leaf(sample_data):
    """Sample Leaf model instance for testing."""
    return LeafModelFactory.build(leave_id=1)

@pytest.fixture
def updated_leaf_model():
    """Sample Leaf model instance with changes for testing."""
    return LeafModelFactory.build(leave_id=7)

@pytest.fixture
def updated_leaf():
    """Sample Leaf model instance with changes for testing."""
    return LeafUpdateFactory.build()
    


@pytest.fixture
def pagination_request():
    """Default pagination request for testing."""
    return PaginationRequest()


@pytest_asyncio.fixture
async def leaf_repository(mock_session_async):
    """Create LeafRepository instance with test session."""
    return LeafRepository(mock_session_async)


@pytest.fixture
def multiple_leaves():
    """Create multiple Leaf instances for testing."""
    return [LeafModelFactory.build(leave_id=i + 1) for i in range(5)]
