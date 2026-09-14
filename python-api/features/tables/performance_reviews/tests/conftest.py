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
from features.tables.performance_reviews.models import PerformanceReviewModel
from features.tables.performance_reviews.schemas import PerformanceReviewCreate, PerformanceReviewUpdate, PerformanceReviewFilter
from features.tables.performance_reviews.repository import PerformanceReviewRepository
from features.tables.performance_reviews.service import PerformanceReviewService

class PerformanceReviewModelFactory(SQLAlchemyFactory[PerformanceReviewModel]):
    __model__ = PerformanceReviewModel
    __set_relationships__ = False
    __random_seed__ = 0



class PerformanceReviewCreateFactory(ModelFactory[PerformanceReviewCreate]):
    __model__ = PerformanceReviewCreate
    __random_seed__ = 0


class PerformanceReviewUpdateFactory(ModelFactory[PerformanceReviewUpdate]):
    __model__ = PerformanceReviewUpdate
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
    """Sample performance_review data for testing."""
    return PerformanceReviewCreateFactory.build().model_dump()

@pytest.fixture
def existing_performance_review(sample_data):
    """Sample PerformanceReview model instance for testing."""
    return PerformanceReviewModelFactory.build(review_id=1)

@pytest.fixture
def updated_performance_review_model():
    """Sample PerformanceReview model instance with changes for testing."""
    return PerformanceReviewModelFactory.build(review_id=7)

@pytest.fixture
def updated_performance_review():
    """Sample PerformanceReview model instance with changes for testing."""
    return PerformanceReviewUpdateFactory.build()
    


@pytest.fixture
def pagination_request():
    """Default pagination request for testing."""
    return PaginationRequest()


@pytest_asyncio.fixture
async def performance_review_repository(mock_session_async):
    """Create PerformanceReviewRepository instance with test session."""
    return PerformanceReviewRepository(mock_session_async)


@pytest.fixture
def multiple_performance_reviews():
    """Create multiple PerformanceReview instances for testing."""
    return [PerformanceReviewModelFactory.build(review_id=i + 1) for i in range(5)]
