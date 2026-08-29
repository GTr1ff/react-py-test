# ROSETIC:crud-guid


"""
Unit tests for the EmployeeBenefitService layer.
"""

from pydantic import ValidationError
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from decimal import Decimal
from sqlalchemy.exc import SQLAlchemyError

from core.pagination import PaginatedResponse
from features.tables.employee_benefits.models import EmployeeBenefitModel
from features.tables.employee_benefits.schemas import EmployeeBenefitResponse, EmployeeBenefitCreate, EmployeeBenefitUpdate, EmployeeBenefitFilter
from features.tables.employee_benefits.service import EmployeeBenefitService
from features.tables.employee_benefits.repository import EmployeeBenefitRepository

class TestEmployeeBenefitService:
    """Test cases for EmployeeBenefitService layer."""


    @pytest.fixture
    def mock_repository(self):
        """Create a mock EmployeeBenefitRepository."""
        return AsyncMock(spec=EmployeeBenefitRepository)

    @pytest.fixture
    def service_with_mock_repo(self, mock_session_async, mock_repository):
        """Create EmployeeBenefitService with mocked repository."""
        service = EmployeeBenefitService(mock_session_async)
        service.repo = mock_repository
        return service

    # ─── Create operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_create_employee_benefit_success(self, service_with_mock_repo, mock_repository, sample_data, existing_employee_benefit):
        """Test successful employee_benefits creation through service."""
        # Arrange
        new_item = EmployeeBenefitCreate(**sample_data)
        mock_repository.create.return_value = existing_employee_benefit
        
        # Act
        result = await service_with_mock_repo.create(new_item)
        
        # Assert
        assert isinstance(result, EmployeeBenefitResponse)
        mock_repository.create.assert_called_once()

    # # ─── Read operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_get_employee_benefit_by_id_success(self, service_with_mock_repo, mock_repository, existing_employee_benefit):
        """Test successful retrieval of employee_benefit by ID."""
        # Arrange
        mock_repository.get_by_id.return_value = existing_employee_benefit
        
        # Act
        result = await service_with_mock_repo.get_by_id(1)
        
        # Assert
        assert isinstance(result, EmployeeBenefitResponse)
        mock_repository.get_by_id.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_get_employee_benefit_by_id_not_found(self, service_with_mock_repo, mock_repository):
        """Test retrieval of non-existent employee_benefit."""
        # Arrange
        mock_repository.get_by_id.return_value = None
        
        # Act
        result = await service_with_mock_repo.get_by_id(999)
        
        # Assert
        assert result is None
        mock_repository.get_by_id.assert_called_once_with(999)

    @pytest.mark.asyncio
    async def test_get_all_success(self, service_with_mock_repo, mock_repository, multiple_employee_benefits, pagination_request):
        """Test successful retrieval of all employee_benefits."""
        # Arrange
        mock_repository.get_all.return_value = (multiple_employee_benefits, len(multiple_employee_benefits))
        
        # Act
        result = await service_with_mock_repo.get_all(pagination_request)
        
        # Assert
        assert isinstance(result, PaginatedResponse)
        assert len(result.items) == len(multiple_employee_benefits)
        assert result.total == len(multiple_employee_benefits)
        mock_repository.get_all.assert_called_once_with(pagination_request)

    

    @pytest.mark.asyncio
    async def test_search_success(self, service_with_mock_repo, mock_repository, multiple_employee_benefits, pagination_request):
        """Test successful search with filters."""
        # Arrange
        filters = EmployeeBenefitFilter()
        mock_repository.search.return_value = (multiple_employee_benefits, len(multiple_employee_benefits))
        
        # Act
        result = await service_with_mock_repo.search(filters, pagination_request)
        
        # Assert
        assert isinstance(result, PaginatedResponse)
        assert len(result.items) == len(multiple_employee_benefits)
        assert result.total == len(multiple_employee_benefits)
        
        # Verify repository was called with correct filter dict
        mock_repository.search.assert_called_once_with(filters, pagination_request)

    @pytest.mark.asyncio
    async def test_search_empty_results(self, service_with_mock_repo, mock_repository, pagination_request):
        """Test search with no matching results."""
        # Arrange
        filters = EmployeeBenefitFilter()
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
    async def test_update_employee_benefit_by_id_success(self, service_with_mock_repo, mock_repository, updated_employee_benefit_model):
        """Test successful employee_benefit update."""
        # Arrange
        mock_repository.update_by_id.return_value = updated_employee_benefit_model
        
        # Act
        result = await service_with_mock_repo.update_by_id(1, EmployeeBenefitUpdate())
        
        # Assert
        assert isinstance(result, EmployeeBenefitResponse)
        mock_repository.update_by_id.assert_called_once_with(1, EmployeeBenefitUpdate().model_dump(exclude_unset=True))

    # # ─── Delete operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_delete_by_id_success(self, service_with_mock_repo, mock_repository):
        """Test successful employee_benefit deletion."""
        # Arrange
        mock_repository.delete_by_id.return_value = True
        
        # Act
        result = await service_with_mock_repo.delete_by_id(1)
        
        # Assert
        assert result is True
        mock_repository.delete_by_id.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_delete_by_id_not_found(self, service_with_mock_repo, mock_repository):
        """Test deletion of non-existent employee_benefit."""
        # Arrange
        mock_repository.delete_by_id.return_value = False
        
        # Act
        result = await service_with_mock_repo.delete_by_id(999)
        
        # Assert
        assert result is False
        mock_repository.delete_by_id.assert_called_once_with(999)
