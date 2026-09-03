# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c


"""
Unit tests for the Inventory_item API router endpoints.
"""
import pytest


import datetime
from decimal import Decimal
from unittest.mock import AsyncMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient

from core.database import get_db
from core.pagination import PaginatedResponse, PaginatedResponse
from features.tables.inventory_item.schemas import InventoryItemResponse, InventoryItemCreate, InventoryItemUpdate, InventoryItemFilter
from features.tables.inventory_item import router as inventory_item_router

class TestInventoryItemRouter:
    """Test cases for InventoryItem API router endpoints."""

    @pytest.fixture
    def app(self):
        """Create FastAPI app with inventory_item router for testing."""
        app = FastAPI()
        app.include_router(inventory_item_router.router)
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
    def expected_response(self, existing_inventory_item):
        return InventoryItemResponse.model_validate(existing_inventory_item)

    @pytest.fixture
    def mock_inventory_item_service(self):
        """Mock InventoryItemService for cleaner testing."""
        with patch.object(inventory_item_router, 'InventoryItemService') as mock_service_class:
            mock_service_instance = AsyncMock()
            mock_service_class.return_value = mock_service_instance
            yield mock_service_class, mock_service_instance

    # ─── Integration Tests with Mocked Service ──────────────────────────────────
    def test_create_inventory_item_integration_success(self, test_client, mock_session_async, expected_response, mock_inventory_item_service, sample_data):
        """Integration test: Create inventory_item endpoint returns 200 with mocked service."""
        # Arrange
        mock_service_class, mock_service_instance = mock_inventory_item_service
        mock_service_instance.create.return_value = expected_response

        # Act
        create_data = InventoryItemCreate(**sample_data).model_dump(mode='json')
        response = test_client.post("/inventory-item/", json=create_data)

        # Assert
        assert response.status_code == 201           
        # Verify service was called correctly
        mock_service_class.assert_called_once_with(session=mock_session_async)
        mock_service_instance.create.assert_called_once()

    def test_create_inventory_item_integration_validation_error(self, test_client, expected_response):
        """Integration test: Create inventory_item with invalid data returns 422."""
        # Arrange
        invalid_request_data = {
            "user_id": "string in int field",
            "ingredient_id": "string in int field",
            "quantity": "string in int field",
            "unit": 123,
            "created_at": None,
            "updated_at": None,
        }

        # Act - Should get validation error before service is called
        response = test_client.post("/inventory-item/", json=invalid_request_data)

        # Assert
        assert response.status_code == 422  # FastAPI validation error
        response_data = response.json()
        assert "detail" in response_data

            

    def test_get_inventory_item_by_id_success(self, test_client, mock_session_async, expected_response, mock_inventory_item_service):
        """Integration test: Get inventory_item by id returns 200."""
        # Unpack the mock service fixture
        mock_service_class, mock_service_instance = mock_inventory_item_service
        mock_service_instance.get_by_id.return_value = expected_response

        # Act
        response = test_client.get("/inventory-item/1")

        # Assert
        assert response.status_code == 200
        
        # Verify service was called correctly
        mock_service_class.assert_called_once_with(session=mock_session_async)
        mock_service_instance.get_by_id.assert_called_once_with(1)

    def test_get_inventory_item_by_id_not_found(self, test_client, mock_session_async, mock_inventory_item_service):
        """Integration test: Get non-existent inventory_item returns 404."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_inventory_item_service
        mock_service_instance.get_by_id.return_value = None

        # Act
        response = test_client.get("/inventory-item/999")

        # Assert
        assert response.status_code == 404        
        mock_service_instance.get_by_id.assert_called_once_with(999)

    def test_get_all_inventory_item_success(self, test_client, mock_session_async, mock_inventory_item_service, multiple_inventory_item):
        """Integration test: Get all inventory_item returns 200 with pagination."""
        # Arrange
        paginated_response = PaginatedResponse[InventoryItemResponse](
            items=multiple_inventory_item,
            page=1,
            size=10,
            total=len(multiple_inventory_item)
        )

        # Unpack the mock service fixture
        _, mock_service_instance = mock_inventory_item_service
        mock_service_instance.get_all.return_value = paginated_response

        # Act
        response = test_client.get("/inventory-item/?page=1&size=10")

        # Assert
        assert response.status_code == 200
        mock_service_instance.get_all.assert_called_once()

    def test_search_inventory_item_success(self, test_client, mock_session_async, mock_inventory_item_service, multiple_inventory_item):
        """Integration test: Search inventory_item returns 200."""
        # Arrange
        search_filters = InventoryItemFilter().model_dump(exclude_unset=True)
        
        paginated_response = PaginatedResponse[InventoryItemResponse](
            items=multiple_inventory_item,
            page=1,
            size=10,
            total=1
        )

        # Unpack the mock service fixture
        _, mock_service_instance = mock_inventory_item_service
        mock_service_instance.search.return_value = paginated_response

        # Act
        response = test_client.post("/inventory-item/search?page=1&size=10", json=search_filters)

        # Assert
        assert response.status_code == 200
        mock_service_instance.search.assert_called_once()

    def test_update_inventory_item_success(self, test_client, updated_inventory_item, mock_inventory_item_service, updated_inventory_item_model):
        """Integration test: Update inventory_item returns 200."""
        # Arrange
        update_data = updated_inventory_item.model_dump(exclude_unset=True, mode='json')
        
        updated_response = InventoryItemResponse.model_validate(updated_inventory_item_model)

        # Unpack the mock service fixture
        _, mock_service_instance = mock_inventory_item_service
        mock_service_instance.update_by_id.return_value = updated_response

        # Act
        response = test_client.put("/inventory-item/1", json=update_data)

        # Assert
        assert response.status_code == 200        
        mock_service_instance.update_by_id.assert_called_once_with(1, InventoryItemUpdate(**update_data))

    def test_update_inventory_item_no_fields(self, test_client):
        """Integration test: Update with no fields returns 400."""
        # Act - Empty update payload
        response = test_client.put("/inventory-item/1", json={})

        # Assert
        assert response.status_code == 400

    def test_update_inventory_item_not_found(self, test_client, mock_session_async, mock_inventory_item_service, updated_inventory_item):
        """Integration test: Update non-existent inventory_item returns 404."""
        # Arrange
        update_data = updated_inventory_item.model_dump(exclude_unset=True, mode='json')

        # Unpack the mock service fixture
        _, mock_service_instance = mock_inventory_item_service
        mock_service_instance.update_by_id.return_value = None

        # Act
        response = test_client.put("/inventory-item/999", json=update_data)

        # Assert
        assert response.status_code == 404

    def test_delete_inventory_item_success(self, test_client, mock_session_async, mock_inventory_item_service):
        """Integration test: Delete inventory_item returns 200."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_inventory_item_service
        mock_service_instance.delete_by_id.return_value = True

        # Act
        response = test_client.delete("/inventory-item/1")

        # Assert
        assert response.status_code == 200

        mock_service_instance.delete_by_id.assert_called_once_with(1)

    def test_delete_inventory_item_not_found(self, test_client, mock_session_async, mock_inventory_item_service):
        """Integration test: Delete non-existent inventory_item returns 404."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_inventory_item_service
        mock_service_instance.delete_by_id.return_value = False

        # Act
        response = test_client.delete("/inventory-item/999")

        # Assert
        assert response.status_code == 404
