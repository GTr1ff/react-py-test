# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c


"""
Unit tests for the Shopping_list_item API router endpoints.
"""
import pytest


import datetime
from decimal import Decimal
from unittest.mock import AsyncMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient

from core.database import get_db
from core.pagination import PaginatedResponse, PaginatedResponse
from features.tables.shopping_list_item.schemas import ShoppingListItemResponse, ShoppingListItemCreate, ShoppingListItemUpdate, ShoppingListItemFilter
from features.tables.shopping_list_item import router as shopping_list_item_router

class TestShoppingListItemRouter:
    """Test cases for ShoppingListItem API router endpoints."""

    @pytest.fixture
    def app(self):
        """Create FastAPI app with shopping_list_item router for testing."""
        app = FastAPI()
        app.include_router(shopping_list_item_router.router)
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
    def expected_response(self, existing_shopping_list_item):
        return ShoppingListItemResponse.model_validate(existing_shopping_list_item)

    @pytest.fixture
    def mock_shopping_list_item_service(self):
        """Mock ShoppingListItemService for cleaner testing."""
        with patch.object(shopping_list_item_router, 'ShoppingListItemService') as mock_service_class:
            mock_service_instance = AsyncMock()
            mock_service_class.return_value = mock_service_instance
            yield mock_service_class, mock_service_instance

    # ─── Integration Tests with Mocked Service ──────────────────────────────────
    def test_create_shopping_list_item_integration_success(self, test_client, mock_session_async, expected_response, mock_shopping_list_item_service, sample_data):
        """Integration test: Create shopping_list_item endpoint returns 200 with mocked service."""
        # Arrange
        mock_service_class, mock_service_instance = mock_shopping_list_item_service
        mock_service_instance.create.return_value = expected_response

        # Act
        create_data = ShoppingListItemCreate(**sample_data).model_dump(mode='json')
        response = test_client.post("/shopping-list-item/", json=create_data)

        # Assert
        assert response.status_code == 201           
        # Verify service was called correctly
        mock_service_class.assert_called_once_with(session=mock_session_async)
        mock_service_instance.create.assert_called_once()

    def test_create_shopping_list_item_integration_validation_error(self, test_client, expected_response):
        """Integration test: Create shopping_list_item with invalid data returns 422."""
        # Arrange
        invalid_request_data = {
            "user_id": "string in int field",
            "item_name": 123,
            "quantity": "string in int field",
            "notes": 123,
            "created_at": None,
            "updated_at": None,
        }

        # Act - Should get validation error before service is called
        response = test_client.post("/shopping-list-item/", json=invalid_request_data)

        # Assert
        assert response.status_code == 422  # FastAPI validation error
        response_data = response.json()
        assert "detail" in response_data

            

    def test_get_shopping_list_item_by_id_success(self, test_client, mock_session_async, expected_response, mock_shopping_list_item_service):
        """Integration test: Get shopping_list_item by id returns 200."""
        # Unpack the mock service fixture
        mock_service_class, mock_service_instance = mock_shopping_list_item_service
        mock_service_instance.get_by_id.return_value = expected_response

        # Act
        response = test_client.get("/shopping-list-item/1")

        # Assert
        assert response.status_code == 200
        
        # Verify service was called correctly
        mock_service_class.assert_called_once_with(session=mock_session_async)
        mock_service_instance.get_by_id.assert_called_once_with(1)

    def test_get_shopping_list_item_by_id_not_found(self, test_client, mock_session_async, mock_shopping_list_item_service):
        """Integration test: Get non-existent shopping_list_item returns 404."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_shopping_list_item_service
        mock_service_instance.get_by_id.return_value = None

        # Act
        response = test_client.get("/shopping-list-item/999")

        # Assert
        assert response.status_code == 404        
        mock_service_instance.get_by_id.assert_called_once_with(999)

    def test_get_all_shopping_list_item_success(self, test_client, mock_session_async, mock_shopping_list_item_service, multiple_shopping_list_item):
        """Integration test: Get all shopping_list_item returns 200 with pagination."""
        # Arrange
        paginated_response = PaginatedResponse[ShoppingListItemResponse](
            items=multiple_shopping_list_item,
            page=1,
            size=10,
            total=len(multiple_shopping_list_item)
        )

        # Unpack the mock service fixture
        _, mock_service_instance = mock_shopping_list_item_service
        mock_service_instance.get_all.return_value = paginated_response

        # Act
        response = test_client.get("/shopping-list-item/?page=1&size=10")

        # Assert
        assert response.status_code == 200
        mock_service_instance.get_all.assert_called_once()

    def test_search_shopping_list_item_success(self, test_client, mock_session_async, mock_shopping_list_item_service, multiple_shopping_list_item):
        """Integration test: Search shopping_list_item returns 200."""
        # Arrange
        search_filters = ShoppingListItemFilter().model_dump(exclude_unset=True)
        
        paginated_response = PaginatedResponse[ShoppingListItemResponse](
            items=multiple_shopping_list_item,
            page=1,
            size=10,
            total=1
        )

        # Unpack the mock service fixture
        _, mock_service_instance = mock_shopping_list_item_service
        mock_service_instance.search.return_value = paginated_response

        # Act
        response = test_client.post("/shopping-list-item/search?page=1&size=10", json=search_filters)

        # Assert
        assert response.status_code == 200
        mock_service_instance.search.assert_called_once()

    def test_update_shopping_list_item_success(self, test_client, updated_shopping_list_item, mock_shopping_list_item_service, updated_shopping_list_item_model):
        """Integration test: Update shopping_list_item returns 200."""
        # Arrange
        update_data = updated_shopping_list_item.model_dump(exclude_unset=True, mode='json')
        
        updated_response = ShoppingListItemResponse.model_validate(updated_shopping_list_item_model)

        # Unpack the mock service fixture
        _, mock_service_instance = mock_shopping_list_item_service
        mock_service_instance.update_by_id.return_value = updated_response

        # Act
        response = test_client.put("/shopping-list-item/1", json=update_data)

        # Assert
        assert response.status_code == 200        
        mock_service_instance.update_by_id.assert_called_once_with(1, ShoppingListItemUpdate(**update_data))

    def test_update_shopping_list_item_no_fields(self, test_client):
        """Integration test: Update with no fields returns 400."""
        # Act - Empty update payload
        response = test_client.put("/shopping-list-item/1", json={})

        # Assert
        assert response.status_code == 400

    def test_update_shopping_list_item_not_found(self, test_client, mock_session_async, mock_shopping_list_item_service, updated_shopping_list_item):
        """Integration test: Update non-existent shopping_list_item returns 404."""
        # Arrange
        update_data = updated_shopping_list_item.model_dump(exclude_unset=True, mode='json')

        # Unpack the mock service fixture
        _, mock_service_instance = mock_shopping_list_item_service
        mock_service_instance.update_by_id.return_value = None

        # Act
        response = test_client.put("/shopping-list-item/999", json=update_data)

        # Assert
        assert response.status_code == 404

    def test_delete_shopping_list_item_success(self, test_client, mock_session_async, mock_shopping_list_item_service):
        """Integration test: Delete shopping_list_item returns 200."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_shopping_list_item_service
        mock_service_instance.delete_by_id.return_value = True

        # Act
        response = test_client.delete("/shopping-list-item/1")

        # Assert
        assert response.status_code == 200

        mock_service_instance.delete_by_id.assert_called_once_with(1)

    def test_delete_shopping_list_item_not_found(self, test_client, mock_session_async, mock_shopping_list_item_service):
        """Integration test: Delete non-existent shopping_list_item returns 404."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_shopping_list_item_service
        mock_service_instance.delete_by_id.return_value = False

        # Act
        response = test_client.delete("/shopping-list-item/999")

        # Assert
        assert response.status_code == 404
