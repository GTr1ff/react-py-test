# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c


"""
Unit tests for the Recipe_ingredient API router endpoints.
"""
import pytest


import datetime
from decimal import Decimal
from unittest.mock import AsyncMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient

from core.database import get_db
from core.pagination import PaginatedResponse, PaginatedResponse
from features.tables.recipe_ingredient.schemas import RecipeIngredientResponse, RecipeIngredientCreate, RecipeIngredientUpdate, RecipeIngredientFilter
from features.tables.recipe_ingredient import router as recipe_ingredient_router

class TestRecipeIngredientRouter:
    """Test cases for RecipeIngredient API router endpoints."""

    @pytest.fixture
    def app(self):
        """Create FastAPI app with recipe_ingredient router for testing."""
        app = FastAPI()
        app.include_router(recipe_ingredient_router.router)
        return app

    @pytest.fixture
    def test_client(self, app, mock_session_async):
        """Test client with mocked database dependency."""
        # Create test client
        test_client = TestClient(app)
        
        # Override the dependency
        test_client.app.dependency_overrides[get_db] = lambda: mock_session_async
        
        yield test_client
        
        # Clean up after test
        test_client.app.dependency_overrides.clear()

    @pytest.fixture
    def expected_response(self, existing_recipe_ingredient):
        return RecipeIngredientResponse.model_validate(existing_recipe_ingredient)

    @pytest.fixture
    def mock_recipe_ingredient_service(self):
        """Mock RecipeIngredientService for cleaner testing."""
        with patch.object(recipe_ingredient_router, 'RecipeIngredientService') as mock_service_class:
            mock_service_instance = AsyncMock()
            mock_service_class.return_value = mock_service_instance
            yield mock_service_class, mock_service_instance

    # ─── Integration Tests with Mocked Service ──────────────────────────────────
    def test_create_recipe_ingredient_integration_success(self, test_client, mock_session_async, expected_response, mock_recipe_ingredient_service, sample_data):
        """Integration test: Create recipe_ingredient endpoint returns 200 with mocked service."""
        # Arrange
        mock_service_class, mock_service_instance = mock_recipe_ingredient_service
        mock_service_instance.create.return_value = expected_response

        # Act
        create_data = RecipeIngredientCreate(**sample_data).model_dump(mode='json')
        response = test_client.post("/recipe-ingredient/", json=create_data)

        # Assert
        assert response.status_code == 201           
        # Verify service was called correctly
        mock_service_class.assert_called_once_with(session=mock_session_async)
        mock_service_instance.create.assert_called_once()

    def test_create_recipe_ingredient_integration_validation_error(self, test_client, expected_response):
        """Integration test: Create recipe_ingredient with invalid data returns 422."""
        # Arrange
        invalid_request_data = {
            "quantity": "string in int field",
            "unit": 123,
            "created_at": None,
            "updated_at": None,
        }

        # Act - Should get validation error before service is called
        response = test_client.post("/recipe-ingredient/", json=invalid_request_data)

        # Assert
        assert response.status_code == 422  # FastAPI validation error
        response_data = response.json()
        assert "detail" in response_data

            

    def test_get_recipe_ingredient_by_id_success(self, test_client, mock_session_async, expected_response, mock_recipe_ingredient_service):
        """Integration test: Get recipe_ingredient by id returns 200."""
        # Unpack the mock service fixture
        mock_service_class, mock_service_instance = mock_recipe_ingredient_service
        mock_service_instance.get_by_id.return_value = expected_response

        # Act
        response = test_client.get("/recipe-ingredient/1")

        # Assert
        assert response.status_code == 200
        
        # Verify service was called correctly
        mock_service_class.assert_called_once_with(session=mock_session_async)
        mock_service_instance.get_by_id.assert_called_once_with(1)

    def test_get_recipe_ingredient_by_id_not_found(self, test_client, mock_session_async, mock_recipe_ingredient_service):
        """Integration test: Get non-existent recipe_ingredient returns 404."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_recipe_ingredient_service
        mock_service_instance.get_by_id.return_value = None

        # Act
        response = test_client.get("/recipe-ingredient/999")

        # Assert
        assert response.status_code == 404        
        mock_service_instance.get_by_id.assert_called_once_with(999)

    def test_get_all_recipe_ingredient_success(self, test_client, mock_session_async, mock_recipe_ingredient_service, multiple_recipe_ingredient):
        """Integration test: Get all recipe_ingredient returns 200 with pagination."""
        # Arrange
        paginated_response = PaginatedResponse[RecipeIngredientResponse](
            items=multiple_recipe_ingredient,
            page=1,
            size=10,
            total=len(multiple_recipe_ingredient)
        )

        # Unpack the mock service fixture
        _, mock_service_instance = mock_recipe_ingredient_service
        mock_service_instance.get_all.return_value = paginated_response

        # Act
        response = test_client.get("/recipe-ingredient/?page=1&size=10")

        # Assert
        assert response.status_code == 200
        mock_service_instance.get_all.assert_called_once()

    def test_search_recipe_ingredient_success(self, test_client, mock_session_async, mock_recipe_ingredient_service, multiple_recipe_ingredient):
        """Integration test: Search recipe_ingredient returns 200."""
        # Arrange
        search_filters = RecipeIngredientFilter().model_dump(exclude_unset=True)
        
        paginated_response = PaginatedResponse[RecipeIngredientResponse](
            items=multiple_recipe_ingredient,
            page=1,
            size=10,
            total=1
        )

        # Unpack the mock service fixture
        _, mock_service_instance = mock_recipe_ingredient_service
        mock_service_instance.search.return_value = paginated_response

        # Act
        response = test_client.post("/recipe-ingredient/search?page=1&size=10", json=search_filters)

        # Assert
        assert response.status_code == 200
        mock_service_instance.search.assert_called_once()

    def test_update_recipe_ingredient_success(self, test_client, updated_recipe_ingredient, mock_recipe_ingredient_service, updated_recipe_ingredient_model):
        """Integration test: Update recipe_ingredient returns 200."""
        # Arrange
        update_data = updated_recipe_ingredient.model_dump(exclude_unset=True, mode='json')
        
        updated_response = RecipeIngredientResponse.model_validate(updated_recipe_ingredient_model)

        # Unpack the mock service fixture
        _, mock_service_instance = mock_recipe_ingredient_service
        mock_service_instance.update_by_id.return_value = updated_response

        # Act
        response = test_client.put("/recipe-ingredient/1", json=update_data)

        # Assert
        assert response.status_code == 200        
        mock_service_instance.update_by_id.assert_called_once_with(1, RecipeIngredientUpdate(**update_data))

    def test_update_recipe_ingredient_no_fields(self, test_client):
        """Integration test: Update with no fields returns 400."""
        # Act - Empty update payload
        response = test_client.put("/recipe-ingredient/1", json={})

        # Assert
        assert response.status_code == 400

    def test_update_recipe_ingredient_not_found(self, test_client, mock_session_async, mock_recipe_ingredient_service, updated_recipe_ingredient):
        """Integration test: Update non-existent recipe_ingredient returns 404."""
        # Arrange
        update_data = updated_recipe_ingredient.model_dump(exclude_unset=True, mode='json')

        # Unpack the mock service fixture
        _, mock_service_instance = mock_recipe_ingredient_service
        mock_service_instance.update_by_id.return_value = None

        # Act
        response = test_client.put("/recipe-ingredient/999", json=update_data)

        # Assert
        assert response.status_code == 404

    def test_delete_recipe_ingredient_success(self, test_client, mock_session_async, mock_recipe_ingredient_service):
        """Integration test: Delete recipe_ingredient returns 200."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_recipe_ingredient_service
        mock_service_instance.delete_by_id.return_value = True

        # Act
        response = test_client.delete("/recipe-ingredient/1")

        # Assert
        assert response.status_code == 200

        mock_service_instance.delete_by_id.assert_called_once_with(1)

    def test_delete_recipe_ingredient_not_found(self, test_client, mock_session_async, mock_recipe_ingredient_service):
        """Integration test: Delete non-existent recipe_ingredient returns 404."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_recipe_ingredient_service
        mock_service_instance.delete_by_id.return_value = False

        # Act
        response = test_client.delete("/recipe-ingredient/999")

        # Assert
        assert response.status_code == 404
