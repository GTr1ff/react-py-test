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
from features.tables.consent.models import ConsentModel
from features.tables.consent.schemas import ConsentCreate, ConsentUpdate, ConsentFilter
from features.tables.consent.repository import ConsentRepository
from features.tables.consent.service import ConsentService

class ConsentModelFactory(SQLAlchemyFactory[ConsentModel]):
    __model__ = ConsentModel
    __set_relationships__ = False
    __random_seed__ = 0



class ConsentCreateFactory(ModelFactory[ConsentCreate]):
    __model__ = ConsentCreate
    __random_seed__ = 0


class ConsentUpdateFactory(ModelFactory[ConsentUpdate]):
    __model__ = ConsentUpdate
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
    """Sample consent data for testing."""
    return ConsentCreateFactory.build().model_dump()

@pytest.fixture
def existing_consent(sample_data):
    """Sample Consent model instance for testing."""
    return ConsentModelFactory.build(id=1)

@pytest.fixture
def updated_consent_model():
    """Sample Consent model instance with changes for testing."""
    return ConsentModelFactory.build(id=7)

@pytest.fixture
def updated_consent():
    """Sample Consent model instance with changes for testing."""
    return ConsentUpdateFactory.build()
    


@pytest.fixture
def pagination_request():
    """Default pagination request for testing."""
    return PaginationRequest()


@pytest_asyncio.fixture
async def consent_repository(mock_session_async):
    """Create ConsentRepository instance with test session."""
    return ConsentRepository(mock_session_async)


@pytest.fixture
def multiple_consent():
    """Create multiple Consent instances for testing."""
    return [ConsentModelFactory.build(id=i + 1) for i in range(5)]
