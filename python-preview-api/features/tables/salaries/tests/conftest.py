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
from features.tables.salaries.models import SalaryModel
from features.tables.salaries.schemas import SalaryCreate, SalaryUpdate, SalaryFilter
from features.tables.salaries.repository import SalaryRepository
from features.tables.salaries.service import SalaryService

class SalaryModelFactory(SQLAlchemyFactory[SalaryModel]):
    __model__ = SalaryModel
    __set_relationships__ = False
    __random_seed__ = 0



class SalaryCreateFactory(ModelFactory[SalaryCreate]):
    __model__ = SalaryCreate
    __random_seed__ = 0


class SalaryUpdateFactory(ModelFactory[SalaryUpdate]):
    __model__ = SalaryUpdate
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
    """Sample salary data for testing."""
    return SalaryCreateFactory.build().model_dump()

@pytest.fixture
def existing_salary(sample_data):
    """Sample Salary model instance for testing."""
    return SalaryModelFactory.build(salary_id=1)

@pytest.fixture
def updated_salary_model():
    """Sample Salary model instance with changes for testing."""
    return SalaryModelFactory.build(salary_id=7)

@pytest.fixture
def updated_salary():
    """Sample Salary model instance with changes for testing."""
    return SalaryUpdateFactory.build()
    


@pytest.fixture
def pagination_request():
    """Default pagination request for testing."""
    return PaginationRequest()


@pytest_asyncio.fixture
async def salary_repository(mock_session_async):
    """Create SalaryRepository instance with test session."""
    return SalaryRepository(mock_session_async)


@pytest.fixture
def multiple_salaries():
    """Create multiple Salary instances for testing."""
    return [SalaryModelFactory.build(salary_id=i + 1) for i in range(5)]
