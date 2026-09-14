# ROSETIC:crud-guid


"""
Unit tests for the EmployeeService layer.
"""

from pydantic import ValidationError
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from decimal import Decimal
from sqlalchemy.exc import SQLAlchemyError

from core.pagination import PaginatedResponse
from features.tables.employees.models import EmployeeModel
from features.tables.employees.schemas import EmployeeResponse, EmployeeCreate, EmployeeUpdate, EmployeeFilter
from features.tables.employees.service import EmployeeService
from features.tables.employees.repository import EmployeeRepository

class TestEmployeeService:
    """Test cases for EmployeeService layer."""


    @pytest.fixture
    def mock_repository(self):
        """Create a mock EmployeeRepository."""
        return AsyncMock(spec=EmployeeRepository)

    @pytest.fixture
    def service_with_mock_repo(self, mock_session_async, mock_repository):
        """Create EmployeeService with mocked repository."""
        service = EmployeeService(mock_session_async)
        service.repo = mock_repository
        return service

    # ─── Create operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_create_employee_success(self, service_with_mock_repo, mock_repository, sample_data, existing_employee):
        """Test successful employees creation through service."""
        # Arrange
        new_item = EmployeeCreate(**sample_data)
        mock_repository.create.return_value = existing_employee
        
        # Act
        result = await service_with_mock_repo.create(new_item)
        
        # Assert
        assert isinstance(result, EmployeeResponse)
        mock_repository.create.assert_called_once()

    # # ─── Read operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_get_employee_by_id_success(self, service_with_mock_repo, mock_repository, existing_employee):
        """Test successful retrieval of employee by ID."""
        # Arrange
        mock_repository.get_by_id.return_value = existing_employee
        
        # Act
        result = await service_with_mock_repo.get_by_id(1)
        
        # Assert
        assert isinstance(result, EmployeeResponse)
        mock_repository.get_by_id.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_get_employee_by_id_not_found(self, service_with_mock_repo, mock_repository):
        """Test retrieval of non-existent employee."""
        # Arrange
        mock_repository.get_by_id.return_value = None
        
        # Act
        result = await service_with_mock_repo.get_by_id(999)
        
        # Assert
        assert result is None
        mock_repository.get_by_id.assert_called_once_with(999)

    @pytest.mark.asyncio
    async def test_get_all_success(self, service_with_mock_repo, mock_repository, multiple_employees, pagination_request):
        """Test successful retrieval of all employees."""
        # Arrange
        mock_repository.get_all.return_value = (multiple_employees, len(multiple_employees))
        
        # Act
        result = await service_with_mock_repo.get_all(pagination_request)
        
        # Assert
        assert isinstance(result, PaginatedResponse)
        assert len(result.items) == len(multiple_employees)
        assert result.total == len(multiple_employees)
        mock_repository.get_all.assert_called_once_with(pagination_request)

    

    @pytest.mark.asyncio
    async def test_search_success(self, service_with_mock_repo, mock_repository, multiple_employees, pagination_request):
        """Test successful search with filters."""
        # Arrange
        filters = EmployeeFilter()
        mock_repository.search.return_value = (multiple_employees, len(multiple_employees))
        
        # Act
        result = await service_with_mock_repo.search(filters, pagination_request)
        
        # Assert
        assert isinstance(result, PaginatedResponse)
        assert len(result.items) == len(multiple_employees)
        assert result.total == len(multiple_employees)
        
        # Verify repository was called with correct filter dict
        mock_repository.search.assert_called_once_with(filters, pagination_request)

    @pytest.mark.asyncio
    async def test_search_empty_results(self, service_with_mock_repo, mock_repository, pagination_request):
        """Test search with no matching results."""
        # Arrange
        filters = EmployeeFilter()
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
    async def test_update_employee_by_id_success(self, service_with_mock_repo, mock_repository, updated_employee_model):
        """Test successful employee update."""
        # Arrange
        mock_repository.update_by_id.return_value = updated_employee_model
        
        # Act
        result = await service_with_mock_repo.update_by_id(1, EmployeeUpdate())
        
        # Assert
        assert isinstance(result, EmployeeResponse)
        mock_repository.update_by_id.assert_called_once_with(1, EmployeeUpdate().model_dump(exclude_unset=True))

    # # ─── Delete operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_delete_by_id_success(self, service_with_mock_repo, mock_repository):
        """Test successful employee deletion."""
        # Arrange
        mock_repository.delete_by_id.return_value = True
        
        # Act
        result = await service_with_mock_repo.delete_by_id(1)
        
        # Assert
        assert result is True
        mock_repository.delete_by_id.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_delete_by_id_not_found(self, service_with_mock_repo, mock_repository):
        """Test deletion of non-existent employee."""
        # Arrange
        mock_repository.delete_by_id.return_value = False
        
        # Act
        result = await service_with_mock_repo.delete_by_id(999)
        
        # Assert
        assert result is False
        mock_repository.delete_by_id.assert_called_once_with(999)
