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
from features.tables.employees.models import EmployeeModel
from features.tables.employees.schemas import EmployeeCreate, EmployeeUpdate, EmployeeFilter
from features.tables.employees.repository import EmployeeRepository
from features.tables.employees.service import EmployeeService

class EmployeeModelFactory(SQLAlchemyFactory[EmployeeModel]):
    __model__ = EmployeeModel
    __set_relationships__ = False
    __random_seed__ = 0



class EmployeeCreateFactory(ModelFactory[EmployeeCreate]):
    __model__ = EmployeeCreate
    __random_seed__ = 0


class EmployeeUpdateFactory(ModelFactory[EmployeeUpdate]):
    __model__ = EmployeeUpdate
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
    """Sample employee data for testing."""
    return EmployeeCreateFactory.build().model_dump()

@pytest.fixture
def existing_employee(sample_data):
    """Sample Employee model instance for testing."""
    return EmployeeModelFactory.build(employee_id=1)

@pytest.fixture
def updated_employee_model():
    """Sample Employee model instance with changes for testing."""
    return EmployeeModelFactory.build(employee_id=7)

@pytest.fixture
def updated_employee():
    """Sample Employee model instance with changes for testing."""
    return EmployeeUpdateFactory.build()
    


@pytest.fixture
def pagination_request():
    """Default pagination request for testing."""
    return PaginationRequest()


@pytest_asyncio.fixture
async def employee_repository(mock_session_async):
    """Create EmployeeRepository instance with test session."""
    return EmployeeRepository(mock_session_async)


@pytest.fixture
def multiple_employees():
    """Create multiple Employee instances for testing."""
    return [EmployeeModelFactory.build(employee_id=i + 1) for i in range(5)]
