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
from features.tables.employee_benefits.models import EmployeeBenefitModel
from features.tables.employee_benefits.schemas import EmployeeBenefitCreate, EmployeeBenefitUpdate, EmployeeBenefitFilter
from features.tables.employee_benefits.repository import EmployeeBenefitRepository
from features.tables.employee_benefits.service import EmployeeBenefitService

class EmployeeBenefitModelFactory(SQLAlchemyFactory[EmployeeBenefitModel]):
    __model__ = EmployeeBenefitModel
    __set_relationships__ = False
    __random_seed__ = 0



class EmployeeBenefitCreateFactory(ModelFactory[EmployeeBenefitCreate]):
    __model__ = EmployeeBenefitCreate
    __random_seed__ = 0


class EmployeeBenefitUpdateFactory(ModelFactory[EmployeeBenefitUpdate]):
    __model__ = EmployeeBenefitUpdate
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
    """Sample employee_benefit data for testing."""
    return EmployeeBenefitCreateFactory.build().model_dump()

@pytest.fixture
def existing_employee_benefit(sample_data):
    """Sample EmployeeBenefit model instance for testing."""
    return EmployeeBenefitModelFactory.build(employee_benefit_id=1)

@pytest.fixture
def updated_employee_benefit_model():
    """Sample EmployeeBenefit model instance with changes for testing."""
    return EmployeeBenefitModelFactory.build(employee_benefit_id=7)

@pytest.fixture
def updated_employee_benefit():
    """Sample EmployeeBenefit model instance with changes for testing."""
    return EmployeeBenefitUpdateFactory.build()
    


@pytest.fixture
def pagination_request():
    """Default pagination request for testing."""
    return PaginationRequest()


@pytest_asyncio.fixture
async def employee_benefit_repository(mock_session_async):
    """Create EmployeeBenefitRepository instance with test session."""
    return EmployeeBenefitRepository(mock_session_async)


@pytest.fixture
def multiple_employee_benefits():
    """Create multiple EmployeeBenefit instances for testing."""
    return [EmployeeBenefitModelFactory.build(employee_benefit_id=i + 1) for i in range(5)]
