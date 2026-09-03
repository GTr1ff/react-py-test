# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c


"""
Unit tests for the UserPreferenceService layer.
"""

from pydantic import ValidationError
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from decimal import Decimal
from sqlalchemy.exc import SQLAlchemyError

from core.pagination import PaginatedResponse
from features.tables.user_preference.models import UserPreferenceModel
from features.tables.user_preference.schemas import UserPreferenceResponse, UserPreferenceCreate, UserPreferenceUpdate, UserPreferenceFilter
from features.tables.user_preference.service import UserPreferenceService
from features.tables.user_preference.repository import UserPreferenceRepository

class TestUserPreferenceService:
    """Test cases for UserPreferenceService layer."""


    @pytest.fixture
    def mock_repository(self):
        """Create a mock UserPreferenceRepository."""
        return AsyncMock(spec=UserPreferenceRepository)

    @pytest.fixture
    def service_with_mock_repo(self, mock_session_async, mock_repository):
        """Create UserPreferenceService with mocked repository."""
        service = UserPreferenceService(mock_session_async)
        service.repo = mock_repository
        return service

    # ─── Create operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_create_user_preference_success(self, service_with_mock_repo, mock_repository, sample_data, existing_user_preference):
        """Test successful user_preference creation through service."""
        # Arrange
        new_item = UserPreferenceCreate(**sample_data)
        mock_repository.create.return_value = existing_user_preference
        
        # Act
        result = await service_with_mock_repo.create(new_item)
        
        # Assert
        assert isinstance(result, UserPreferenceResponse)
        mock_repository.create.assert_called_once()

    # # ─── Read operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_get_user_preference_by_id_success(self, service_with_mock_repo, mock_repository, existing_user_preference):
        """Test successful retrieval of user_preference by ID."""
        # Arrange
        mock_repository.get_by_id.return_value = existing_user_preference
        
        # Act
        result = await service_with_mock_repo.get_by_id(1)
        
        # Assert
        assert isinstance(result, UserPreferenceResponse)
        mock_repository.get_by_id.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_get_user_preference_by_id_not_found(self, service_with_mock_repo, mock_repository):
        """Test retrieval of non-existent user_preference."""
        # Arrange
        mock_repository.get_by_id.return_value = None
        
        # Act
        result = await service_with_mock_repo.get_by_id(999)
        
        # Assert
        assert result is None
        mock_repository.get_by_id.assert_called_once_with(999)

    @pytest.mark.asyncio
    async def test_get_all_success(self, service_with_mock_repo, mock_repository, multiple_user_preference, pagination_request):
        """Test successful retrieval of all user_preference."""
        # Arrange
        mock_repository.get_all.return_value = (multiple_user_preference, len(multiple_user_preference))
        
        # Act
        result = await service_with_mock_repo.get_all(pagination_request)
        
        # Assert
        assert isinstance(result, PaginatedResponse)
        assert len(result.items) == len(multiple_user_preference)
        assert result.total == len(multiple_user_preference)
        mock_repository.get_all.assert_called_once_with(pagination_request)

    

    @pytest.mark.asyncio
    async def test_search_success(self, service_with_mock_repo, mock_repository, multiple_user_preference, pagination_request):
        """Test successful search with filters."""
        # Arrange
        filters = UserPreferenceFilter()
        mock_repository.search.return_value = (multiple_user_preference, len(multiple_user_preference))
        
        # Act
        result = await service_with_mock_repo.search(filters, pagination_request)
        
        # Assert
        assert isinstance(result, PaginatedResponse)
        assert len(result.items) == len(multiple_user_preference)
        assert result.total == len(multiple_user_preference)
        
        # Verify repository was called with correct filter dict
        mock_repository.search.assert_called_once_with(filters, pagination_request)

    @pytest.mark.asyncio
    async def test_search_empty_results(self, service_with_mock_repo, mock_repository, pagination_request):
        """Test search with no matching results."""
        # Arrange
        filters = UserPreferenceFilter()
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
    async def test_update_user_preference_by_id_success(self, service_with_mock_repo, mock_repository, updated_user_preference_model):
        """Test successful user_preference update."""
        # Arrange
        mock_repository.update_by_id.return_value = updated_user_preference_model
        
        # Act
        result = await service_with_mock_repo.update_by_id(1, UserPreferenceUpdate())
        
        # Assert
        assert isinstance(result, UserPreferenceResponse)
        mock_repository.update_by_id.assert_called_once_with(1, UserPreferenceUpdate().model_dump(exclude_unset=True))

    # # ─── Delete operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_delete_by_id_success(self, service_with_mock_repo, mock_repository):
        """Test successful user_preference deletion."""
        # Arrange
        mock_repository.delete_by_id.return_value = True
        
        # Act
        result = await service_with_mock_repo.delete_by_id(1)
        
        # Assert
        assert result is True
        mock_repository.delete_by_id.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_delete_by_id_not_found(self, service_with_mock_repo, mock_repository):
        """Test deletion of non-existent user_preference."""
        # Arrange
        mock_repository.delete_by_id.return_value = False
        
        # Act
        result = await service_with_mock_repo.delete_by_id(999)
        
        # Assert
        assert result is False
        mock_repository.delete_by_id.assert_called_once_with(999)
