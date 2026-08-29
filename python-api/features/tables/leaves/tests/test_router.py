# ROSETIC:crud-guid


"""
Unit tests for the Leaves API router endpoints.
"""
import pytest


import datetime

from unittest.mock import AsyncMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient

from core.database import get_db
from core.pagination import PaginatedResponse, PaginatedResponse
from features.tables.leaves.schemas import LeafResponse, LeafCreate, LeafUpdate, LeafFilter
from features.tables.leaves import router as leaves_router

class TestLeafRouter:
    """Test cases for Leaf API router endpoints."""

    @pytest.fixture
    def app(self):
        """Create FastAPI app with leaves router for testing."""
        app = FastAPI()
        app.include_router(leaves_router.router)
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
    def expected_response(self, existing_leaf):
        return LeafResponse.model_validate(existing_leaf)

    @pytest.fixture
    def mock_leaf_service(self):
        """Mock LeafService for cleaner testing."""
        with patch.object(leaves_router, 'LeafService') as mock_service_class:
            mock_service_instance = AsyncMock()
            mock_service_class.return_value = mock_service_instance
            yield mock_service_class, mock_service_instance

    # ─── Integration Tests with Mocked Service ──────────────────────────────────
    def test_create_leaf_integration_success(self, test_client, mock_session_async, expected_response, mock_leaf_service, sample_data):
        """Integration test: Create leaf endpoint returns 200 with mocked service."""
        # Arrange
        mock_service_class, mock_service_instance = mock_leaf_service
        mock_service_instance.create.return_value = expected_response

        # Act
        create_data = LeafCreate(**sample_data).model_dump(mode='json')
        response = test_client.post("/leaves/", json=create_data)

        # Assert
        assert response.status_code == 201           
        # Verify service was called correctly
        mock_service_class.assert_called_once_with(session=mock_session_async)
        mock_service_instance.create.assert_called_once()

    def test_create_leaf_integration_validation_error(self, test_client, expected_response):
        """Integration test: Create leaf with invalid data returns 422."""
        # Arrange
        invalid_request_data = {
            "approval_status": 123,
            "approved_by": "string in int field",
            "employee_id": "string in int field",
            "end_date": None,
            "reason": 123,
            "start_date": None,
        }

        # Act - Should get validation error before service is called
        response = test_client.post("/leaves/", json=invalid_request_data)

        # Assert
        assert response.status_code == 422  # FastAPI validation error
        response_data = response.json()
        assert "detail" in response_data

            

    def test_get_leaf_by_id_success(self, test_client, mock_session_async, expected_response, mock_leaf_service):
        """Integration test: Get leaf by id returns 200."""
        # Unpack the mock service fixture
        mock_service_class, mock_service_instance = mock_leaf_service
        mock_service_instance.get_by_id.return_value = expected_response

        # Act
        response = test_client.get("/leaves/1")

        # Assert
        assert response.status_code == 200
        
        # Verify service was called correctly
        mock_service_class.assert_called_once_with(session=mock_session_async)
        mock_service_instance.get_by_id.assert_called_once_with(1)

    def test_get_leaf_by_id_not_found(self, test_client, mock_session_async, mock_leaf_service):
        """Integration test: Get non-existent leaf returns 404."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_leaf_service
        mock_service_instance.get_by_id.return_value = None

        # Act
        response = test_client.get("/leaves/999")

        # Assert
        assert response.status_code == 404        
        mock_service_instance.get_by_id.assert_called_once_with(999)

    def test_get_all_leaf_success(self, test_client, mock_session_async, mock_leaf_service, multiple_leaves):
        """Integration test: Get all leaf returns 200 with pagination."""
        # Arrange
        paginated_response = PaginatedResponse[LeafResponse](
            items=multiple_leaves,
            page=1,
            size=10,
            total=len(multiple_leaves)
        )

        # Unpack the mock service fixture
        _, mock_service_instance = mock_leaf_service
        mock_service_instance.get_all.return_value = paginated_response

        # Act
        response = test_client.get("/leaves/?page=1&size=10")

        # Assert
        assert response.status_code == 200
        mock_service_instance.get_all.assert_called_once()

    def test_search_leaves_success(self, test_client, mock_session_async, mock_leaf_service, multiple_leaves):
        """Integration test: Search leaf returns 200."""
        # Arrange
        search_filters = LeafFilter().model_dump(exclude_unset=True)
        
        paginated_response = PaginatedResponse[LeafResponse](
            items=multiple_leaves,
            page=1,
            size=10,
            total=1
        )

        # Unpack the mock service fixture
        _, mock_service_instance = mock_leaf_service
        mock_service_instance.search.return_value = paginated_response

        # Act
        response = test_client.post("/leaves/search?page=1&size=10", json=search_filters)

        # Assert
        assert response.status_code == 200
        mock_service_instance.search.assert_called_once()

    def test_update_leaf_success(self, test_client, updated_leaf, mock_leaf_service, updated_leaf_model):
        """Integration test: Update leaf returns 200."""
        # Arrange
        update_data = updated_leaf.model_dump(exclude_unset=True, mode='json')
        
        updated_response = LeafResponse.model_validate(updated_leaf_model)

        # Unpack the mock service fixture
        _, mock_service_instance = mock_leaf_service
        mock_service_instance.update_by_id.return_value = updated_response

        # Act
        response = test_client.put("/leaves/1", json=update_data)

        # Assert
        assert response.status_code == 200        
        mock_service_instance.update_by_id.assert_called_once_with(1, LeafUpdate(**update_data))

    def test_update_leaf_no_fields(self, test_client):
        """Integration test: Update with no fields returns 400."""
        # Act - Empty update payload
        response = test_client.put("/leaves/1", json={})

        # Assert
        assert response.status_code == 400

    def test_update_leaf_not_found(self, test_client, mock_session_async, mock_leaf_service, updated_leaf):
        """Integration test: Update non-existent leaf returns 404."""
        # Arrange
        update_data = updated_leaf.model_dump(exclude_unset=True, mode='json')

        # Unpack the mock service fixture
        _, mock_service_instance = mock_leaf_service
        mock_service_instance.update_by_id.return_value = None

        # Act
        response = test_client.put("/leaves/999", json=update_data)

        # Assert
        assert response.status_code == 404

    def test_delete_leaf_success(self, test_client, mock_session_async, mock_leaf_service):
        """Integration test: Delete leaf returns 200."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_leaf_service
        mock_service_instance.delete_by_id.return_value = True

        # Act
        response = test_client.delete("/leaves/1")

        # Assert
        assert response.status_code == 200

        mock_service_instance.delete_by_id.assert_called_once_with(1)

    def test_delete_leaf_not_found(self, test_client, mock_session_async, mock_leaf_service):
        """Integration test: Delete non-existent leaf returns 404."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_leaf_service
        mock_service_instance.delete_by_id.return_value = False

        # Act
        response = test_client.delete("/leaves/999")

        # Assert
        assert response.status_code == 404
