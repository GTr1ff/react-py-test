# ROSETIC:crud-guid


"""
Unit tests for the SettingService layer.
"""

from pydantic import ValidationError
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from decimal import Decimal
from sqlalchemy.exc import SQLAlchemyError

from core.pagination import PaginatedResponse
from features.tables.settings.models import SettingModel
from features.tables.settings.schemas import SettingResponse, SettingCreate, SettingUpdate, SettingFilter
from features.tables.settings.service import SettingService
from features.tables.settings.repository import SettingRepository

class TestSettingService:
    """Test cases for SettingService layer."""


    @pytest.fixture
    def mock_repository(self):
        """Create a mock SettingRepository."""
        return AsyncMock(spec=SettingRepository)

    @pytest.fixture
    def service_with_mock_repo(self, mock_session_async, mock_repository):
        """Create SettingService with mocked repository."""
        service = SettingService(mock_session_async)
        service.repo = mock_repository
        return service

    # ─── Create operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_create_setting_success(self, service_with_mock_repo, mock_repository, sample_data, existing_setting):
        """Test successful settings creation through service."""
        # Arrange
        new_item = SettingCreate(**sample_data)
        mock_repository.create.return_value = existing_setting
        
        # Act
        result = await service_with_mock_repo.create(new_item)
        
        # Assert
        assert isinstance(result, SettingResponse)
        mock_repository.create.assert_called_once()

    # # ─── Read operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_get_setting_by_id_success(self, service_with_mock_repo, mock_repository, existing_setting):
        """Test successful retrieval of setting by ID."""
        # Arrange
        mock_repository.get_by_id.return_value = existing_setting
        
        # Act
        result = await service_with_mock_repo.get_by_id(1)
        
        # Assert
        assert isinstance(result, SettingResponse)
        mock_repository.get_by_id.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_get_setting_by_id_not_found(self, service_with_mock_repo, mock_repository):
        """Test retrieval of non-existent setting."""
        # Arrange
        mock_repository.get_by_id.return_value = None
        
        # Act
        result = await service_with_mock_repo.get_by_id(999)
        
        # Assert
        assert result is None
        mock_repository.get_by_id.assert_called_once_with(999)

    @pytest.mark.asyncio
    async def test_get_all_success(self, service_with_mock_repo, mock_repository, multiple_settings, pagination_request):
        """Test successful retrieval of all settings."""
        # Arrange
        mock_repository.get_all.return_value = (multiple_settings, len(multiple_settings))
        
        # Act
        result = await service_with_mock_repo.get_all(pagination_request)
        
        # Assert
        assert isinstance(result, PaginatedResponse)
        assert len(result.items) == len(multiple_settings)
        assert result.total == len(multiple_settings)
        mock_repository.get_all.assert_called_once_with(pagination_request)

    

    @pytest.mark.asyncio
    async def test_search_success(self, service_with_mock_repo, mock_repository, multiple_settings, pagination_request):
        """Test successful search with filters."""
        # Arrange
        filters = SettingFilter()
        mock_repository.search.return_value = (multiple_settings, len(multiple_settings))
        
        # Act
        result = await service_with_mock_repo.search(filters, pagination_request)
        
        # Assert
        assert isinstance(result, PaginatedResponse)
        assert len(result.items) == len(multiple_settings)
        assert result.total == len(multiple_settings)
        
        # Verify repository was called with correct filter dict
        mock_repository.search.assert_called_once_with(filters, pagination_request)

    @pytest.mark.asyncio
    async def test_search_empty_results(self, service_with_mock_repo, mock_repository, pagination_request):
        """Test search with no matching results."""
        # Arrange
        filters = SettingFilter()
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
    async def test_update_setting_by_id_success(self, service_with_mock_repo, mock_repository, updated_setting_model):
        """Test successful setting update."""
        # Arrange
        mock_repository.update_by_id.return_value = updated_setting_model
        
        # Act
        result = await service_with_mock_repo.update_by_id(1, SettingUpdate())
        
        # Assert
        assert isinstance(result, SettingResponse)
        mock_repository.update_by_id.assert_called_once_with(1, SettingUpdate().model_dump(exclude_unset=True))

    # # ─── Delete operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_delete_by_id_success(self, service_with_mock_repo, mock_repository):
        """Test successful setting deletion."""
        # Arrange
        mock_repository.delete_by_id.return_value = True
        
        # Act
        result = await service_with_mock_repo.delete_by_id(1)
        
        # Assert
        assert result is True
        mock_repository.delete_by_id.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_delete_by_id_not_found(self, service_with_mock_repo, mock_repository):
        """Test deletion of non-existent setting."""
        # Arrange
        mock_repository.delete_by_id.return_value = False
        
        # Act
        result = await service_with_mock_repo.delete_by_id(999)
        
        # Assert
        assert result is False
        mock_repository.delete_by_id.assert_called_once_with(999)
