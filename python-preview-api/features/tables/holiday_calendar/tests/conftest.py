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
from features.tables.holiday_calendar.models import HolidayCalendarModel
from features.tables.holiday_calendar.schemas import HolidayCalendarCreate, HolidayCalendarUpdate, HolidayCalendarFilter
from features.tables.holiday_calendar.repository import HolidayCalendarRepository
from features.tables.holiday_calendar.service import HolidayCalendarService

class HolidayCalendarModelFactory(SQLAlchemyFactory[HolidayCalendarModel]):
    __model__ = HolidayCalendarModel
    __set_relationships__ = False
    __random_seed__ = 0



class HolidayCalendarCreateFactory(ModelFactory[HolidayCalendarCreate]):
    __model__ = HolidayCalendarCreate
    __random_seed__ = 0


class HolidayCalendarUpdateFactory(ModelFactory[HolidayCalendarUpdate]):
    __model__ = HolidayCalendarUpdate
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
    """Sample holiday_calendar data for testing."""
    return HolidayCalendarCreateFactory.build().model_dump()

@pytest.fixture
def existing_holiday_calendar(sample_data):
    """Sample HolidayCalendar model instance for testing."""
    return HolidayCalendarModelFactory.build(holiday_id=1)

@pytest.fixture
def updated_holiday_calendar_model():
    """Sample HolidayCalendar model instance with changes for testing."""
    return HolidayCalendarModelFactory.build(holiday_id=7)

@pytest.fixture
def updated_holiday_calendar():
    """Sample HolidayCalendar model instance with changes for testing."""
    return HolidayCalendarUpdateFactory.build()
    


@pytest.fixture
def pagination_request():
    """Default pagination request for testing."""
    return PaginationRequest()


@pytest_asyncio.fixture
async def holiday_calendar_repository(mock_session_async):
    """Create HolidayCalendarRepository instance with test session."""
    return HolidayCalendarRepository(mock_session_async)


@pytest.fixture
def multiple_holiday_calendar():
    """Create multiple HolidayCalendar instances for testing."""
    return [HolidayCalendarModelFactory.build(holiday_id=i + 1) for i in range(5)]
