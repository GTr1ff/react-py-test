# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c


"""
Unit tests for the RecipeIngredientService layer.
"""

from pydantic import ValidationError
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from decimal import Decimal
from sqlalchemy.exc import SQLAlchemyError

from core.pagination import PaginatedResponse
from features.tables.recipe_ingredient.models import RecipeIngredientModel
from features.tables.recipe_ingredient.schemas import RecipeIngredientResponse, RecipeIngredientCreate, RecipeIngredientUpdate, RecipeIngredientFilter
from features.tables.recipe_ingredient.service import RecipeIngredientService
from features.tables.recipe_ingredient.repository import RecipeIngredientRepository

class TestRecipeIngredientService:
    """Test cases for RecipeIngredientService layer."""


    @pytest.fixture
    def mock_repository(self):
        """Create a mock RecipeIngredientRepository."""
        return AsyncMock(spec=RecipeIngredientRepository)

    @pytest.fixture
    def service_with_mock_repo(self, mock_session_async, mock_repository):
        """Create RecipeIngredientService with mocked repository."""
        service = RecipeIngredientService(mock_session_async)
        service.repo = mock_repository
        return service

    # ─── Create operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_create_recipe_ingredient_success(self, service_with_mock_repo, mock_repository, sample_data, existing_recipe_ingredient):
        """Test successful recipe_ingredient creation through service."""
        # Arrange
        new_item = RecipeIngredientCreate(**sample_data)
        mock_repository.create.return_value = existing_recipe_ingredient
        
        # Act
        result = await service_with_mock_repo.create(new_item)
        
        # Assert
        assert isinstance(result, RecipeIngredientResponse)
        mock_repository.create.assert_called_once()

    # # ─── Read operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_get_recipe_ingredient_by_id_success(self, service_with_mock_repo, mock_repository, existing_recipe_ingredient):
        """Test successful retrieval of recipe_ingredient by ID."""
        # Arrange
        mock_repository.get_by_id.return_value = existing_recipe_ingredient
        
        # Act
        result = await service_with_mock_repo.get_by_id(1)
        
        # Assert
        assert isinstance(result, RecipeIngredientResponse)
        mock_repository.get_by_id.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_get_recipe_ingredient_by_id_not_found(self, service_with_mock_repo, mock_repository):
        """Test retrieval of non-existent recipe_ingredient."""
        # Arrange
        mock_repository.get_by_id.return_value = None
        
        # Act
        result = await service_with_mock_repo.get_by_id(999)
        
        # Assert
        assert result is None
        mock_repository.get_by_id.assert_called_once_with(999)

    @pytest.mark.asyncio
    async def test_get_all_success(self, service_with_mock_repo, mock_repository, multiple_recipe_ingredient, pagination_request):
        """Test successful retrieval of all recipe_ingredient."""
        # Arrange
        mock_repository.get_all.return_value = (multiple_recipe_ingredient, len(multiple_recipe_ingredient))
        
        # Act
        result = await service_with_mock_repo.get_all(pagination_request)
        
        # Assert
        assert isinstance(result, PaginatedResponse)
        assert len(result.items) == len(multiple_recipe_ingredient)
        assert result.total == len(multiple_recipe_ingredient)
        mock_repository.get_all.assert_called_once_with(pagination_request)

    

    @pytest.mark.asyncio
    async def test_search_success(self, service_with_mock_repo, mock_repository, multiple_recipe_ingredient, pagination_request):
        """Test successful search with filters."""
        # Arrange
        filters = RecipeIngredientFilter()
        mock_repository.search.return_value = (multiple_recipe_ingredient, len(multiple_recipe_ingredient))
        
        # Act
        result = await service_with_mock_repo.search(filters, pagination_request)
        
        # Assert
        assert isinstance(result, PaginatedResponse)
        assert len(result.items) == len(multiple_recipe_ingredient)
        assert result.total == len(multiple_recipe_ingredient)
        
        # Verify repository was called with correct filter dict
        mock_repository.search.assert_called_once_with(filters, pagination_request)

    @pytest.mark.asyncio
    async def test_search_empty_results(self, service_with_mock_repo, mock_repository, pagination_request):
        """Test search with no matching results."""
        # Arrange
        filters = RecipeIngredientFilter()
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
    async def test_update_recipe_ingredient_by_id_success(self, service_with_mock_repo, mock_repository, updated_recipe_ingredient_model):
        """Test successful recipe_ingredient update."""
        # Arrange
        mock_repository.update_by_id.return_value = updated_recipe_ingredient_model
        
        # Act
        result = await service_with_mock_repo.update_by_id(1, RecipeIngredientUpdate())
        
        # Assert
        assert isinstance(result, RecipeIngredientResponse)
        mock_repository.update_by_id.assert_called_once_with(1, RecipeIngredientUpdate().model_dump(exclude_unset=True))

    # # ─── Delete operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_delete_by_id_success(self, service_with_mock_repo, mock_repository):
        """Test successful recipe_ingredient deletion."""
        # Arrange
        mock_repository.delete_by_id.return_value = True
        
        # Act
        result = await service_with_mock_repo.delete_by_id(1)
        
        # Assert
        assert result is True
        mock_repository.delete_by_id.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_delete_by_id_not_found(self, service_with_mock_repo, mock_repository):
        """Test deletion of non-existent recipe_ingredient."""
        # Arrange
        mock_repository.delete_by_id.return_value = False
        
        # Act
        result = await service_with_mock_repo.delete_by_id(999)
        
        # Assert
        assert result is False
        mock_repository.delete_by_id.assert_called_once_with(999)
