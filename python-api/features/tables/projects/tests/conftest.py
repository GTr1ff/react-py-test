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
from features.tables.projects.models import ProjectModel
from features.tables.projects.schemas import ProjectCreate, ProjectUpdate, ProjectFilter
from features.tables.projects.repository import ProjectRepository
from features.tables.projects.service import ProjectService

class ProjectModelFactory(SQLAlchemyFactory[ProjectModel]):
    __model__ = ProjectModel
    __set_relationships__ = False
    __random_seed__ = 0

    # JSON-backed array columns can default to a dict from the factory; 
    # Force tags to match the list[str] schema.
    @classmethod
    def tags(cls) -> list[str]:
        return cls.__faker__.pylist(value_types=[str])


class ProjectCreateFactory(ModelFactory[ProjectCreate]):
    __model__ = ProjectCreate
    __random_seed__ = 0


class ProjectUpdateFactory(ModelFactory[ProjectUpdate]):
    __model__ = ProjectUpdate
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
    """Sample project data for testing."""
    return ProjectCreateFactory.build().model_dump()

@pytest.fixture
def existing_project(sample_data):
    """Sample Project model instance for testing."""
    return ProjectModelFactory.build(project_id=1)

@pytest.fixture
def updated_project_model():
    """Sample Project model instance with changes for testing."""
    return ProjectModelFactory.build(project_id=7)

@pytest.fixture
def updated_project():
    """Sample Project model instance with changes for testing."""
    return ProjectUpdateFactory.build()
    


@pytest.fixture
def pagination_request():
    """Default pagination request for testing."""
    return PaginationRequest()


@pytest_asyncio.fixture
async def project_repository(mock_session_async):
    """Create ProjectRepository instance with test session."""
    return ProjectRepository(mock_session_async)


@pytest.fixture
def multiple_projects():
    """Create multiple Project instances for testing."""
    return [ProjectModelFactory.build(project_id=i + 1) for i in range(5)]
