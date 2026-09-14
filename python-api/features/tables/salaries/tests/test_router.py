# ROSETIC:crud-guid


"""
Unit tests for the Salaries API router endpoints.
"""
import pytest


import datetime
from decimal import Decimal
from unittest.mock import AsyncMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient

from core.database import get_db
from core.pagination import PaginatedResponse, PaginatedResponse
from features.tables.salaries.schemas import SalaryResponse, SalaryCreate, SalaryUpdate, SalaryFilter
from features.tables.salaries import router as salaries_router

class TestSalaryRouter:
    """Test cases for Salary API router endpoints."""

    @pytest.fixture
    def app(self):
        """Create FastAPI app with salaries router for testing."""
        app = FastAPI()
        app.include_router(salaries_router.router)
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
    def expected_response(self, existing_salary):
        return SalaryResponse.model_validate(existing_salary)

    @pytest.fixture
    def mock_salary_service(self):
        """Mock SalaryService for cleaner testing."""
        with patch.object(salaries_router, 'SalaryService') as mock_service_class:
            mock_service_instance = AsyncMock()
            mock_service_class.return_value = mock_service_instance
            yield mock_service_class, mock_service_instance

    # ─── Integration Tests with Mocked Service ──────────────────────────────────
    def test_create_salary_integration_success(self, test_client, mock_session_async, expected_response, mock_salary_service, sample_data):
        """Integration test: Create salary endpoint returns 200 with mocked service."""
        # Arrange
        mock_service_class, mock_service_instance = mock_salary_service
        mock_service_instance.create.return_value = expected_response

        # Act
        create_data = SalaryCreate(**sample_data).model_dump(mode='json')
        response = test_client.post("/salaries/", json=create_data)

        # Assert
        assert response.status_code == 201           
        # Verify service was called correctly
        mock_service_class.assert_called_once_with(session=mock_session_async)
        mock_service_instance.create.assert_called_once()

    def test_create_salary_integration_validation_error(self, test_client, expected_response):
        """Integration test: Create salary with invalid data returns 422."""
        # Arrange
        invalid_request_data = {
            "currency": 123,
            "effective_date": None,
            "employee_id": "string in int field",
            "salary": "string in int field",
        }

        # Act - Should get validation error before service is called
        response = test_client.post("/salaries/", json=invalid_request_data)

        # Assert
        assert response.status_code == 422  # FastAPI validation error
        response_data = response.json()
        assert "detail" in response_data

            

    def test_get_salary_by_id_success(self, test_client, mock_session_async, expected_response, mock_salary_service):
        """Integration test: Get salary by id returns 200."""
        # Unpack the mock service fixture
        mock_service_class, mock_service_instance = mock_salary_service
        mock_service_instance.get_by_id.return_value = expected_response

        # Act
        response = test_client.get("/salaries/1")

        # Assert
        assert response.status_code == 200
        
        # Verify service was called correctly
        mock_service_class.assert_called_once_with(session=mock_session_async)
        mock_service_instance.get_by_id.assert_called_once_with(1)

    def test_get_salary_by_id_not_found(self, test_client, mock_session_async, mock_salary_service):
        """Integration test: Get non-existent salary returns 404."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_salary_service
        mock_service_instance.get_by_id.return_value = None

        # Act
        response = test_client.get("/salaries/999")

        # Assert
        assert response.status_code == 404        
        mock_service_instance.get_by_id.assert_called_once_with(999)

    def test_get_all_salary_success(self, test_client, mock_session_async, mock_salary_service, multiple_salaries):
        """Integration test: Get all salary returns 200 with pagination."""
        # Arrange
        paginated_response = PaginatedResponse[SalaryResponse](
            items=multiple_salaries,
            page=1,
            size=10,
            total=len(multiple_salaries)
        )

        # Unpack the mock service fixture
        _, mock_service_instance = mock_salary_service
        mock_service_instance.get_all.return_value = paginated_response

        # Act
        response = test_client.get("/salaries/?page=1&size=10")

        # Assert
        assert response.status_code == 200
        mock_service_instance.get_all.assert_called_once()

    def test_search_salaries_success(self, test_client, mock_session_async, mock_salary_service, multiple_salaries):
        """Integration test: Search salary returns 200."""
        # Arrange
        search_filters = SalaryFilter().model_dump(exclude_unset=True)
        
        paginated_response = PaginatedResponse[SalaryResponse](
            items=multiple_salaries,
            page=1,
            size=10,
            total=1
        )

        # Unpack the mock service fixture
        _, mock_service_instance = mock_salary_service
        mock_service_instance.search.return_value = paginated_response

        # Act
        response = test_client.post("/salaries/search?page=1&size=10", json=search_filters)

        # Assert
        assert response.status_code == 200
        mock_service_instance.search.assert_called_once()

    def test_update_salary_success(self, test_client, updated_salary, mock_salary_service, updated_salary_model):
        """Integration test: Update salary returns 200."""
        # Arrange
        update_data = updated_salary.model_dump(exclude_unset=True, mode='json')
        
        updated_response = SalaryResponse.model_validate(updated_salary_model)

        # Unpack the mock service fixture
        _, mock_service_instance = mock_salary_service
        mock_service_instance.update_by_id.return_value = updated_response

        # Act
        response = test_client.put("/salaries/1", json=update_data)

        # Assert
        assert response.status_code == 200        
        mock_service_instance.update_by_id.assert_called_once_with(1, SalaryUpdate(**update_data))

    def test_update_salary_no_fields(self, test_client):
        """Integration test: Update with no fields returns 400."""
        # Act - Empty update payload
        response = test_client.put("/salaries/1", json={})

        # Assert
        assert response.status_code == 400

    def test_update_salary_not_found(self, test_client, mock_session_async, mock_salary_service, updated_salary):
        """Integration test: Update non-existent salary returns 404."""
        # Arrange
        update_data = updated_salary.model_dump(exclude_unset=True, mode='json')

        # Unpack the mock service fixture
        _, mock_service_instance = mock_salary_service
        mock_service_instance.update_by_id.return_value = None

        # Act
        response = test_client.put("/salaries/999", json=update_data)

        # Assert
        assert response.status_code == 404

    def test_delete_salary_success(self, test_client, mock_session_async, mock_salary_service):
        """Integration test: Delete salary returns 200."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_salary_service
        mock_service_instance.delete_by_id.return_value = True

        # Act
        response = test_client.delete("/salaries/1")

        # Assert
        assert response.status_code == 200

        mock_service_instance.delete_by_id.assert_called_once_with(1)

    def test_delete_salary_not_found(self, test_client, mock_session_async, mock_salary_service):
        """Integration test: Delete non-existent salary returns 404."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_salary_service
        mock_service_instance.delete_by_id.return_value = False

        # Act
        response = test_client.delete("/salaries/999")

        # Assert
        assert response.status_code == 404
