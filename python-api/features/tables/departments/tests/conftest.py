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
from features.tables.departments.models import DepartmentModel
from features.tables.departments.schemas import DepartmentCreate, DepartmentUpdate, DepartmentFilter
from features.tables.departments.repository import DepartmentRepository
from features.tables.departments.service import DepartmentService

class DepartmentModelFactory(SQLAlchemyFactory[DepartmentModel]):
    __model__ = DepartmentModel
    __set_relationships__ = False
    __random_seed__ = 0



class DepartmentCreateFactory(ModelFactory[DepartmentCreate]):
    __model__ = DepartmentCreate
    __random_seed__ = 0


class DepartmentUpdateFactory(ModelFactory[DepartmentUpdate]):
    __model__ = DepartmentUpdate
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
    """Sample department data for testing."""
    return DepartmentCreateFactory.build().model_dump()

@pytest.fixture
def existing_department(sample_data):
    """Sample Department model instance for testing."""
    return DepartmentModelFactory.build(department_id=1)

@pytest.fixture
def updated_department_model():
    """Sample Department model instance with changes for testing."""
    return DepartmentModelFactory.build(department_id=7)

@pytest.fixture
def updated_department():
    """Sample Department model instance with changes for testing."""
    return DepartmentUpdateFactory.build()
    


@pytest.fixture
def pagination_request():
    """Default pagination request for testing."""
    return PaginationRequest()


@pytest_asyncio.fixture
async def department_repository(mock_session_async):
    """Create DepartmentRepository instance with test session."""
    return DepartmentRepository(mock_session_async)


@pytest.fixture
def multiple_departments():
    """Create multiple Department instances for testing."""
    return [DepartmentModelFactory.build(department_id=i + 1) for i in range(5)]
