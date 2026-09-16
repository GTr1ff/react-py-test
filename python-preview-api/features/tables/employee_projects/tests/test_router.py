# ROSETIC:crud-guid


"""
Unit tests for the Employee_projects API router endpoints.
"""
import pytest


import datetime

from unittest.mock import AsyncMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient

from core.database import get_db
from core.pagination import PaginatedResponse, PaginatedResponse
from features.tables.employee_projects.schemas import EmployeeProjectResponse, EmployeeProjectCreate, EmployeeProjectUpdate, EmployeeProjectFilter
from features.tables.employee_projects import router as employee_projects_router

class TestEmployeeProjectRouter:
    """Test cases for EmployeeProject API router endpoints."""

    @pytest.fixture
    def app(self):
        """Create FastAPI app with employee_projects router for testing."""
        app = FastAPI()
        app.include_router(employee_projects_router.router)
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
    def expected_response(self, existing_employee_project):
        return EmployeeProjectResponse.model_validate(existing_employee_project)

    @pytest.fixture
    def mock_employee_project_service(self):
        """Mock EmployeeProjectService for cleaner testing."""
        with patch.object(employee_projects_router, 'EmployeeProjectService') as mock_service_class:
            mock_service_instance = AsyncMock()
            mock_service_class.return_value = mock_service_instance
            yield mock_service_class, mock_service_instance

    # ─── Integration Tests with Mocked Service ──────────────────────────────────
    def test_create_employee_project_integration_success(self, test_client, mock_session_async, expected_response, mock_employee_project_service, sample_data):
        """Integration test: Create employee_project endpoint returns 200 with mocked service."""
        # Arrange
        mock_service_class, mock_service_instance = mock_employee_project_service
        mock_service_instance.create.return_value = expected_response

        # Act
        create_data = EmployeeProjectCreate(**sample_data).model_dump(mode='json')
        response = test_client.post("/employee-projects/", json=create_data)

        # Assert
        assert response.status_code == 201           
        # Verify service was called correctly
        mock_service_class.assert_called_once_with(session=mock_session_async)
        mock_service_instance.create.assert_called_once()

    def test_create_employee_project_integration_validation_error(self, test_client, expected_response):
        """Integration test: Create employee_project with invalid data returns 422."""
        # Arrange
        invalid_request_data = {
            "assigned_date": None,
            "employee_id": "string in int field",
            "project_id": "string in int field",
            "role_name": 123,
        }

        # Act - Should get validation error before service is called
        response = test_client.post("/employee-projects/", json=invalid_request_data)

        # Assert
        assert response.status_code == 422  # FastAPI validation error
        response_data = response.json()
        assert "detail" in response_data

            

    def test_get_employee_project_by_id_success(self, test_client, mock_session_async, expected_response, mock_employee_project_service):
        """Integration test: Get employee_project by id returns 200."""
        # Unpack the mock service fixture
        mock_service_class, mock_service_instance = mock_employee_project_service
        mock_service_instance.get_by_id.return_value = expected_response

        # Act
        response = test_client.get("/employee-projects/1")

        # Assert
        assert response.status_code == 200
        
        # Verify service was called correctly
        mock_service_class.assert_called_once_with(session=mock_session_async)
        mock_service_instance.get_by_id.assert_called_once_with(1)

    def test_get_employee_project_by_id_not_found(self, test_client, mock_session_async, mock_employee_project_service):
        """Integration test: Get non-existent employee_project returns 404."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_employee_project_service
        mock_service_instance.get_by_id.return_value = None

        # Act
        response = test_client.get("/employee-projects/999")

        # Assert
        assert response.status_code == 404        
        mock_service_instance.get_by_id.assert_called_once_with(999)

    def test_get_all_employee_project_success(self, test_client, mock_session_async, mock_employee_project_service, multiple_employee_projects):
        """Integration test: Get all employee_project returns 200 with pagination."""
        # Arrange
        paginated_response = PaginatedResponse[EmployeeProjectResponse](
            items=multiple_employee_projects,
            page=1,
            size=10,
            total=len(multiple_employee_projects)
        )

        # Unpack the mock service fixture
        _, mock_service_instance = mock_employee_project_service
        mock_service_instance.get_all.return_value = paginated_response

        # Act
        response = test_client.get("/employee-projects/?page=1&size=10")

        # Assert
        assert response.status_code == 200
        mock_service_instance.get_all.assert_called_once()

    def test_search_employee_projects_success(self, test_client, mock_session_async, mock_employee_project_service, multiple_employee_projects):
        """Integration test: Search employee_project returns 200."""
        # Arrange
        search_filters = EmployeeProjectFilter().model_dump(exclude_unset=True)
        
        paginated_response = PaginatedResponse[EmployeeProjectResponse](
            items=multiple_employee_projects,
            page=1,
            size=10,
            total=1
        )

        # Unpack the mock service fixture
        _, mock_service_instance = mock_employee_project_service
        mock_service_instance.search.return_value = paginated_response

        # Act
        response = test_client.post("/employee-projects/search?page=1&size=10", json=search_filters)

        # Assert
        assert response.status_code == 200
        mock_service_instance.search.assert_called_once()

    def test_update_employee_project_success(self, test_client, updated_employee_project, mock_employee_project_service, updated_employee_project_model):
        """Integration test: Update employee_project returns 200."""
        # Arrange
        update_data = updated_employee_project.model_dump(exclude_unset=True, mode='json')
        
        updated_response = EmployeeProjectResponse.model_validate(updated_employee_project_model)

        # Unpack the mock service fixture
        _, mock_service_instance = mock_employee_project_service
        mock_service_instance.update_by_id.return_value = updated_response

        # Act
        response = test_client.put("/employee-projects/1", json=update_data)

        # Assert
        assert response.status_code == 200        
        mock_service_instance.update_by_id.assert_called_once_with(1, EmployeeProjectUpdate(**update_data))

    def test_update_employee_project_no_fields(self, test_client):
        """Integration test: Update with no fields returns 400."""
        # Act - Empty update payload
        response = test_client.put("/employee-projects/1", json={})

        # Assert
        assert response.status_code == 400

    def test_update_employee_project_not_found(self, test_client, mock_session_async, mock_employee_project_service, updated_employee_project):
        """Integration test: Update non-existent employee_project returns 404."""
        # Arrange
        update_data = updated_employee_project.model_dump(exclude_unset=True, mode='json')

        # Unpack the mock service fixture
        _, mock_service_instance = mock_employee_project_service
        mock_service_instance.update_by_id.return_value = None

        # Act
        response = test_client.put("/employee-projects/999", json=update_data)

        # Assert
        assert response.status_code == 404

    def test_delete_employee_project_success(self, test_client, mock_session_async, mock_employee_project_service):
        """Integration test: Delete employee_project returns 200."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_employee_project_service
        mock_service_instance.delete_by_id.return_value = True

        # Act
        response = test_client.delete("/employee-projects/1")

        # Assert
        assert response.status_code == 200

        mock_service_instance.delete_by_id.assert_called_once_with(1)

    def test_delete_employee_project_not_found(self, test_client, mock_session_async, mock_employee_project_service):
        """Integration test: Delete non-existent employee_project returns 404."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_employee_project_service
        mock_service_instance.delete_by_id.return_value = False

        # Act
        response = test_client.delete("/employee-projects/999")

        # Assert
        assert response.status_code == 404
