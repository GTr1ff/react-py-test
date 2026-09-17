# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c


"""
Unit tests for the Tag API router endpoints.
"""
import pytest


import datetime

from unittest.mock import AsyncMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient

from core.database import get_db
from core.pagination import PaginatedResponse, PaginatedResponse
from features.tables.tag.schemas import TagResponse, TagCreate, TagUpdate, TagFilter
from features.tables.tag import router as tag_router

class TestTagRouter:
    """Test cases for Tag API router endpoints."""

    @pytest.fixture
    def app(self):
        """Create FastAPI app with tag router for testing."""
        app = FastAPI()
        app.include_router(tag_router.router)
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
    def expected_response(self, existing_tag):
        return TagResponse.model_validate(existing_tag)

    @pytest.fixture
    def mock_tag_service(self):
        """Mock TagService for cleaner testing."""
        with patch.object(tag_router, 'TagService') as mock_service_class:
            mock_service_instance = AsyncMock()
            mock_service_class.return_value = mock_service_instance
            yield mock_service_class, mock_service_instance

    # ─── Integration Tests with Mocked Service ──────────────────────────────────
    def test_create_tag_integration_success(self, test_client, mock_session_async, expected_response, mock_tag_service, sample_data):
        """Integration test: Create tag endpoint returns 200 with mocked service."""
        # Arrange
        mock_service_class, mock_service_instance = mock_tag_service
        mock_service_instance.create.return_value = expected_response

        # Act
        create_data = TagCreate(**sample_data).model_dump(mode='json')
        response = test_client.post("/tag/", json=create_data)

        # Assert
        assert response.status_code == 201           
        # Verify service was called correctly
        mock_service_class.assert_called_once_with(session=mock_session_async)
        mock_service_instance.create.assert_called_once()

    def test_create_tag_integration_validation_error(self, test_client, expected_response):
        """Integration test: Create tag with invalid data returns 422."""
        # Arrange
        invalid_request_data = {
            "tag_name": 123,
            "description": 123,
            "created_at": None,
            "updated_at": None,
        }

        # Act - Should get validation error before service is called
        response = test_client.post("/tag/", json=invalid_request_data)

        # Assert
        assert response.status_code == 422  # FastAPI validation error
        response_data = response.json()
        assert "detail" in response_data

            

    def test_get_tag_by_id_success(self, test_client, mock_session_async, expected_response, mock_tag_service):
        """Integration test: Get tag by id returns 200."""
        # Unpack the mock service fixture
        mock_service_class, mock_service_instance = mock_tag_service
        mock_service_instance.get_by_id.return_value = expected_response

        # Act
        response = test_client.get("/tag/1")

        # Assert
        assert response.status_code == 200
        
        # Verify service was called correctly
        mock_service_class.assert_called_once_with(session=mock_session_async)
        mock_service_instance.get_by_id.assert_called_once_with(1)

    def test_get_tag_by_id_not_found(self, test_client, mock_session_async, mock_tag_service):
        """Integration test: Get non-existent tag returns 404."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_tag_service
        mock_service_instance.get_by_id.return_value = None

        # Act
        response = test_client.get("/tag/999")

        # Assert
        assert response.status_code == 404        
        mock_service_instance.get_by_id.assert_called_once_with(999)

    def test_get_all_tag_success(self, test_client, mock_session_async, mock_tag_service, multiple_tag):
        """Integration test: Get all tag returns 200 with pagination."""
        # Arrange
        paginated_response = PaginatedResponse[TagResponse](
            items=multiple_tag,
            page=1,
            size=10,
            total=len(multiple_tag)
        )

        # Unpack the mock service fixture
        _, mock_service_instance = mock_tag_service
        mock_service_instance.get_all.return_value = paginated_response

        # Act
        response = test_client.get("/tag/?page=1&size=10")

        # Assert
        assert response.status_code == 200
        mock_service_instance.get_all.assert_called_once()

    def test_search_tag_success(self, test_client, mock_session_async, mock_tag_service, multiple_tag):
        """Integration test: Search tag returns 200."""
        # Arrange
        search_filters = TagFilter().model_dump(exclude_unset=True)
        
        paginated_response = PaginatedResponse[TagResponse](
            items=multiple_tag,
            page=1,
            size=10,
            total=1
        )

        # Unpack the mock service fixture
        _, mock_service_instance = mock_tag_service
        mock_service_instance.search.return_value = paginated_response

        # Act
        response = test_client.post("/tag/search?page=1&size=10", json=search_filters)

        # Assert
        assert response.status_code == 200
        mock_service_instance.search.assert_called_once()

    def test_update_tag_success(self, test_client, updated_tag, mock_tag_service, updated_tag_model):
        """Integration test: Update tag returns 200."""
        # Arrange
        update_data = updated_tag.model_dump(exclude_unset=True, mode='json')
        
        updated_response = TagResponse.model_validate(updated_tag_model)

        # Unpack the mock service fixture
        _, mock_service_instance = mock_tag_service
        mock_service_instance.update_by_id.return_value = updated_response

        # Act
        response = test_client.put("/tag/1", json=update_data)

        # Assert
        assert response.status_code == 200        
        mock_service_instance.update_by_id.assert_called_once_with(1, TagUpdate(**update_data))

    def test_update_tag_no_fields(self, test_client):
        """Integration test: Update with no fields returns 400."""
        # Act - Empty update payload
        response = test_client.put("/tag/1", json={})

        # Assert
        assert response.status_code == 400

    def test_update_tag_not_found(self, test_client, mock_session_async, mock_tag_service, updated_tag):
        """Integration test: Update non-existent tag returns 404."""
        # Arrange
        update_data = updated_tag.model_dump(exclude_unset=True, mode='json')

        # Unpack the mock service fixture
        _, mock_service_instance = mock_tag_service
        mock_service_instance.update_by_id.return_value = None

        # Act
        response = test_client.put("/tag/999", json=update_data)

        # Assert
        assert response.status_code == 404

    def test_delete_tag_success(self, test_client, mock_session_async, mock_tag_service):
        """Integration test: Delete tag returns 200."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_tag_service
        mock_service_instance.delete_by_id.return_value = True

        # Act
        response = test_client.delete("/tag/1")

        # Assert
        assert response.status_code == 200

        mock_service_instance.delete_by_id.assert_called_once_with(1)

    def test_delete_tag_not_found(self, test_client, mock_session_async, mock_tag_service):
        """Integration test: Delete non-existent tag returns 404."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_tag_service
        mock_service_instance.delete_by_id.return_value = False

        # Act
        response = test_client.delete("/tag/999")

        # Assert
        assert response.status_code == 404
