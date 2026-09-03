# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c

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
from features.tables.audit_log.models import AuditLogModel
from features.tables.audit_log.schemas import AuditLogCreate, AuditLogUpdate, AuditLogFilter
from features.tables.audit_log.repository import AuditLogRepository
from features.tables.audit_log.service import AuditLogService

class AuditLogModelFactory(SQLAlchemyFactory[AuditLogModel]):
    __model__ = AuditLogModel
    __set_relationships__ = False
    __random_seed__ = 0



class AuditLogCreateFactory(ModelFactory[AuditLogCreate]):
    __model__ = AuditLogCreate
    __random_seed__ = 0


class AuditLogUpdateFactory(ModelFactory[AuditLogUpdate]):
    __model__ = AuditLogUpdate
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
    """Sample audit_log data for testing."""
    return AuditLogCreateFactory.build().model_dump()

@pytest.fixture
def existing_audit_log(sample_data):
    """Sample AuditLog model instance for testing."""
    return AuditLogModelFactory.build(id=1)

@pytest.fixture
def updated_audit_log_model():
    """Sample AuditLog model instance with changes for testing."""
    return AuditLogModelFactory.build(id=7)

@pytest.fixture
def updated_audit_log():
    """Sample AuditLog model instance with changes for testing."""
    return AuditLogUpdateFactory.build()
    


@pytest.fixture
def pagination_request():
    """Default pagination request for testing."""
    return PaginationRequest()


@pytest_asyncio.fixture
async def audit_log_repository(mock_session_async):
    """Create AuditLogRepository instance with test session."""
    return AuditLogRepository(mock_session_async)


@pytest.fixture
def multiple_audit_log():
    """Create multiple AuditLog instances for testing."""
    return [AuditLogModelFactory.build(id=i + 1) for i in range(5)]
