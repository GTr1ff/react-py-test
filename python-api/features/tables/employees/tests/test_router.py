# ROSETIC:crud-guid


"""
Unit tests for the Employees API router endpoints.
"""
import pytest


import datetime

from unittest.mock import AsyncMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient

from core.database import get_db
from core.pagination import PaginatedResponse, PaginatedResponse
from features.tables.employees.schemas import EmployeeResponse, EmployeeCreate, EmployeeUpdate, EmployeeFilter
from features.tables.employees import router as employees_router

class TestEmployeeRouter:
    """Test cases for Employee API router endpoints."""

    @pytest.fixture
    def app(self):
        """Create FastAPI app with employees router for testing."""
        app = FastAPI()
        app.include_router(employees_router.router)
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
    def expected_response(self, existing_employee):
        return EmployeeResponse.model_validate(existing_employee)

    @pytest.fixture
    def mock_employee_service(self):
        """Mock EmployeeService for cleaner testing."""
        with patch.object(employees_router, 'EmployeeService') as mock_service_class:
            mock_service_instance = AsyncMock()
            mock_service_class.return_value = mock_service_instance
            yield mock_service_class, mock_service_instance

    # ─── Integration Tests with Mocked Service ──────────────────────────────────
    def test_create_employee_integration_success(self, test_client, mock_session_async, expected_response, mock_employee_service, sample_data):
        """Integration test: Create employee endpoint returns 200 with mocked service."""
        # Arrange
        mock_service_class, mock_service_instance = mock_employee_service
        mock_service_instance.create.return_value = expected_response

        # Act
        create_data = EmployeeCreate(**sample_data).model_dump(mode='json')
        response = test_client.post("/employees/", json=create_data)

        # Assert
        assert response.status_code == 201           
        # Verify service was called correctly
        mock_service_class.assert_called_once_with(session=mock_session_async)
        mock_service_instance.create.assert_called_once()

    def test_create_employee_integration_validation_error(self, test_client, expected_response):
        """Integration test: Create employee with invalid data returns 422."""
        # Arrange
        invalid_request_data = {
            "birth_date": None,
            "created_at": None,
            "department_id": "string in int field",
            "email": 123,
            "first_name": 123,
            "hire_date": None,
            "is_active": "string in bool field",
            "last_name": 123,
            "phone": 123,
            "updated_at": None,
        }

        # Act - Should get validation error before service is called
        response = test_client.post("/employees/", json=invalid_request_data)

        # Assert
        assert response.status_code == 422  # FastAPI validation error
        response_data = response.json()
        assert "detail" in response_data

            

    def test_get_employee_by_id_success(self, test_client, mock_session_async, expected_response, mock_employee_service):
        """Integration test: Get employee by id returns 200."""
        # Unpack the mock service fixture
        mock_service_class, mock_service_instance = mock_employee_service
        mock_service_instance.get_by_id.return_value = expected_response

        # Act
        response = test_client.get("/employees/1")

        # Assert
        assert response.status_code == 200
        
        # Verify service was called correctly
        mock_service_class.assert_called_once_with(session=mock_session_async)
        mock_service_instance.get_by_id.assert_called_once_with(1)

    def test_get_employee_by_id_not_found(self, test_client, mock_session_async, mock_employee_service):
        """Integration test: Get non-existent employee returns 404."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_employee_service
        mock_service_instance.get_by_id.return_value = None

        # Act
        response = test_client.get("/employees/999")

        # Assert
        assert response.status_code == 404        
        mock_service_instance.get_by_id.assert_called_once_with(999)

    def test_get_all_employee_success(self, test_client, mock_session_async, mock_employee_service, multiple_employees):
        """Integration test: Get all employee returns 200 with pagination."""
        # Arrange
        paginated_response = PaginatedResponse[EmployeeResponse](
            items=multiple_employees,
            page=1,
            size=10,
            total=len(multiple_employees)
        )

        # Unpack the mock service fixture
        _, mock_service_instance = mock_employee_service
        mock_service_instance.get_all.return_value = paginated_response

        # Act
        response = test_client.get("/employees/?page=1&size=10")

        # Assert
        assert response.status_code == 200
        mock_service_instance.get_all.assert_called_once()

    def test_search_employees_success(self, test_client, mock_session_async, mock_employee_service, multiple_employees):
        """Integration test: Search employee returns 200."""
        # Arrange
        search_filters = EmployeeFilter().model_dump(exclude_unset=True)
        
        paginated_response = PaginatedResponse[EmployeeResponse](
            items=multiple_employees,
            page=1,
            size=10,
            total=1
        )

        # Unpack the mock service fixture
        _, mock_service_instance = mock_employee_service
        mock_service_instance.search.return_value = paginated_response

        # Act
        response = test_client.post("/employees/search?page=1&size=10", json=search_filters)

        # Assert
        assert response.status_code == 200
        mock_service_instance.search.assert_called_once()

    def test_update_employee_success(self, test_client, updated_employee, mock_employee_service, updated_employee_model):
        """Integration test: Update employee returns 200."""
        # Arrange
        update_data = updated_employee.model_dump(exclude_unset=True, mode='json')
        
        updated_response = EmployeeResponse.model_validate(updated_employee_model)

        # Unpack the mock service fixture
        _, mock_service_instance = mock_employee_service
        mock_service_instance.update_by_id.return_value = updated_response

        # Act
        response = test_client.put("/employees/1", json=update_data)

        # Assert
        assert response.status_code == 200        
        mock_service_instance.update_by_id.assert_called_once_with(1, EmployeeUpdate(**update_data))

    def test_update_employee_no_fields(self, test_client):
        """Integration test: Update with no fields returns 400."""
        # Act - Empty update payload
        response = test_client.put("/employees/1", json={})

        # Assert
        assert response.status_code == 400

    def test_update_employee_not_found(self, test_client, mock_session_async, mock_employee_service, updated_employee):
        """Integration test: Update non-existent employee returns 404."""
        # Arrange
        update_data = updated_employee.model_dump(exclude_unset=True, mode='json')

        # Unpack the mock service fixture
        _, mock_service_instance = mock_employee_service
        mock_service_instance.update_by_id.return_value = None

        # Act
        response = test_client.put("/employees/999", json=update_data)

        # Assert
        assert response.status_code == 404

    def test_delete_employee_success(self, test_client, mock_session_async, mock_employee_service):
        """Integration test: Delete employee returns 200."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_employee_service
        mock_service_instance.delete_by_id.return_value = True

        # Act
        response = test_client.delete("/employees/1")

        # Assert
        assert response.status_code == 200

        mock_service_instance.delete_by_id.assert_called_once_with(1)

    def test_delete_employee_not_found(self, test_client, mock_session_async, mock_employee_service):
        """Integration test: Delete non-existent employee returns 404."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_employee_service
        mock_service_instance.delete_by_id.return_value = False

        # Act
        response = test_client.delete("/employees/999")

        # Assert
        assert response.status_code == 404
