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
from features.tables.memos.models import MemoModel
from features.tables.memos.schemas import MemoCreate, MemoUpdate, MemoFilter
from features.tables.memos.repository import MemoRepository
from features.tables.memos.service import MemoService

class MemoModelFactory(SQLAlchemyFactory[MemoModel]):
    __model__ = MemoModel
    __set_relationships__ = False
    __random_seed__ = 0

    # JSON-backed array columns can default to a dict from the factory; 
    # Force cc_employees to match the list[int] schema.
    @classmethod
    def cc_employees(cls) -> list[int]:
        return cls.__faker__.pylist(value_types=[int])


class MemoCreateFactory(ModelFactory[MemoCreate]):
    __model__ = MemoCreate
    __random_seed__ = 0


class MemoUpdateFactory(ModelFactory[MemoUpdate]):
    __model__ = MemoUpdate
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
    """Sample memo data for testing."""
    return MemoCreateFactory.build().model_dump()

@pytest.fixture
def existing_memo(sample_data):
    """Sample Memo model instance for testing."""
    return MemoModelFactory.build(memo_id=1)

@pytest.fixture
def updated_memo_model():
    """Sample Memo model instance with changes for testing."""
    return MemoModelFactory.build(memo_id=7)

@pytest.fixture
def updated_memo():
    """Sample Memo model instance with changes for testing."""
    return MemoUpdateFactory.build()
    


@pytest.fixture
def pagination_request():
    """Default pagination request for testing."""
    return PaginationRequest()


@pytest_asyncio.fixture
async def memo_repository(mock_session_async):
    """Create MemoRepository instance with test session."""
    return MemoRepository(mock_session_async)


@pytest.fixture
def multiple_memos():
    """Create multiple Memo instances for testing."""
    return [MemoModelFactory.build(memo_id=i + 1) for i in range(5)]
