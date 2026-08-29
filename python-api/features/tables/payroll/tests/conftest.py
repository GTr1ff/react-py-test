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
from features.tables.payroll.models import PayrollModel
from features.tables.payroll.schemas import PayrollCreate, PayrollUpdate, PayrollFilter
from features.tables.payroll.repository import PayrollRepository
from features.tables.payroll.service import PayrollService

class PayrollModelFactory(SQLAlchemyFactory[PayrollModel]):
    __model__ = PayrollModel
    __set_relationships__ = False
    __random_seed__ = 0



class PayrollCreateFactory(ModelFactory[PayrollCreate]):
    __model__ = PayrollCreate
    __random_seed__ = 0


class PayrollUpdateFactory(ModelFactory[PayrollUpdate]):
    __model__ = PayrollUpdate
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
    """Sample payroll data for testing."""
    return PayrollCreateFactory.build().model_dump()

@pytest.fixture
def existing_payroll(sample_data):
    """Sample Payroll model instance for testing."""
    return PayrollModelFactory.build(payroll_id=1)

@pytest.fixture
def updated_payroll_model():
    """Sample Payroll model instance with changes for testing."""
    return PayrollModelFactory.build(payroll_id=7)

@pytest.fixture
def updated_payroll():
    """Sample Payroll model instance with changes for testing."""
    return PayrollUpdateFactory.build()
    


@pytest.fixture
def pagination_request():
    """Default pagination request for testing."""
    return PaginationRequest()


@pytest_asyncio.fixture
async def payroll_repository(mock_session_async):
    """Create PayrollRepository instance with test session."""
    return PayrollRepository(mock_session_async)


@pytest.fixture
def multiple_payroll():
    """Create multiple Payroll instances for testing."""
    return [PayrollModelFactory.build(payroll_id=i + 1) for i in range(5)]
