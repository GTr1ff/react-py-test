# ROSETIC:crud-guid


"""
Unit tests for the Roles API router endpoints.
"""
import pytest




from unittest.mock import AsyncMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient

from core.database import get_db
from core.pagination import PaginatedResponse, PaginatedResponse
from features.tables.roles.schemas import RoleResponse, RoleCreate, RoleUpdate, RoleFilter
from features.tables.roles import router as roles_router

class TestRoleRouter:
    """Test cases for Role API router endpoints."""

    @pytest.fixture
    def app(self):
        """Create FastAPI app with roles router for testing."""
        app = FastAPI()
        app.include_router(roles_router.router)
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
    def expected_response(self, existing_role):
        return RoleResponse.model_validate(existing_role)

    @pytest.fixture
    def mock_role_service(self):
        """Mock RoleService for cleaner testing."""
        with patch.object(roles_router, 'RoleService') as mock_service_class:
            mock_service_instance = AsyncMock()
            mock_service_class.return_value = mock_service_instance
            yield mock_service_class, mock_service_instance

    # ─── Integration Tests with Mocked Service ──────────────────────────────────
    def test_create_role_integration_success(self, test_client, mock_session_async, expected_response, mock_role_service, sample_data):
        """Integration test: Create role endpoint returns 200 with mocked service."""
        # Arrange
        mock_service_class, mock_service_instance = mock_role_service
        mock_service_instance.create.return_value = expected_response

        # Act
        create_data = RoleCreate(**sample_data).model_dump(mode='json')
        response = test_client.post("/roles/", json=create_data)

        # Assert
        assert response.status_code == 201           
        # Verify service was called correctly
        mock_service_class.assert_called_once_with(session=mock_session_async)
        mock_service_instance.create.assert_called_once()

    def test_create_role_integration_validation_error(self, test_client, expected_response):
        """Integration test: Create role with invalid data returns 422."""
        # Arrange
        invalid_request_data = {
            "privileges": None,
            "role_name": 123,
        }

        # Act - Should get validation error before service is called
        response = test_client.post("/roles/", json=invalid_request_data)

        # Assert
        assert response.status_code == 422  # FastAPI validation error
        response_data = response.json()
        assert "detail" in response_data

            

    def test_get_role_by_id_success(self, test_client, mock_session_async, expected_response, mock_role_service):
        """Integration test: Get role by id returns 200."""
        # Unpack the mock service fixture
        mock_service_class, mock_service_instance = mock_role_service
        mock_service_instance.get_by_id.return_value = expected_response

        # Act
        response = test_client.get("/roles/1")

        # Assert
        assert response.status_code == 200
        
        # Verify service was called correctly
        mock_service_class.assert_called_once_with(session=mock_session_async)
        mock_service_instance.get_by_id.assert_called_once_with(1)

    def test_get_role_by_id_not_found(self, test_client, mock_session_async, mock_role_service):
        """Integration test: Get non-existent role returns 404."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_role_service
        mock_service_instance.get_by_id.return_value = None

        # Act
        response = test_client.get("/roles/999")

        # Assert
        assert response.status_code == 404        
        mock_service_instance.get_by_id.assert_called_once_with(999)

    def test_get_all_role_success(self, test_client, mock_session_async, mock_role_service, multiple_roles):
        """Integration test: Get all role returns 200 with pagination."""
        # Arrange
        paginated_response = PaginatedResponse[RoleResponse](
            items=multiple_roles,
            page=1,
            size=10,
            total=len(multiple_roles)
        )

        # Unpack the mock service fixture
        _, mock_service_instance = mock_role_service
        mock_service_instance.get_all.return_value = paginated_response

        # Act
        response = test_client.get("/roles/?page=1&size=10")

        # Assert
        assert response.status_code == 200
        mock_service_instance.get_all.assert_called_once()

    def test_search_roles_success(self, test_client, mock_session_async, mock_role_service, multiple_roles):
        """Integration test: Search role returns 200."""
        # Arrange
        search_filters = RoleFilter().model_dump(exclude_unset=True)
        
        paginated_response = PaginatedResponse[RoleResponse](
            items=multiple_roles,
            page=1,
            size=10,
            total=1
        )

        # Unpack the mock service fixture
        _, mock_service_instance = mock_role_service
        mock_service_instance.search.return_value = paginated_response

        # Act
        response = test_client.post("/roles/search?page=1&size=10", json=search_filters)

        # Assert
        assert response.status_code == 200
        mock_service_instance.search.assert_called_once()

    def test_update_role_success(self, test_client, updated_role, mock_role_service, updated_role_model):
        """Integration test: Update role returns 200."""
        # Arrange
        update_data = updated_role.model_dump(exclude_unset=True, mode='json')
        
        updated_response = RoleResponse.model_validate(updated_role_model)

        # Unpack the mock service fixture
        _, mock_service_instance = mock_role_service
        mock_service_instance.update_by_id.return_value = updated_response

        # Act
        response = test_client.put("/roles/1", json=update_data)

        # Assert
        assert response.status_code == 200        
        mock_service_instance.update_by_id.assert_called_once_with(1, RoleUpdate(**update_data))

    def test_update_role_no_fields(self, test_client):
        """Integration test: Update with no fields returns 400."""
        # Act - Empty update payload
        response = test_client.put("/roles/1", json={})

        # Assert
        assert response.status_code == 400

    def test_update_role_not_found(self, test_client, mock_session_async, mock_role_service, updated_role):
        """Integration test: Update non-existent role returns 404."""
        # Arrange
        update_data = updated_role.model_dump(exclude_unset=True, mode='json')

        # Unpack the mock service fixture
        _, mock_service_instance = mock_role_service
        mock_service_instance.update_by_id.return_value = None

        # Act
        response = test_client.put("/roles/999", json=update_data)

        # Assert
        assert response.status_code == 404

    def test_delete_role_success(self, test_client, mock_session_async, mock_role_service):
        """Integration test: Delete role returns 200."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_role_service
        mock_service_instance.delete_by_id.return_value = True

        # Act
        response = test_client.delete("/roles/1")

        # Assert
        assert response.status_code == 200

        mock_service_instance.delete_by_id.assert_called_once_with(1)

    def test_delete_role_not_found(self, test_client, mock_session_async, mock_role_service):
        """Integration test: Delete non-existent role returns 404."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_role_service
        mock_service_instance.delete_by_id.return_value = False

        # Act
        response = test_client.delete("/roles/999")

        # Assert
        assert response.status_code == 404
