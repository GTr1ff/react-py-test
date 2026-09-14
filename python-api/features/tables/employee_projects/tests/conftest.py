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
from features.tables.employee_projects.models import EmployeeProjectModel
from features.tables.employee_projects.schemas import EmployeeProjectCreate, EmployeeProjectUpdate, EmployeeProjectFilter
from features.tables.employee_projects.repository import EmployeeProjectRepository
from features.tables.employee_projects.service import EmployeeProjectService

class EmployeeProjectModelFactory(SQLAlchemyFactory[EmployeeProjectModel]):
    __model__ = EmployeeProjectModel
    __set_relationships__ = False
    __random_seed__ = 0



class EmployeeProjectCreateFactory(ModelFactory[EmployeeProjectCreate]):
    __model__ = EmployeeProjectCreate
    __random_seed__ = 0


class EmployeeProjectUpdateFactory(ModelFactory[EmployeeProjectUpdate]):
    __model__ = EmployeeProjectUpdate
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
    """Sample employee_project data for testing."""
    return EmployeeProjectCreateFactory.build().model_dump()

@pytest.fixture
def existing_employee_project(sample_data):
    """Sample EmployeeProject model instance for testing."""
    return EmployeeProjectModelFactory.build(employee_project_id=1)

@pytest.fixture
def updated_employee_project_model():
    """Sample EmployeeProject model instance with changes for testing."""
    return EmployeeProjectModelFactory.build(employee_project_id=7)

@pytest.fixture
def updated_employee_project():
    """Sample EmployeeProject model instance with changes for testing."""
    return EmployeeProjectUpdateFactory.build()
    


@pytest.fixture
def pagination_request():
    """Default pagination request for testing."""
    return PaginationRequest()


@pytest_asyncio.fixture
async def employee_project_repository(mock_session_async):
    """Create EmployeeProjectRepository instance with test session."""
    return EmployeeProjectRepository(mock_session_async)


@pytest.fixture
def multiple_employee_projects():
    """Create multiple EmployeeProject instances for testing."""
    return [EmployeeProjectModelFactory.build(employee_project_id=i + 1) for i in range(5)]
