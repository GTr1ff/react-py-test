# ROSETIC:crud-guid


"""
Unit tests for the RoleService layer.
"""

from pydantic import ValidationError
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from decimal import Decimal
from sqlalchemy.exc import SQLAlchemyError

from core.pagination import PaginatedResponse
from features.tables.roles.models import RoleModel
from features.tables.roles.schemas import RoleResponse, RoleCreate, RoleUpdate, RoleFilter
from features.tables.roles.service import RoleService
from features.tables.roles.repository import RoleRepository

class TestRoleService:
    """Test cases for RoleService layer."""


    @pytest.fixture
    def mock_repository(self):
        """Create a mock RoleRepository."""
        return AsyncMock(spec=RoleRepository)

    @pytest.fixture
    def service_with_mock_repo(self, mock_session_async, mock_repository):
        """Create RoleService with mocked repository."""
        service = RoleService(mock_session_async)
        service.repo = mock_repository
        return service

    # ─── Create operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_create_role_success(self, service_with_mock_repo, mock_repository, sample_data, existing_role):
        """Test successful roles creation through service."""
        # Arrange
        new_item = RoleCreate(**sample_data)
        mock_repository.create.return_value = existing_role
        
        # Act
        result = await service_with_mock_repo.create(new_item)
        
        # Assert
        assert isinstance(result, RoleResponse)
        mock_repository.create.assert_called_once()

    # # ─── Read operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_get_role_by_id_success(self, service_with_mock_repo, mock_repository, existing_role):
        """Test successful retrieval of role by ID."""
        # Arrange
        mock_repository.get_by_id.return_value = existing_role
        
        # Act
        result = await service_with_mock_repo.get_by_id(1)
        
        # Assert
        assert isinstance(result, RoleResponse)
        mock_repository.get_by_id.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_get_role_by_id_not_found(self, service_with_mock_repo, mock_repository):
        """Test retrieval of non-existent role."""
        # Arrange
        mock_repository.get_by_id.return_value = None
        
        # Act
        result = await service_with_mock_repo.get_by_id(999)
        
        # Assert
        assert result is None
        mock_repository.get_by_id.assert_called_once_with(999)

    @pytest.mark.asyncio
    async def test_get_all_success(self, service_with_mock_repo, mock_repository, multiple_roles, pagination_request):
        """Test successful retrieval of all roles."""
        # Arrange
        mock_repository.get_all.return_value = (multiple_roles, len(multiple_roles))
        
        # Act
        result = await service_with_mock_repo.get_all(pagination_request)
        
        # Assert
        assert isinstance(result, PaginatedResponse)
        assert len(result.items) == len(multiple_roles)
        assert result.total == len(multiple_roles)
        mock_repository.get_all.assert_called_once_with(pagination_request)

    

    @pytest.mark.asyncio
    async def test_search_success(self, service_with_mock_repo, mock_repository, multiple_roles, pagination_request):
        """Test successful search with filters."""
        # Arrange
        filters = RoleFilter()
        mock_repository.search.return_value = (multiple_roles, len(multiple_roles))
        
        # Act
        result = await service_with_mock_repo.search(filters, pagination_request)
        
        # Assert
        assert isinstance(result, PaginatedResponse)
        assert len(result.items) == len(multiple_roles)
        assert result.total == len(multiple_roles)
        
        # Verify repository was called with correct filter dict
        mock_repository.search.assert_called_once_with(filters, pagination_request)

    @pytest.mark.asyncio
    async def test_search_empty_results(self, service_with_mock_repo, mock_repository, pagination_request):
        """Test search with no matching results."""
        # Arrange
        filters = RoleFilter()
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
    async def test_update_role_by_id_success(self, service_with_mock_repo, mock_repository, updated_role_model):
        """Test successful role update."""
        # Arrange
        mock_repository.update_by_id.return_value = updated_role_model
        
        # Act
        result = await service_with_mock_repo.update_by_id(1, RoleUpdate())
        
        # Assert
        assert isinstance(result, RoleResponse)
        mock_repository.update_by_id.assert_called_once_with(1, RoleUpdate().model_dump(exclude_unset=True))

    # # ─── Delete operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_delete_by_id_success(self, service_with_mock_repo, mock_repository):
        """Test successful role deletion."""
        # Arrange
        mock_repository.delete_by_id.return_value = True
        
        # Act
        result = await service_with_mock_repo.delete_by_id(1)
        
        # Assert
        assert result is True
        mock_repository.delete_by_id.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_delete_by_id_not_found(self, service_with_mock_repo, mock_repository):
        """Test deletion of non-existent role."""
        # Arrange
        mock_repository.delete_by_id.return_value = False
        
        # Act
        result = await service_with_mock_repo.delete_by_id(999)
        
        # Assert
        assert result is False
        mock_repository.delete_by_id.assert_called_once_with(999)
