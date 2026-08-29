# ROSETIC:crud-guid

"""
Shared test fixtures and configuration for the test suite.
"""


import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock
from polyfactory.factories.pydantic_factory import ModelFactory
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory

import base64


from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker


from core.pagination import PaginationRequest
from features.tables.documents.models import DocumentModel
from features.tables.documents.schemas import DocumentCreate, DocumentUpdate, DocumentFilter
from features.tables.documents.repository import DocumentRepository
from features.tables.documents.service import DocumentService

class DocumentModelFactory(SQLAlchemyFactory[DocumentModel]):
    __model__ = DocumentModel
    __set_relationships__ = False
    __random_seed__ = 0



class DocumentCreateFactory(ModelFactory[DocumentCreate]):
    __model__ = DocumentCreate
    __random_seed__ = 0


class DocumentUpdateFactory(ModelFactory[DocumentUpdate]):
    __model__ = DocumentUpdate
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
    """Sample document data for testing."""
    return DocumentCreateFactory.build().model_dump()

@pytest.fixture
def existing_document(sample_data):
    """Sample Document model instance for testing."""
    return DocumentModelFactory.build(document_id=1)

@pytest.fixture
def updated_document_model():
    """Sample Document model instance with changes for testing."""
    return DocumentModelFactory.build(document_id=7)

@pytest.fixture
def updated_document():
    """Sample Document model instance with changes for testing."""
    return DocumentUpdateFactory.build()
    


@pytest.fixture
def pagination_request():
    """Default pagination request for testing."""
    return PaginationRequest()


@pytest_asyncio.fixture
async def document_repository(mock_session_async):
    """Create DocumentRepository instance with test session."""
    return DocumentRepository(mock_session_async)


@pytest.fixture
def multiple_documents():
    """Create multiple Document instances for testing."""
    return [DocumentModelFactory.build(document_id=i + 1) for i in range(5)]
