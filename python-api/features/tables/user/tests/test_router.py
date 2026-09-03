# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c


"""
Unit tests for the User API router endpoints.
"""
import pytest


import datetime

from unittest.mock import AsyncMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient

from core.database import get_db
from core.pagination import PaginatedResponse, PaginatedResponse
from features.tables.user.schemas import UserResponse, UserCreate, UserUpdate, UserFilter
from features.tables.user import router as user_router

class TestUserRouter:
    """Test cases for User API router endpoints."""

    @pytest.fixture
    def app(self):
        """Create FastAPI app with user router for testing."""
        app = FastAPI()
        app.include_router(user_router.router)
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
    def expected_response(self, existing_user):
        return UserResponse.model_validate(existing_user)

    @pytest.fixture
    def mock_user_service(self):
        """Mock UserService for cleaner testing."""
        with patch.object(user_router, 'UserService') as mock_service_class:
            mock_service_instance = AsyncMock()
            mock_service_class.return_value = mock_service_instance
            yield mock_service_class, mock_service_instance

    # ─── Integration Tests with Mocked Service ──────────────────────────────────
    def test_create_user_integration_success(self, test_client, mock_session_async, expected_response, mock_user_service, sample_data):
        """Integration test: Create user endpoint returns 200 with mocked service."""
        # Arrange
        mock_service_class, mock_service_instance = mock_user_service
        mock_service_instance.create.return_value = expected_response

        # Act
        create_data = UserCreate(**sample_data).model_dump(mode='json')
        response = test_client.post("/user/", json=create_data)

        # Assert
        assert response.status_code == 201           
        # Verify service was called correctly
        mock_service_class.assert_called_once_with(session=mock_session_async)
        mock_service_instance.create.assert_called_once()

    def test_create_user_integration_validation_error(self, test_client, expected_response):
        """Integration test: Create user with invalid data returns 422."""
        # Arrange
        invalid_request_data = {
            "username": 123,
            "email": 123,
            "hashed_password": 123,
            "is_active": "string in bool field",
            "last_login_at": None,
            "created_at": None,
            "updated_at": None,
        }

        # Act - Should get validation error before service is called
        response = test_client.post("/user/", json=invalid_request_data)

        # Assert
        assert response.status_code == 422  # FastAPI validation error
        response_data = response.json()
        assert "detail" in response_data

            

    def test_get_user_by_id_success(self, test_client, mock_session_async, expected_response, mock_user_service):
        """Integration test: Get user by id returns 200."""
        # Unpack the mock service fixture
        mock_service_class, mock_service_instance = mock_user_service
        mock_service_instance.get_by_id.return_value = expected_response

        # Act
        response = test_client.get("/user/1")

        # Assert
        assert response.status_code == 200
        
        # Verify service was called correctly
        mock_service_class.assert_called_once_with(session=mock_session_async)
        mock_service_instance.get_by_id.assert_called_once_with(1)

    def test_get_user_by_id_not_found(self, test_client, mock_session_async, mock_user_service):
        """Integration test: Get non-existent user returns 404."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_user_service
        mock_service_instance.get_by_id.return_value = None

        # Act
        response = test_client.get("/user/999")

        # Assert
        assert response.status_code == 404        
        mock_service_instance.get_by_id.assert_called_once_with(999)

    def test_get_all_user_success(self, test_client, mock_session_async, mock_user_service, multiple_user):
        """Integration test: Get all user returns 200 with pagination."""
        # Arrange
        paginated_response = PaginatedResponse[UserResponse](
            items=multiple_user,
            page=1,
            size=10,
            total=len(multiple_user)
        )

        # Unpack the mock service fixture
        _, mock_service_instance = mock_user_service
        mock_service_instance.get_all.return_value = paginated_response

        # Act
        response = test_client.get("/user/?page=1&size=10")

        # Assert
        assert response.status_code == 200
        mock_service_instance.get_all.assert_called_once()

    def test_search_user_success(self, test_client, mock_session_async, mock_user_service, multiple_user):
        """Integration test: Search user returns 200."""
        # Arrange
        search_filters = UserFilter().model_dump(exclude_unset=True)
        
        paginated_response = PaginatedResponse[UserResponse](
            items=multiple_user,
            page=1,
            size=10,
            total=1
        )

        # Unpack the mock service fixture
        _, mock_service_instance = mock_user_service
        mock_service_instance.search.return_value = paginated_response

        # Act
        response = test_client.post("/user/search?page=1&size=10", json=search_filters)

        # Assert
        assert response.status_code == 200
        mock_service_instance.search.assert_called_once()

    def test_update_user_success(self, test_client, updated_user, mock_user_service, updated_user_model):
        """Integration test: Update user returns 200."""
        # Arrange
        update_data = updated_user.model_dump(exclude_unset=True, mode='json')
        
        updated_response = UserResponse.model_validate(updated_user_model)

        # Unpack the mock service fixture
        _, mock_service_instance = mock_user_service
        mock_service_instance.update_by_id.return_value = updated_response

        # Act
        response = test_client.put("/user/1", json=update_data)

        # Assert
        assert response.status_code == 200        
        mock_service_instance.update_by_id.assert_called_once_with(1, UserUpdate(**update_data))

    def test_update_user_no_fields(self, test_client):
        """Integration test: Update with no fields returns 400."""
        # Act - Empty update payload
        response = test_client.put("/user/1", json={})

        # Assert
        assert response.status_code == 400

    def test_update_user_not_found(self, test_client, mock_session_async, mock_user_service, updated_user):
        """Integration test: Update non-existent user returns 404."""
        # Arrange
        update_data = updated_user.model_dump(exclude_unset=True, mode='json')

        # Unpack the mock service fixture
        _, mock_service_instance = mock_user_service
        mock_service_instance.update_by_id.return_value = None

        # Act
        response = test_client.put("/user/999", json=update_data)

        # Assert
        assert response.status_code == 404

    def test_delete_user_success(self, test_client, mock_session_async, mock_user_service):
        """Integration test: Delete user returns 200."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_user_service
        mock_service_instance.delete_by_id.return_value = True

        # Act
        response = test_client.delete("/user/1")

        # Assert
        assert response.status_code == 200

        mock_service_instance.delete_by_id.assert_called_once_with(1)

    def test_delete_user_not_found(self, test_client, mock_session_async, mock_user_service):
        """Integration test: Delete non-existent user returns 404."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_user_service
        mock_service_instance.delete_by_id.return_value = False

        # Act
        response = test_client.delete("/user/999")

        # Assert
        assert response.status_code == 404
