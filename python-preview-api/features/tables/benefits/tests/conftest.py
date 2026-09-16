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
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from tests.conftest import get_test_time, get_test_date

from core.pagination import PaginationRequest
from features.tables.benefits.models import BenefitModel
from features.tables.benefits.schemas import BenefitCreate, BenefitUpdate, BenefitFilter
from features.tables.benefits.repository import BenefitRepository
from features.tables.benefits.service import BenefitService

class BenefitModelFactory(SQLAlchemyFactory[BenefitModel]):
    __model__ = BenefitModel
    __set_relationships__ = False
    __random_seed__ = 0



class BenefitCreateFactory(ModelFactory[BenefitCreate]):
    __model__ = BenefitCreate
    __random_seed__ = 0


class BenefitUpdateFactory(ModelFactory[BenefitUpdate]):
    __model__ = BenefitUpdate
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
    """Sample benefit data for testing."""
    return BenefitCreateFactory.build().model_dump()

@pytest.fixture
def existing_benefit(sample_data):
    """Sample Benefit model instance for testing."""
    return BenefitModelFactory.build(benefit_id=1)

@pytest.fixture
def updated_benefit_model():
    """Sample Benefit model instance with changes for testing."""
    return BenefitModelFactory.build(benefit_id=7)

@pytest.fixture
def updated_benefit():
    """Sample Benefit model instance with changes for testing."""
    return BenefitUpdateFactory.build()
    


@pytest.fixture
def pagination_request():
    """Default pagination request for testing."""
    return PaginationRequest()


@pytest_asyncio.fixture
async def benefit_repository(mock_session_async):
    """Create BenefitRepository instance with test session."""
    return BenefitRepository(mock_session_async)


@pytest.fixture
def multiple_benefits():
    """Create multiple Benefit instances for testing."""
    return [BenefitModelFactory.build(benefit_id=i + 1) for i in range(5)]
