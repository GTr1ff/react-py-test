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
from features.tables.locations.models import LocationModel
from features.tables.locations.schemas import LocationCreate, LocationUpdate, LocationFilter
from features.tables.locations.repository import LocationRepository
from features.tables.locations.service import LocationService

class LocationModelFactory(SQLAlchemyFactory[LocationModel]):
    __model__ = LocationModel
    __set_relationships__ = False
    __random_seed__ = 0



class LocationCreateFactory(ModelFactory[LocationCreate]):
    __model__ = LocationCreate
    __random_seed__ = 0


class LocationUpdateFactory(ModelFactory[LocationUpdate]):
    __model__ = LocationUpdate
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
    """Sample location data for testing."""
    return LocationCreateFactory.build().model_dump()

@pytest.fixture
def existing_location(sample_data):
    """Sample Location model instance for testing."""
    return LocationModelFactory.build(location_id=1)

@pytest.fixture
def updated_location_model():
    """Sample Location model instance with changes for testing."""
    return LocationModelFactory.build(location_id=7)

@pytest.fixture
def updated_location():
    """Sample Location model instance with changes for testing."""
    return LocationUpdateFactory.build()
    


@pytest.fixture
def pagination_request():
    """Default pagination request for testing."""
    return PaginationRequest()


@pytest_asyncio.fixture
async def location_repository(mock_session_async):
    """Create LocationRepository instance with test session."""
    return LocationRepository(mock_session_async)


@pytest.fixture
def multiple_locations():
    """Create multiple Location instances for testing."""
    return [LocationModelFactory.build(location_id=i + 1) for i in range(5)]
