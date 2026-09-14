# ROSETIC:crud-guid


"""
Unit tests for the BenefitService layer.
"""

from pydantic import ValidationError
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from decimal import Decimal
from sqlalchemy.exc import SQLAlchemyError

from core.pagination import PaginatedResponse
from features.tables.benefits.models import BenefitModel
from features.tables.benefits.schemas import BenefitResponse, BenefitCreate, BenefitUpdate, BenefitFilter
from features.tables.benefits.service import BenefitService
from features.tables.benefits.repository import BenefitRepository

class TestBenefitService:
    """Test cases for BenefitService layer."""


    @pytest.fixture
    def mock_repository(self):
        """Create a mock BenefitRepository."""
        return AsyncMock(spec=BenefitRepository)

    @pytest.fixture
    def service_with_mock_repo(self, mock_session_async, mock_repository):
        """Create BenefitService with mocked repository."""
        service = BenefitService(mock_session_async)
        service.repo = mock_repository
        return service

    # ─── Create operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_create_benefit_success(self, service_with_mock_repo, mock_repository, sample_data, existing_benefit):
        """Test successful benefits creation through service."""
        # Arrange
        new_item = BenefitCreate(**sample_data)
        mock_repository.create.return_value = existing_benefit
        
        # Act
        result = await service_with_mock_repo.create(new_item)
        
        # Assert
        assert isinstance(result, BenefitResponse)
        mock_repository.create.assert_called_once()

    # # ─── Read operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_get_benefit_by_id_success(self, service_with_mock_repo, mock_repository, existing_benefit):
        """Test successful retrieval of benefit by ID."""
        # Arrange
        mock_repository.get_by_id.return_value = existing_benefit
        
        # Act
        result = await service_with_mock_repo.get_by_id(1)
        
        # Assert
        assert isinstance(result, BenefitResponse)
        mock_repository.get_by_id.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_get_benefit_by_id_not_found(self, service_with_mock_repo, mock_repository):
        """Test retrieval of non-existent benefit."""
        # Arrange
        mock_repository.get_by_id.return_value = None
        
        # Act
        result = await service_with_mock_repo.get_by_id(999)
        
        # Assert
        assert result is None
        mock_repository.get_by_id.assert_called_once_with(999)

    @pytest.mark.asyncio
    async def test_get_all_success(self, service_with_mock_repo, mock_repository, multiple_benefits, pagination_request):
        """Test successful retrieval of all benefits."""
        # Arrange
        mock_repository.get_all.return_value = (multiple_benefits, len(multiple_benefits))
        
        # Act
        result = await service_with_mock_repo.get_all(pagination_request)
        
        # Assert
        assert isinstance(result, PaginatedResponse)
        assert len(result.items) == len(multiple_benefits)
        assert result.total == len(multiple_benefits)
        mock_repository.get_all.assert_called_once_with(pagination_request)

    

    @pytest.mark.asyncio
    async def test_search_success(self, service_with_mock_repo, mock_repository, multiple_benefits, pagination_request):
        """Test successful search with filters."""
        # Arrange
        filters = BenefitFilter()
        mock_repository.search.return_value = (multiple_benefits, len(multiple_benefits))
        
        # Act
        result = await service_with_mock_repo.search(filters, pagination_request)
        
        # Assert
        assert isinstance(result, PaginatedResponse)
        assert len(result.items) == len(multiple_benefits)
        assert result.total == len(multiple_benefits)
        
        # Verify repository was called with correct filter dict
        mock_repository.search.assert_called_once_with(filters, pagination_request)

    @pytest.mark.asyncio
    async def test_search_empty_results(self, service_with_mock_repo, mock_repository, pagination_request):
        """Test search with no matching results."""
        # Arrange
        filters = BenefitFilter()
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
    async def test_update_benefit_by_id_success(self, service_with_mock_repo, mock_repository, updated_benefit_model):
        """Test successful benefit update."""
        # Arrange
        mock_repository.update_by_id.return_value = updated_benefit_model
        
        # Act
        result = await service_with_mock_repo.update_by_id(1, BenefitUpdate())
        
        # Assert
        assert isinstance(result, BenefitResponse)
        mock_repository.update_by_id.assert_called_once_with(1, BenefitUpdate().model_dump(exclude_unset=True))

    # # ─── Delete operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_delete_by_id_success(self, service_with_mock_repo, mock_repository):
        """Test successful benefit deletion."""
        # Arrange
        mock_repository.delete_by_id.return_value = True
        
        # Act
        result = await service_with_mock_repo.delete_by_id(1)
        
        # Assert
        assert result is True
        mock_repository.delete_by_id.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_delete_by_id_not_found(self, service_with_mock_repo, mock_repository):
        """Test deletion of non-existent benefit."""
        # Arrange
        mock_repository.delete_by_id.return_value = False
        
        # Act
        result = await service_with_mock_repo.delete_by_id(999)
        
        # Assert
        assert result is False
        mock_repository.delete_by_id.assert_called_once_with(999)
