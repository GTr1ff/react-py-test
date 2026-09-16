# ROSETIC:crud-guid

"""
Shared test fixtures and configuration for the test suite.
"""


import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock
from polyfactory.factories.pydantic_factory import ModelFactory
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory




from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker


from core.pagination import PaginationRequest
from features.tables.roles.models import RoleModel
from features.tables.roles.schemas import RoleCreate, RoleUpdate, RoleFilter
from features.tables.roles.repository import RoleRepository
from features.tables.roles.service import RoleService

class RoleModelFactory(SQLAlchemyFactory[RoleModel]):
    __model__ = RoleModel
    __set_relationships__ = False
    __random_seed__ = 0

    # JSON-backed array columns can default to a dict from the factory; 
    # Force privileges to match the list[str] schema.
    @classmethod
    def privileges(cls) -> list[str]:
        return cls.__faker__.pylist(value_types=[str])


class RoleCreateFactory(ModelFactory[RoleCreate]):
    __model__ = RoleCreate
    __random_seed__ = 0


class RoleUpdateFactory(ModelFactory[RoleUpdate]):
    __model__ = RoleUpdate
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
    """Sample role data for testing."""
    return RoleCreateFactory.build().model_dump()

@pytest.fixture
def existing_role(sample_data):
    """Sample Role model instance for testing."""
    return RoleModelFactory.build(role_id=1)

@pytest.fixture
def updated_role_model():
    """Sample Role model instance with changes for testing."""
    return RoleModelFactory.build(role_id=7)

@pytest.fixture
def updated_role():
    """Sample Role model instance with changes for testing."""
    return RoleUpdateFactory.build()
    


@pytest.fixture
def pagination_request():
    """Default pagination request for testing."""
    return PaginationRequest()


@pytest_asyncio.fixture
async def role_repository(mock_session_async):
    """Create RoleRepository instance with test session."""
    return RoleRepository(mock_session_async)


@pytest.fixture
def multiple_roles():
    """Create multiple Role instances for testing."""
    return [RoleModelFactory.build(role_id=i + 1) for i in range(5)]
