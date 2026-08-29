# ROSETIC:crud-guid


"""
Unit tests for the LeafService layer.
"""

from pydantic import ValidationError
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from decimal import Decimal
from sqlalchemy.exc import SQLAlchemyError

from core.pagination import PaginatedResponse
from features.tables.leaves.models import LeafModel
from features.tables.leaves.schemas import LeafResponse, LeafCreate, LeafUpdate, LeafFilter
from features.tables.leaves.service import LeafService
from features.tables.leaves.repository import LeafRepository

class TestLeafService:
    """Test cases for LeafService layer."""


    @pytest.fixture
    def mock_repository(self):
        """Create a mock LeafRepository."""
        return AsyncMock(spec=LeafRepository)

    @pytest.fixture
    def service_with_mock_repo(self, mock_session_async, mock_repository):
        """Create LeafService with mocked repository."""
        service = LeafService(mock_session_async)
        service.repo = mock_repository
        return service

    # ─── Create operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_create_leaf_success(self, service_with_mock_repo, mock_repository, sample_data, existing_leaf):
        """Test successful leaves creation through service."""
        # Arrange
        new_item = LeafCreate(**sample_data)
        mock_repository.create.return_value = existing_leaf
        
        # Act
        result = await service_with_mock_repo.create(new_item)
        
        # Assert
        assert isinstance(result, LeafResponse)
        mock_repository.create.assert_called_once()

    # # ─── Read operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_get_leaf_by_id_success(self, service_with_mock_repo, mock_repository, existing_leaf):
        """Test successful retrieval of leaf by ID."""
        # Arrange
        mock_repository.get_by_id.return_value = existing_leaf
        
        # Act
        result = await service_with_mock_repo.get_by_id(1)
        
        # Assert
        assert isinstance(result, LeafResponse)
        mock_repository.get_by_id.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_get_leaf_by_id_not_found(self, service_with_mock_repo, mock_repository):
        """Test retrieval of non-existent leaf."""
        # Arrange
        mock_repository.get_by_id.return_value = None
        
        # Act
        result = await service_with_mock_repo.get_by_id(999)
        
        # Assert
        assert result is None
        mock_repository.get_by_id.assert_called_once_with(999)

    @pytest.mark.asyncio
    async def test_get_all_success(self, service_with_mock_repo, mock_repository, multiple_leaves, pagination_request):
        """Test successful retrieval of all leaves."""
        # Arrange
        mock_repository.get_all.return_value = (multiple_leaves, len(multiple_leaves))
        
        # Act
        result = await service_with_mock_repo.get_all(pagination_request)
        
        # Assert
        assert isinstance(result, PaginatedResponse)
        assert len(result.items) == len(multiple_leaves)
        assert result.total == len(multiple_leaves)
        mock_repository.get_all.assert_called_once_with(pagination_request)

    

    @pytest.mark.asyncio
    async def test_search_success(self, service_with_mock_repo, mock_repository, multiple_leaves, pagination_request):
        """Test successful search with filters."""
        # Arrange
        filters = LeafFilter()
        mock_repository.search.return_value = (multiple_leaves, len(multiple_leaves))
        
        # Act
        result = await service_with_mock_repo.search(filters, pagination_request)
        
        # Assert
        assert isinstance(result, PaginatedResponse)
        assert len(result.items) == len(multiple_leaves)
        assert result.total == len(multiple_leaves)
        
        # Verify repository was called with correct filter dict
        mock_repository.search.assert_called_once_with(filters, pagination_request)

    @pytest.mark.asyncio
    async def test_search_empty_results(self, service_with_mock_repo, mock_repository, pagination_request):
        """Test search with no matching results."""
        # Arrange
        filters = LeafFilter()
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
    async def test_update_leaf_by_id_success(self, service_with_mock_repo, mock_repository, updated_leaf_model):
        """Test successful leaf update."""
        # Arrange
        mock_repository.update_by_id.return_value = updated_leaf_model
        
        # Act
        result = await service_with_mock_repo.update_by_id(1, LeafUpdate())
        
        # Assert
        assert isinstance(result, LeafResponse)
        mock_repository.update_by_id.assert_called_once_with(1, LeafUpdate().model_dump(exclude_unset=True))

    # # ─── Delete operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_delete_by_id_success(self, service_with_mock_repo, mock_repository):
        """Test successful leaf deletion."""
        # Arrange
        mock_repository.delete_by_id.return_value = True
        
        # Act
        result = await service_with_mock_repo.delete_by_id(1)
        
        # Assert
        assert result is True
        mock_repository.delete_by_id.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_delete_by_id_not_found(self, service_with_mock_repo, mock_repository):
        """Test deletion of non-existent leaf."""
        # Arrange
        mock_repository.delete_by_id.return_value = False
        
        # Act
        result = await service_with_mock_repo.delete_by_id(999)
        
        # Assert
        assert result is False
        mock_repository.delete_by_id.assert_called_once_with(999)
