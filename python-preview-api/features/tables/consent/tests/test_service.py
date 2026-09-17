# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c


"""
Unit tests for the ConsentService layer.
"""

from pydantic import ValidationError
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from decimal import Decimal
from sqlalchemy.exc import SQLAlchemyError

from core.pagination import PaginatedResponse
from features.tables.consent.models import ConsentModel
from features.tables.consent.schemas import ConsentResponse, ConsentCreate, ConsentUpdate, ConsentFilter
from features.tables.consent.service import ConsentService
from features.tables.consent.repository import ConsentRepository

class TestConsentService:
    """Test cases for ConsentService layer."""


    @pytest.fixture
    def mock_repository(self):
        """Create a mock ConsentRepository."""
        return AsyncMock(spec=ConsentRepository)

    @pytest.fixture
    def service_with_mock_repo(self, mock_session_async, mock_repository):
        """Create ConsentService with mocked repository."""
        service = ConsentService(mock_session_async)
        service.repo = mock_repository
        return service

    # ─── Create operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_create_consent_success(self, service_with_mock_repo, mock_repository, sample_data, existing_consent):
        """Test successful consent creation through service."""
        # Arrange
        new_item = ConsentCreate(**sample_data)
        mock_repository.create.return_value = existing_consent
        
        # Act
        result = await service_with_mock_repo.create(new_item)
        
        # Assert
        assert isinstance(result, ConsentResponse)
        mock_repository.create.assert_called_once()

    # # ─── Read operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_get_consent_by_id_success(self, service_with_mock_repo, mock_repository, existing_consent):
        """Test successful retrieval of consent by ID."""
        # Arrange
        mock_repository.get_by_id.return_value = existing_consent
        
        # Act
        result = await service_with_mock_repo.get_by_id(1)
        
        # Assert
        assert isinstance(result, ConsentResponse)
        mock_repository.get_by_id.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_get_consent_by_id_not_found(self, service_with_mock_repo, mock_repository):
        """Test retrieval of non-existent consent."""
        # Arrange
        mock_repository.get_by_id.return_value = None
        
        # Act
        result = await service_with_mock_repo.get_by_id(999)
        
        # Assert
        assert result is None
        mock_repository.get_by_id.assert_called_once_with(999)

    @pytest.mark.asyncio
    async def test_get_all_success(self, service_with_mock_repo, mock_repository, multiple_consent, pagination_request):
        """Test successful retrieval of all consent."""
        # Arrange
        mock_repository.get_all.return_value = (multiple_consent, len(multiple_consent))
        
        # Act
        result = await service_with_mock_repo.get_all(pagination_request)
        
        # Assert
        assert isinstance(result, PaginatedResponse)
        assert len(result.items) == len(multiple_consent)
        assert result.total == len(multiple_consent)
        mock_repository.get_all.assert_called_once_with(pagination_request)

    

    @pytest.mark.asyncio
    async def test_search_success(self, service_with_mock_repo, mock_repository, multiple_consent, pagination_request):
        """Test successful search with filters."""
        # Arrange
        filters = ConsentFilter()
        mock_repository.search.return_value = (multiple_consent, len(multiple_consent))
        
        # Act
        result = await service_with_mock_repo.search(filters, pagination_request)
        
        # Assert
        assert isinstance(result, PaginatedResponse)
        assert len(result.items) == len(multiple_consent)
        assert result.total == len(multiple_consent)
        
        # Verify repository was called with correct filter dict
        mock_repository.search.assert_called_once_with(filters, pagination_request)

    @pytest.mark.asyncio
    async def test_search_empty_results(self, service_with_mock_repo, mock_repository, pagination_request):
        """Test search with no matching results."""
        # Arrange
        filters = ConsentFilter()
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
    async def test_update_consent_by_id_success(self, service_with_mock_repo, mock_repository, updated_consent_model):
        """Test successful consent update."""
        # Arrange
        mock_repository.update_by_id.return_value = updated_consent_model
        
        # Act
        result = await service_with_mock_repo.update_by_id(1, ConsentUpdate())
        
        # Assert
        assert isinstance(result, ConsentResponse)
        mock_repository.update_by_id.assert_called_once_with(1, ConsentUpdate().model_dump(exclude_unset=True))

    # # ─── Delete operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_delete_by_id_success(self, service_with_mock_repo, mock_repository):
        """Test successful consent deletion."""
        # Arrange
        mock_repository.delete_by_id.return_value = True
        
        # Act
        result = await service_with_mock_repo.delete_by_id(1)
        
        # Assert
        assert result is True
        mock_repository.delete_by_id.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_delete_by_id_not_found(self, service_with_mock_repo, mock_repository):
        """Test deletion of non-existent consent."""
        # Arrange
        mock_repository.delete_by_id.return_value = False
        
        # Act
        result = await service_with_mock_repo.delete_by_id(999)
        
        # Assert
        assert result is False
        mock_repository.delete_by_id.assert_called_once_with(999)
