# ROSETIC:crud-guid


"""
Unit tests for the DepartmentService layer.
"""

from pydantic import ValidationError
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from decimal import Decimal
from sqlalchemy.exc import SQLAlchemyError

from core.pagination import PaginatedResponse
from features.tables.departments.models import DepartmentModel
from features.tables.departments.schemas import DepartmentResponse, DepartmentCreate, DepartmentUpdate, DepartmentFilter
from features.tables.departments.service import DepartmentService
from features.tables.departments.repository import DepartmentRepository

class TestDepartmentService:
    """Test cases for DepartmentService layer."""


    @pytest.fixture
    def mock_repository(self):
        """Create a mock DepartmentRepository."""
        return AsyncMock(spec=DepartmentRepository)

    @pytest.fixture
    def service_with_mock_repo(self, mock_session_async, mock_repository):
        """Create DepartmentService with mocked repository."""
        service = DepartmentService(mock_session_async)
        service.repo = mock_repository
        return service

    # ─── Create operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_create_department_success(self, service_with_mock_repo, mock_repository, sample_data, existing_department):
        """Test successful departments creation through service."""
        # Arrange
        new_item = DepartmentCreate(**sample_data)
        mock_repository.create.return_value = existing_department
        
        # Act
        result = await service_with_mock_repo.create(new_item)
        
        # Assert
        assert isinstance(result, DepartmentResponse)
        mock_repository.create.assert_called_once()

    # # ─── Read operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_get_department_by_id_success(self, service_with_mock_repo, mock_repository, existing_department):
        """Test successful retrieval of department by ID."""
        # Arrange
        mock_repository.get_by_id.return_value = existing_department
        
        # Act
        result = await service_with_mock_repo.get_by_id(1)
        
        # Assert
        assert isinstance(result, DepartmentResponse)
        mock_repository.get_by_id.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_get_department_by_id_not_found(self, service_with_mock_repo, mock_repository):
        """Test retrieval of non-existent department."""
        # Arrange
        mock_repository.get_by_id.return_value = None
        
        # Act
        result = await service_with_mock_repo.get_by_id(999)
        
        # Assert
        assert result is None
        mock_repository.get_by_id.assert_called_once_with(999)

    @pytest.mark.asyncio
    async def test_get_all_success(self, service_with_mock_repo, mock_repository, multiple_departments, pagination_request):
        """Test successful retrieval of all departments."""
        # Arrange
        mock_repository.get_all.return_value = (multiple_departments, len(multiple_departments))
        
        # Act
        result = await service_with_mock_repo.get_all(pagination_request)
        
        # Assert
        assert isinstance(result, PaginatedResponse)
        assert len(result.items) == len(multiple_departments)
        assert result.total == len(multiple_departments)
        mock_repository.get_all.assert_called_once_with(pagination_request)

    

    @pytest.mark.asyncio
    async def test_search_success(self, service_with_mock_repo, mock_repository, multiple_departments, pagination_request):
        """Test successful search with filters."""
        # Arrange
        filters = DepartmentFilter()
        mock_repository.search.return_value = (multiple_departments, len(multiple_departments))
        
        # Act
        result = await service_with_mock_repo.search(filters, pagination_request)
        
        # Assert
        assert isinstance(result, PaginatedResponse)
        assert len(result.items) == len(multiple_departments)
        assert result.total == len(multiple_departments)
        
        # Verify repository was called with correct filter dict
        mock_repository.search.assert_called_once_with(filters, pagination_request)

    @pytest.mark.asyncio
    async def test_search_empty_results(self, service_with_mock_repo, mock_repository, pagination_request):
        """Test search with no matching results."""
        # Arrange
        filters = DepartmentFilter()
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
    async def test_update_department_by_id_success(self, service_with_mock_repo, mock_repository, updated_department_model):
        """Test successful department update."""
        # Arrange
        mock_repository.update_by_id.return_value = updated_department_model
        
        # Act
        result = await service_with_mock_repo.update_by_id(1, DepartmentUpdate())
        
        # Assert
        assert isinstance(result, DepartmentResponse)
        mock_repository.update_by_id.assert_called_once_with(1, DepartmentUpdate().model_dump(exclude_unset=True))

    # # ─── Delete operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_delete_by_id_success(self, service_with_mock_repo, mock_repository):
        """Test successful department deletion."""
        # Arrange
        mock_repository.delete_by_id.return_value = True
        
        # Act
        result = await service_with_mock_repo.delete_by_id(1)
        
        # Assert
        assert result is True
        mock_repository.delete_by_id.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_delete_by_id_not_found(self, service_with_mock_repo, mock_repository):
        """Test deletion of non-existent department."""
        # Arrange
        mock_repository.delete_by_id.return_value = False
        
        # Act
        result = await service_with_mock_repo.delete_by_id(999)
        
        # Assert
        assert result is False
        mock_repository.delete_by_id.assert_called_once_with(999)
