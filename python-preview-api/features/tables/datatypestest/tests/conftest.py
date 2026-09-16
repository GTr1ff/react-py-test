# ROSETIC:crud-guid

"""
Shared test fixtures and configuration for the test suite.
"""


import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock
from polyfactory.factories.pydantic_factory import ModelFactory
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory
import uuid
import base64
import datetime
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from tests.conftest import get_test_time, get_test_date

from core.pagination import PaginationRequest
from features.tables.datatypestest.models import DatatypestestModel
from features.tables.datatypestest.schemas import DatatypestestCreate, DatatypestestUpdate, DatatypestestFilter
from features.tables.datatypestest.repository import DatatypestestRepository
from features.tables.datatypestest.service import DatatypestestService

class DatatypestestModelFactory(SQLAlchemyFactory[DatatypestestModel]):
    __model__ = DatatypestestModel
    __set_relationships__ = False
    __random_seed__ = 0

    # JSON-backed array columns can default to a dict from the factory;
    # Force set_col to match the list[str] schema.
    @classmethod
    def set_col(cls) -> list[str]:
        return cls.__faker__.pylist(nb_elements=4, value_types=[str])
    # JSON-backed array columns can default to a dict from the factory; 
    # Force int_array_col to match the list[int] schema.
    @classmethod
    def int_array_col(cls) -> list[int]:
        return cls.__faker__.pylist(value_types=[int])
    # JSON-backed array columns can default to a dict from the factory; 
    # Force text_array_col to match the list[str] schema.
    @classmethod
    def text_array_col(cls) -> list[str]:
        return cls.__faker__.pylist(value_types=[str])


class DatatypestestCreateFactory(ModelFactory[DatatypestestCreate]):
    __model__ = DatatypestestCreate
    __random_seed__ = 0


class DatatypestestUpdateFactory(ModelFactory[DatatypestestUpdate]):
    __model__ = DatatypestestUpdate
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
    """Sample datatypestest data for testing."""
    return DatatypestestCreateFactory.build().model_dump()

@pytest.fixture
def existing_datatypestest(sample_data):
    """Sample Datatypestest model instance for testing."""
    return DatatypestestModelFactory.build(keykey=1)

@pytest.fixture
def updated_datatypestest_model():
    """Sample Datatypestest model instance with changes for testing."""
    return DatatypestestModelFactory.build(keykey=7)

@pytest.fixture
def updated_datatypestest():
    """Sample Datatypestest model instance with changes for testing."""
    return DatatypestestUpdateFactory.build()
    


@pytest.fixture
def pagination_request():
    """Default pagination request for testing."""
    return PaginationRequest()


@pytest_asyncio.fixture
async def datatypestest_repository(mock_session_async):
    """Create DatatypestestRepository instance with test session."""
    return DatatypestestRepository(mock_session_async)


@pytest.fixture
def multiple_datatypestest():
    """Create multiple Datatypestest instances for testing."""
    return [DatatypestestModelFactory.build(keykey=i + 1) for i in range(5)]
