# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c


"""
Unit tests for the AuditLogService layer.
"""

from pydantic import ValidationError
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from decimal import Decimal
from sqlalchemy.exc import SQLAlchemyError

from core.pagination import PaginatedResponse
from features.tables.audit_log.models import AuditLogModel
from features.tables.audit_log.schemas import AuditLogResponse, AuditLogCreate, AuditLogUpdate, AuditLogFilter
from features.tables.audit_log.service import AuditLogService
from features.tables.audit_log.repository import AuditLogRepository

class TestAuditLogService:
    """Test cases for AuditLogService layer."""


    @pytest.fixture
    def mock_repository(self):
        """Create a mock AuditLogRepository."""
        return AsyncMock(spec=AuditLogRepository)

    @pytest.fixture
    def service_with_mock_repo(self, mock_session_async, mock_repository):
        """Create AuditLogService with mocked repository."""
        service = AuditLogService(mock_session_async)
        service.repo = mock_repository
        return service

    # ─── Create operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_create_audit_log_success(self, service_with_mock_repo, mock_repository, sample_data, existing_audit_log):
        """Test successful audit_log creation through service."""
        # Arrange
        new_item = AuditLogCreate(**sample_data)
        mock_repository.create.return_value = existing_audit_log
        
        # Act
        result = await service_with_mock_repo.create(new_item)
        
        # Assert
        assert isinstance(result, AuditLogResponse)
        mock_repository.create.assert_called_once()

    # # ─── Read operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_get_audit_log_by_id_success(self, service_with_mock_repo, mock_repository, existing_audit_log):
        """Test successful retrieval of audit_log by ID."""
        # Arrange
        mock_repository.get_by_id.return_value = existing_audit_log
        
        # Act
        result = await service_with_mock_repo.get_by_id(1)
        
        # Assert
        assert isinstance(result, AuditLogResponse)
        mock_repository.get_by_id.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_get_audit_log_by_id_not_found(self, service_with_mock_repo, mock_repository):
        """Test retrieval of non-existent audit_log."""
        # Arrange
        mock_repository.get_by_id.return_value = None
        
        # Act
        result = await service_with_mock_repo.get_by_id(999)
        
        # Assert
        assert result is None
        mock_repository.get_by_id.assert_called_once_with(999)

    @pytest.mark.asyncio
    async def test_get_all_success(self, service_with_mock_repo, mock_repository, multiple_audit_log, pagination_request):
        """Test successful retrieval of all audit_log."""
        # Arrange
        mock_repository.get_all.return_value = (multiple_audit_log, len(multiple_audit_log))
        
        # Act
        result = await service_with_mock_repo.get_all(pagination_request)
        
        # Assert
        assert isinstance(result, PaginatedResponse)
        assert len(result.items) == len(multiple_audit_log)
        assert result.total == len(multiple_audit_log)
        mock_repository.get_all.assert_called_once_with(pagination_request)

    

    @pytest.mark.asyncio
    async def test_search_success(self, service_with_mock_repo, mock_repository, multiple_audit_log, pagination_request):
        """Test successful search with filters."""
        # Arrange
        filters = AuditLogFilter()
        mock_repository.search.return_value = (multiple_audit_log, len(multiple_audit_log))
        
        # Act
        result = await service_with_mock_repo.search(filters, pagination_request)
        
        # Assert
        assert isinstance(result, PaginatedResponse)
        assert len(result.items) == len(multiple_audit_log)
        assert result.total == len(multiple_audit_log)
        
        # Verify repository was called with correct filter dict
        mock_repository.search.assert_called_once_with(filters, pagination_request)

    @pytest.mark.asyncio
    async def test_search_empty_results(self, service_with_mock_repo, mock_repository, pagination_request):
        """Test search with no matching results."""
        # Arrange
        filters = AuditLogFilter()
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
    async def test_update_audit_log_by_id_success(self, service_with_mock_repo, mock_repository, updated_audit_log_model):
        """Test successful audit_log update."""
        # Arrange
        mock_repository.update_by_id.return_value = updated_audit_log_model
        
        # Act
        result = await service_with_mock_repo.update_by_id(1, AuditLogUpdate())
        
        # Assert
        assert isinstance(result, AuditLogResponse)
        mock_repository.update_by_id.assert_called_once_with(1, AuditLogUpdate().model_dump(exclude_unset=True))

    # # ─── Delete operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_delete_by_id_success(self, service_with_mock_repo, mock_repository):
        """Test successful audit_log deletion."""
        # Arrange
        mock_repository.delete_by_id.return_value = True
        
        # Act
        result = await service_with_mock_repo.delete_by_id(1)
        
        # Assert
        assert result is True
        mock_repository.delete_by_id.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_delete_by_id_not_found(self, service_with_mock_repo, mock_repository):
        """Test deletion of non-existent audit_log."""
        # Arrange
        mock_repository.delete_by_id.return_value = False
        
        # Act
        result = await service_with_mock_repo.delete_by_id(999)
        
        # Assert
        assert result is False
        mock_repository.delete_by_id.assert_called_once_with(999)
