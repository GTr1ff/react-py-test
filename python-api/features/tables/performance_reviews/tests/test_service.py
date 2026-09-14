# ROSETIC:crud-guid


"""
Unit tests for the PerformanceReviewService layer.
"""

from pydantic import ValidationError
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from decimal import Decimal
from sqlalchemy.exc import SQLAlchemyError

from core.pagination import PaginatedResponse
from features.tables.performance_reviews.models import PerformanceReviewModel
from features.tables.performance_reviews.schemas import PerformanceReviewResponse, PerformanceReviewCreate, PerformanceReviewUpdate, PerformanceReviewFilter
from features.tables.performance_reviews.service import PerformanceReviewService
from features.tables.performance_reviews.repository import PerformanceReviewRepository

class TestPerformanceReviewService:
    """Test cases for PerformanceReviewService layer."""


    @pytest.fixture
    def mock_repository(self):
        """Create a mock PerformanceReviewRepository."""
        return AsyncMock(spec=PerformanceReviewRepository)

    @pytest.fixture
    def service_with_mock_repo(self, mock_session_async, mock_repository):
        """Create PerformanceReviewService with mocked repository."""
        service = PerformanceReviewService(mock_session_async)
        service.repo = mock_repository
        return service

    # ─── Create operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_create_performance_review_success(self, service_with_mock_repo, mock_repository, sample_data, existing_performance_review):
        """Test successful performance_reviews creation through service."""
        # Arrange
        new_item = PerformanceReviewCreate(**sample_data)
        mock_repository.create.return_value = existing_performance_review
        
        # Act
        result = await service_with_mock_repo.create(new_item)
        
        # Assert
        assert isinstance(result, PerformanceReviewResponse)
        mock_repository.create.assert_called_once()

    # # ─── Read operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_get_performance_review_by_id_success(self, service_with_mock_repo, mock_repository, existing_performance_review):
        """Test successful retrieval of performance_review by ID."""
        # Arrange
        mock_repository.get_by_id.return_value = existing_performance_review
        
        # Act
        result = await service_with_mock_repo.get_by_id(1)
        
        # Assert
        assert isinstance(result, PerformanceReviewResponse)
        mock_repository.get_by_id.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_get_performance_review_by_id_not_found(self, service_with_mock_repo, mock_repository):
        """Test retrieval of non-existent performance_review."""
        # Arrange
        mock_repository.get_by_id.return_value = None
        
        # Act
        result = await service_with_mock_repo.get_by_id(999)
        
        # Assert
        assert result is None
        mock_repository.get_by_id.assert_called_once_with(999)

    @pytest.mark.asyncio
    async def test_get_all_success(self, service_with_mock_repo, mock_repository, multiple_performance_reviews, pagination_request):
        """Test successful retrieval of all performance_reviews."""
        # Arrange
        mock_repository.get_all.return_value = (multiple_performance_reviews, len(multiple_performance_reviews))
        
        # Act
        result = await service_with_mock_repo.get_all(pagination_request)
        
        # Assert
        assert isinstance(result, PaginatedResponse)
        assert len(result.items) == len(multiple_performance_reviews)
        assert result.total == len(multiple_performance_reviews)
        mock_repository.get_all.assert_called_once_with(pagination_request)

    

    @pytest.mark.asyncio
    async def test_search_success(self, service_with_mock_repo, mock_repository, multiple_performance_reviews, pagination_request):
        """Test successful search with filters."""
        # Arrange
        filters = PerformanceReviewFilter()
        mock_repository.search.return_value = (multiple_performance_reviews, len(multiple_performance_reviews))
        
        # Act
        result = await service_with_mock_repo.search(filters, pagination_request)
        
        # Assert
        assert isinstance(result, PaginatedResponse)
        assert len(result.items) == len(multiple_performance_reviews)
        assert result.total == len(multiple_performance_reviews)
        
        # Verify repository was called with correct filter dict
        mock_repository.search.assert_called_once_with(filters, pagination_request)

    @pytest.mark.asyncio
    async def test_search_empty_results(self, service_with_mock_repo, mock_repository, pagination_request):
        """Test search with no matching results."""
        # Arrange
        filters = PerformanceReviewFilter()
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
    async def test_update_performance_review_by_id_success(self, service_with_mock_repo, mock_repository, updated_performance_review_model):
        """Test successful performance_review update."""
        # Arrange
        mock_repository.update_by_id.return_value = updated_performance_review_model
        
        # Act
        result = await service_with_mock_repo.update_by_id(1, PerformanceReviewUpdate())
        
        # Assert
        assert isinstance(result, PerformanceReviewResponse)
        mock_repository.update_by_id.assert_called_once_with(1, PerformanceReviewUpdate().model_dump(exclude_unset=True))

    # # ─── Delete operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_delete_by_id_success(self, service_with_mock_repo, mock_repository):
        """Test successful performance_review deletion."""
        # Arrange
        mock_repository.delete_by_id.return_value = True
        
        # Act
        result = await service_with_mock_repo.delete_by_id(1)
        
        # Assert
        assert result is True
        mock_repository.delete_by_id.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_delete_by_id_not_found(self, service_with_mock_repo, mock_repository):
        """Test deletion of non-existent performance_review."""
        # Arrange
        mock_repository.delete_by_id.return_value = False
        
        # Act
        result = await service_with_mock_repo.delete_by_id(999)
        
        # Assert
        assert result is False
        mock_repository.delete_by_id.assert_called_once_with(999)
