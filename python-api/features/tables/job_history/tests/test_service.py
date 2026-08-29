# ROSETIC:crud-guid


"""
Unit tests for the JobHistoryService layer.
"""

from pydantic import ValidationError
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from decimal import Decimal
from sqlalchemy.exc import SQLAlchemyError

from core.pagination import PaginatedResponse
from features.tables.job_history.models import JobHistoryModel
from features.tables.job_history.schemas import JobHistoryResponse, JobHistoryCreate, JobHistoryUpdate, JobHistoryFilter
from features.tables.job_history.service import JobHistoryService
from features.tables.job_history.repository import JobHistoryRepository

class TestJobHistoryService:
    """Test cases for JobHistoryService layer."""


    @pytest.fixture
    def mock_repository(self):
        """Create a mock JobHistoryRepository."""
        return AsyncMock(spec=JobHistoryRepository)

    @pytest.fixture
    def service_with_mock_repo(self, mock_session_async, mock_repository):
        """Create JobHistoryService with mocked repository."""
        service = JobHistoryService(mock_session_async)
        service.repo = mock_repository
        return service

    # ─── Create operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_create_job_history_success(self, service_with_mock_repo, mock_repository, sample_data, existing_job_history):
        """Test successful job_history creation through service."""
        # Arrange
        new_item = JobHistoryCreate(**sample_data)
        mock_repository.create.return_value = existing_job_history
        
        # Act
        result = await service_with_mock_repo.create(new_item)
        
        # Assert
        assert isinstance(result, JobHistoryResponse)
        mock_repository.create.assert_called_once()

    # # ─── Read operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_get_job_history_by_id_success(self, service_with_mock_repo, mock_repository, existing_job_history):
        """Test successful retrieval of job_history by ID."""
        # Arrange
        mock_repository.get_by_id.return_value = existing_job_history
        
        # Act
        result = await service_with_mock_repo.get_by_id(1)
        
        # Assert
        assert isinstance(result, JobHistoryResponse)
        mock_repository.get_by_id.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_get_job_history_by_id_not_found(self, service_with_mock_repo, mock_repository):
        """Test retrieval of non-existent job_history."""
        # Arrange
        mock_repository.get_by_id.return_value = None
        
        # Act
        result = await service_with_mock_repo.get_by_id(999)
        
        # Assert
        assert result is None
        mock_repository.get_by_id.assert_called_once_with(999)

    @pytest.mark.asyncio
    async def test_get_all_success(self, service_with_mock_repo, mock_repository, multiple_job_history, pagination_request):
        """Test successful retrieval of all job_history."""
        # Arrange
        mock_repository.get_all.return_value = (multiple_job_history, len(multiple_job_history))
        
        # Act
        result = await service_with_mock_repo.get_all(pagination_request)
        
        # Assert
        assert isinstance(result, PaginatedResponse)
        assert len(result.items) == len(multiple_job_history)
        assert result.total == len(multiple_job_history)
        mock_repository.get_all.assert_called_once_with(pagination_request)

    

    @pytest.mark.asyncio
    async def test_search_success(self, service_with_mock_repo, mock_repository, multiple_job_history, pagination_request):
        """Test successful search with filters."""
        # Arrange
        filters = JobHistoryFilter()
        mock_repository.search.return_value = (multiple_job_history, len(multiple_job_history))
        
        # Act
        result = await service_with_mock_repo.search(filters, pagination_request)
        
        # Assert
        assert isinstance(result, PaginatedResponse)
        assert len(result.items) == len(multiple_job_history)
        assert result.total == len(multiple_job_history)
        
        # Verify repository was called with correct filter dict
        mock_repository.search.assert_called_once_with(filters, pagination_request)

    @pytest.mark.asyncio
    async def test_search_empty_results(self, service_with_mock_repo, mock_repository, pagination_request):
        """Test search with no matching results."""
        # Arrange
        filters = JobHistoryFilter()
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
    async def test_update_job_history_by_id_success(self, service_with_mock_repo, mock_repository, updated_job_history_model):
        """Test successful job_history update."""
        # Arrange
        mock_repository.update_by_id.return_value = updated_job_history_model
        
        # Act
        result = await service_with_mock_repo.update_by_id(1, JobHistoryUpdate())
        
        # Assert
        assert isinstance(result, JobHistoryResponse)
        mock_repository.update_by_id.assert_called_once_with(1, JobHistoryUpdate().model_dump(exclude_unset=True))

    # # ─── Delete operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_delete_by_id_success(self, service_with_mock_repo, mock_repository):
        """Test successful job_history deletion."""
        # Arrange
        mock_repository.delete_by_id.return_value = True
        
        # Act
        result = await service_with_mock_repo.delete_by_id(1)
        
        # Assert
        assert result is True
        mock_repository.delete_by_id.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_delete_by_id_not_found(self, service_with_mock_repo, mock_repository):
        """Test deletion of non-existent job_history."""
        # Arrange
        mock_repository.delete_by_id.return_value = False
        
        # Act
        result = await service_with_mock_repo.delete_by_id(999)
        
        # Assert
        assert result is False
        mock_repository.delete_by_id.assert_called_once_with(999)
