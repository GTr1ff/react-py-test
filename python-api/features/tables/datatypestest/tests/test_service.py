# ROSETIC:crud-guid


"""
Unit tests for the DatatypestestService layer.
"""
import uuid
from pydantic import ValidationError
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from decimal import Decimal
from sqlalchemy.exc import SQLAlchemyError

from core.pagination import PaginatedResponse
from features.tables.datatypestest.models import DatatypestestModel
from features.tables.datatypestest.schemas import DatatypestestResponse, DatatypestestCreate, DatatypestestUpdate, DatatypestestFilter
from features.tables.datatypestest.service import DatatypestestService
from features.tables.datatypestest.repository import DatatypestestRepository

class TestDatatypestestService:
    """Test cases for DatatypestestService layer."""


    @pytest.fixture
    def mock_repository(self):
        """Create a mock DatatypestestRepository."""
        return AsyncMock(spec=DatatypestestRepository)

    @pytest.fixture
    def service_with_mock_repo(self, mock_session_async, mock_repository):
        """Create DatatypestestService with mocked repository."""
        service = DatatypestestService(mock_session_async)
        service.repo = mock_repository
        return service

    # ─── Create operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_create_datatypestest_success(self, service_with_mock_repo, mock_repository, sample_data, existing_datatypestest):
        """Test successful datatypestest creation through service."""
        # Arrange
        new_item = DatatypestestCreate(**sample_data)
        mock_repository.create.return_value = existing_datatypestest
        
        # Act
        result = await service_with_mock_repo.create(new_item)
        
        # Assert
        assert isinstance(result, DatatypestestResponse)
        mock_repository.create.assert_called_once()

    # # ─── Read operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_get_datatypestest_by_keykey_success(self, service_with_mock_repo, mock_repository, existing_datatypestest):
        """Test successful retrieval of datatypestest by ID."""
        # Arrange
        mock_repository.get_by_keykey.return_value = existing_datatypestest
        
        # Act
        result = await service_with_mock_repo.get_by_keykey(1)
        
        # Assert
        assert isinstance(result, DatatypestestResponse)
        mock_repository.get_by_keykey.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_get_datatypestest_by_keykey_not_found(self, service_with_mock_repo, mock_repository):
        """Test retrieval of non-existent datatypestest."""
        # Arrange
        mock_repository.get_by_keykey.return_value = None
        
        # Act
        result = await service_with_mock_repo.get_by_keykey(999)
        
        # Assert
        assert result is None
        mock_repository.get_by_keykey.assert_called_once_with(999)

    @pytest.mark.asyncio
    async def test_get_all_success(self, service_with_mock_repo, mock_repository, multiple_datatypestest, pagination_request):
        """Test successful retrieval of all datatypestest."""
        # Arrange
        mock_repository.get_all.return_value = (multiple_datatypestest, len(multiple_datatypestest))
        
        # Act
        result = await service_with_mock_repo.get_all(pagination_request)
        
        # Assert
        assert isinstance(result, PaginatedResponse)
        assert len(result.items) == len(multiple_datatypestest)
        assert result.total == len(multiple_datatypestest)
        mock_repository.get_all.assert_called_once_with(pagination_request)

    

    @pytest.mark.asyncio
    async def test_search_success(self, service_with_mock_repo, mock_repository, multiple_datatypestest, pagination_request):
        """Test successful search with filters."""
        # Arrange
        filters = DatatypestestFilter()
        mock_repository.search.return_value = (multiple_datatypestest, len(multiple_datatypestest))
        
        # Act
        result = await service_with_mock_repo.search(filters, pagination_request)
        
        # Assert
        assert isinstance(result, PaginatedResponse)
        assert len(result.items) == len(multiple_datatypestest)
        assert result.total == len(multiple_datatypestest)
        
        # Verify repository was called with correct filter dict
        mock_repository.search.assert_called_once_with(filters, pagination_request)

    @pytest.mark.asyncio
    async def test_search_empty_results(self, service_with_mock_repo, mock_repository, pagination_request):
        """Test search with no matching results."""
        # Arrange
        filters = DatatypestestFilter()
        mock_repository.search.return_value = ([], 0)
        
        # Act
        result = await service_with_mock_repo.search(filters, pagination_request)
        
        # Assert
        assert isinstance(result, PaginatedResponse)
        assert len(result.items) == 0
        assert result.total == 0
        mock_repository.search.assert_called_once_with(filters, pagination_request)

    # # ─── Update operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_update_datatypestest_by_keykey_success(self, service_with_mock_repo, mock_repository, updated_datatypestest_model):
        """Test successful datatypestest update."""
        # Arrange
        mock_repository.update_by_keykey.return_value = updated_datatypestest_model
        
        # Act
        result = await service_with_mock_repo.update_by_keykey(1, DatatypestestUpdate())
        
        # Assert
        assert isinstance(result, DatatypestestResponse)
        mock_repository.update_by_keykey.assert_called_once_with(1, DatatypestestUpdate().model_dump(exclude_unset=True))

    # # ─── Delete operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_delete_by_keykey_success(self, service_with_mock_repo, mock_repository):
        """Test successful datatypestest deletion."""
        # Arrange
        mock_repository.delete_by_keykey.return_value = True
        
        # Act
        result = await service_with_mock_repo.delete_by_keykey(1)
        
        # Assert
        assert result is True
        mock_repository.delete_by_keykey.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_delete_by_keykey_not_found(self, service_with_mock_repo, mock_repository):
        """Test deletion of non-existent datatypestest."""
        # Arrange
        mock_repository.delete_by_keykey.return_value = False
        
        # Act
        result = await service_with_mock_repo.delete_by_keykey(999)
        
        # Assert
        assert result is False
        mock_repository.delete_by_keykey.assert_called_once_with(999)
