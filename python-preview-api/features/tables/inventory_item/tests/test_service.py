# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c


"""
Unit tests for the InventoryItemService layer.
"""

from pydantic import ValidationError
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from decimal import Decimal
from sqlalchemy.exc import SQLAlchemyError

from core.pagination import PaginatedResponse
from features.tables.inventory_item.models import InventoryItemModel
from features.tables.inventory_item.schemas import InventoryItemResponse, InventoryItemCreate, InventoryItemUpdate, InventoryItemFilter
from features.tables.inventory_item.service import InventoryItemService
from features.tables.inventory_item.repository import InventoryItemRepository

class TestInventoryItemService:
    """Test cases for InventoryItemService layer."""


    @pytest.fixture
    def mock_repository(self):
        """Create a mock InventoryItemRepository."""
        return AsyncMock(spec=InventoryItemRepository)

    @pytest.fixture
    def service_with_mock_repo(self, mock_session_async, mock_repository):
        """Create InventoryItemService with mocked repository."""
        service = InventoryItemService(mock_session_async)
        service.repo = mock_repository
        return service

    # ─── Create operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_create_inventory_item_success(self, service_with_mock_repo, mock_repository, sample_data, existing_inventory_item):
        """Test successful inventory_item creation through service."""
        # Arrange
        new_item = InventoryItemCreate(**sample_data)
        mock_repository.create.return_value = existing_inventory_item
        
        # Act
        result = await service_with_mock_repo.create(new_item)
        
        # Assert
        assert isinstance(result, InventoryItemResponse)
        mock_repository.create.assert_called_once()

    # # ─── Read operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_get_inventory_item_by_id_success(self, service_with_mock_repo, mock_repository, existing_inventory_item):
        """Test successful retrieval of inventory_item by ID."""
        # Arrange
        mock_repository.get_by_id.return_value = existing_inventory_item
        
        # Act
        result = await service_with_mock_repo.get_by_id(1)
        
        # Assert
        assert isinstance(result, InventoryItemResponse)
        mock_repository.get_by_id.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_get_inventory_item_by_id_not_found(self, service_with_mock_repo, mock_repository):
        """Test retrieval of non-existent inventory_item."""
        # Arrange
        mock_repository.get_by_id.return_value = None
        
        # Act
        result = await service_with_mock_repo.get_by_id(999)
        
        # Assert
        assert result is None
        mock_repository.get_by_id.assert_called_once_with(999)

    @pytest.mark.asyncio
    async def test_get_all_success(self, service_with_mock_repo, mock_repository, multiple_inventory_item, pagination_request):
        """Test successful retrieval of all inventory_item."""
        # Arrange
        mock_repository.get_all.return_value = (multiple_inventory_item, len(multiple_inventory_item))
        
        # Act
        result = await service_with_mock_repo.get_all(pagination_request)
        
        # Assert
        assert isinstance(result, PaginatedResponse)
        assert len(result.items) == len(multiple_inventory_item)
        assert result.total == len(multiple_inventory_item)
        mock_repository.get_all.assert_called_once_with(pagination_request)

    

    @pytest.mark.asyncio
    async def test_search_success(self, service_with_mock_repo, mock_repository, multiple_inventory_item, pagination_request):
        """Test successful search with filters."""
        # Arrange
        filters = InventoryItemFilter()
        mock_repository.search.return_value = (multiple_inventory_item, len(multiple_inventory_item))
        
        # Act
        result = await service_with_mock_repo.search(filters, pagination_request)
        
        # Assert
        assert isinstance(result, PaginatedResponse)
        assert len(result.items) == len(multiple_inventory_item)
        assert result.total == len(multiple_inventory_item)
        
        # Verify repository was called with correct filter dict
        mock_repository.search.assert_called_once_with(filters, pagination_request)

    @pytest.mark.asyncio
    async def test_search_empty_results(self, service_with_mock_repo, mock_repository, pagination_request):
        """Test search with no matching results."""
        # Arrange
        filters = InventoryItemFilter()
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
    async def test_update_inventory_item_by_id_success(self, service_with_mock_repo, mock_repository, updated_inventory_item_model):
        """Test successful inventory_item update."""
        # Arrange
        mock_repository.update_by_id.return_value = updated_inventory_item_model
        
        # Act
        result = await service_with_mock_repo.update_by_id(1, InventoryItemUpdate())
        
        # Assert
        assert isinstance(result, InventoryItemResponse)
        mock_repository.update_by_id.assert_called_once_with(1, InventoryItemUpdate().model_dump(exclude_unset=True))

    # # ─── Delete operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_delete_by_id_success(self, service_with_mock_repo, mock_repository):
        """Test successful inventory_item deletion."""
        # Arrange
        mock_repository.delete_by_id.return_value = True
        
        # Act
        result = await service_with_mock_repo.delete_by_id(1)
        
        # Assert
        assert result is True
        mock_repository.delete_by_id.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_delete_by_id_not_found(self, service_with_mock_repo, mock_repository):
        """Test deletion of non-existent inventory_item."""
        # Arrange
        mock_repository.delete_by_id.return_value = False
        
        # Act
        result = await service_with_mock_repo.delete_by_id(999)
        
        # Assert
        assert result is False
        mock_repository.delete_by_id.assert_called_once_with(999)
