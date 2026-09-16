# ROSETIC:crud-guid


"""
Unit tests for the Departments API router endpoints.
"""
import pytest


import datetime
from decimal import Decimal
from unittest.mock import AsyncMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient

from core.database import get_db
from core.pagination import PaginatedResponse, PaginatedResponse
from features.tables.departments.schemas import DepartmentResponse, DepartmentCreate, DepartmentUpdate, DepartmentFilter
from features.tables.departments import router as departments_router

class TestDepartmentRouter:
    """Test cases for Department API router endpoints."""

    @pytest.fixture
    def app(self):
        """Create FastAPI app with departments router for testing."""
        app = FastAPI()
        app.include_router(departments_router.router)
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
    def expected_response(self, existing_department):
        return DepartmentResponse.model_validate(existing_department)

    @pytest.fixture
    def mock_department_service(self):
        """Mock DepartmentService for cleaner testing."""
        with patch.object(departments_router, 'DepartmentService') as mock_service_class:
            mock_service_instance = AsyncMock()
            mock_service_class.return_value = mock_service_instance
            yield mock_service_class, mock_service_instance

    # ─── Integration Tests with Mocked Service ──────────────────────────────────
    def test_create_department_integration_success(self, test_client, mock_session_async, expected_response, mock_department_service, sample_data):
        """Integration test: Create department endpoint returns 200 with mocked service."""
        # Arrange
        mock_service_class, mock_service_instance = mock_department_service
        mock_service_instance.create.return_value = expected_response

        # Act
        create_data = DepartmentCreate(**sample_data).model_dump(mode='json')
        response = test_client.post("/departments/", json=create_data)

        # Assert
        assert response.status_code == 201           
        # Verify service was called correctly
        mock_service_class.assert_called_once_with(session=mock_session_async)
        mock_service_instance.create.assert_called_once()

    def test_create_department_integration_validation_error(self, test_client, expected_response):
        """Integration test: Create department with invalid data returns 422."""
        # Arrange
        invalid_request_data = {
            "budget": "string in int field",
            "created_at": None,
            "department_name": 123,
            "location": 123,
            "manager_id": "string in int field",
            "updated_at": None,
        }

        # Act - Should get validation error before service is called
        response = test_client.post("/departments/", json=invalid_request_data)

        # Assert
        assert response.status_code == 422  # FastAPI validation error
        response_data = response.json()
        assert "detail" in response_data

            

    def test_get_department_by_id_success(self, test_client, mock_session_async, expected_response, mock_department_service):
        """Integration test: Get department by id returns 200."""
        # Unpack the mock service fixture
        mock_service_class, mock_service_instance = mock_department_service
        mock_service_instance.get_by_id.return_value = expected_response

        # Act
        response = test_client.get("/departments/1")

        # Assert
        assert response.status_code == 200
        
        # Verify service was called correctly
        mock_service_class.assert_called_once_with(session=mock_session_async)
        mock_service_instance.get_by_id.assert_called_once_with(1)

    def test_get_department_by_id_not_found(self, test_client, mock_session_async, mock_department_service):
        """Integration test: Get non-existent department returns 404."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_department_service
        mock_service_instance.get_by_id.return_value = None

        # Act
        response = test_client.get("/departments/999")

        # Assert
        assert response.status_code == 404        
        mock_service_instance.get_by_id.assert_called_once_with(999)

    def test_get_all_department_success(self, test_client, mock_session_async, mock_department_service, multiple_departments):
        """Integration test: Get all department returns 200 with pagination."""
        # Arrange
        paginated_response = PaginatedResponse[DepartmentResponse](
            items=multiple_departments,
            page=1,
            size=10,
            total=len(multiple_departments)
        )

        # Unpack the mock service fixture
        _, mock_service_instance = mock_department_service
        mock_service_instance.get_all.return_value = paginated_response

        # Act
        response = test_client.get("/departments/?page=1&size=10")

        # Assert
        assert response.status_code == 200
        mock_service_instance.get_all.assert_called_once()

    def test_search_departments_success(self, test_client, mock_session_async, mock_department_service, multiple_departments):
        """Integration test: Search department returns 200."""
        # Arrange
        search_filters = DepartmentFilter().model_dump(exclude_unset=True)
        
        paginated_response = PaginatedResponse[DepartmentResponse](
            items=multiple_departments,
            page=1,
            size=10,
            total=1
        )

        # Unpack the mock service fixture
        _, mock_service_instance = mock_department_service
        mock_service_instance.search.return_value = paginated_response

        # Act
        response = test_client.post("/departments/search?page=1&size=10", json=search_filters)

        # Assert
        assert response.status_code == 200
        mock_service_instance.search.assert_called_once()

    def test_update_department_success(self, test_client, updated_department, mock_department_service, updated_department_model):
        """Integration test: Update department returns 200."""
        # Arrange
        update_data = updated_department.model_dump(exclude_unset=True, mode='json')
        
        updated_response = DepartmentResponse.model_validate(updated_department_model)

        # Unpack the mock service fixture
        _, mock_service_instance = mock_department_service
        mock_service_instance.update_by_id.return_value = updated_response

        # Act
        response = test_client.put("/departments/1", json=update_data)

        # Assert
        assert response.status_code == 200        
        mock_service_instance.update_by_id.assert_called_once_with(1, DepartmentUpdate(**update_data))

    def test_update_department_no_fields(self, test_client):
        """Integration test: Update with no fields returns 400."""
        # Act - Empty update payload
        response = test_client.put("/departments/1", json={})

        # Assert
        assert response.status_code == 400

    def test_update_department_not_found(self, test_client, mock_session_async, mock_department_service, updated_department):
        """Integration test: Update non-existent department returns 404."""
        # Arrange
        update_data = updated_department.model_dump(exclude_unset=True, mode='json')

        # Unpack the mock service fixture
        _, mock_service_instance = mock_department_service
        mock_service_instance.update_by_id.return_value = None

        # Act
        response = test_client.put("/departments/999", json=update_data)

        # Assert
        assert response.status_code == 404

    def test_delete_department_success(self, test_client, mock_session_async, mock_department_service):
        """Integration test: Delete department returns 200."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_department_service
        mock_service_instance.delete_by_id.return_value = True

        # Act
        response = test_client.delete("/departments/1")

        # Assert
        assert response.status_code == 200

        mock_service_instance.delete_by_id.assert_called_once_with(1)

    def test_delete_department_not_found(self, test_client, mock_session_async, mock_department_service):
        """Integration test: Delete non-existent department returns 404."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_department_service
        mock_service_instance.delete_by_id.return_value = False

        # Act
        response = test_client.delete("/departments/999")

        # Assert
        assert response.status_code == 404
