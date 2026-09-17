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
from features.tables.tag.models import TagModel
from features.tables.tag.schemas import TagCreate, TagUpdate, TagFilter
from features.tables.tag.repository import TagRepository
from features.tables.tag.service import TagService

class TagModelFactory(SQLAlchemyFactory[TagModel]):
    __model__ = TagModel
    __set_relationships__ = False
    __random_seed__ = 0



class TagCreateFactory(ModelFactory[TagCreate]):
    __model__ = TagCreate
    __random_seed__ = 0


class TagUpdateFactory(ModelFactory[TagUpdate]):
    __model__ = TagUpdate
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
    """Sample tag data for testing."""
    return TagCreateFactory.build().model_dump()

@pytest.fixture
def existing_tag(sample_data):
    """Sample Tag model instance for testing."""
    return TagModelFactory.build(id=1)

@pytest.fixture
def updated_tag_model():
    """Sample Tag model instance with changes for testing."""
    return TagModelFactory.build(id=7)

@pytest.fixture
def updated_tag():
    """Sample Tag model instance with changes for testing."""
    return TagUpdateFactory.build()
    


@pytest.fixture
def pagination_request():
    """Default pagination request for testing."""
    return PaginationRequest()


@pytest_asyncio.fixture
async def tag_repository(mock_session_async):
    """Create TagRepository instance with test session."""
    return TagRepository(mock_session_async)


@pytest.fixture
def multiple_tag():
    """Create multiple Tag instances for testing."""
    return [TagModelFactory.build(id=i + 1) for i in range(5)]
