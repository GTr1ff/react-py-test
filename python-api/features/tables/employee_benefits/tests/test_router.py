# ROSETIC:crud-guid


"""
Unit tests for the Employee_benefits API router endpoints.
"""
import pytest


import datetime

from unittest.mock import AsyncMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient

from core.database import get_db
from core.pagination import PaginatedResponse, PaginatedResponse
from features.tables.employee_benefits.schemas import EmployeeBenefitResponse, EmployeeBenefitCreate, EmployeeBenefitUpdate, EmployeeBenefitFilter
from features.tables.employee_benefits import router as employee_benefits_router

class TestEmployeeBenefitRouter:
    """Test cases for EmployeeBenefit API router endpoints."""

    @pytest.fixture
    def app(self):
        """Create FastAPI app with employee_benefits router for testing."""
        app = FastAPI()
        app.include_router(employee_benefits_router.router)
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
    def expected_response(self, existing_employee_benefit):
        return EmployeeBenefitResponse.model_validate(existing_employee_benefit)

    @pytest.fixture
    def mock_employee_benefit_service(self):
        """Mock EmployeeBenefitService for cleaner testing."""
        with patch.object(employee_benefits_router, 'EmployeeBenefitService') as mock_service_class:
            mock_service_instance = AsyncMock()
            mock_service_class.return_value = mock_service_instance
            yield mock_service_class, mock_service_instance

    # ─── Integration Tests with Mocked Service ──────────────────────────────────
    def test_create_employee_benefit_integration_success(self, test_client, mock_session_async, expected_response, mock_employee_benefit_service, sample_data):
        """Integration test: Create employee_benefit endpoint returns 200 with mocked service."""
        # Arrange
        mock_service_class, mock_service_instance = mock_employee_benefit_service
        mock_service_instance.create.return_value = expected_response

        # Act
        create_data = EmployeeBenefitCreate(**sample_data).model_dump(mode='json')
        response = test_client.post("/employee-benefits/", json=create_data)

        # Assert
        assert response.status_code == 201           
        # Verify service was called correctly
        mock_service_class.assert_called_once_with(session=mock_session_async)
        mock_service_instance.create.assert_called_once()

    def test_create_employee_benefit_integration_validation_error(self, test_client, expected_response):
        """Integration test: Create employee_benefit with invalid data returns 422."""
        # Arrange
        invalid_request_data = {
            "benefit_id": "string in int field",
            "employee_id": "string in int field",
            "enrollment_date": None,
        }

        # Act - Should get validation error before service is called
        response = test_client.post("/employee-benefits/", json=invalid_request_data)

        # Assert
        assert response.status_code == 422  # FastAPI validation error
        response_data = response.json()
        assert "detail" in response_data

            

    def test_get_employee_benefit_by_id_success(self, test_client, mock_session_async, expected_response, mock_employee_benefit_service):
        """Integration test: Get employee_benefit by id returns 200."""
        # Unpack the mock service fixture
        mock_service_class, mock_service_instance = mock_employee_benefit_service
        mock_service_instance.get_by_id.return_value = expected_response

        # Act
        response = test_client.get("/employee-benefits/1")

        # Assert
        assert response.status_code == 200
        
        # Verify service was called correctly
        mock_service_class.assert_called_once_with(session=mock_session_async)
        mock_service_instance.get_by_id.assert_called_once_with(1)

    def test_get_employee_benefit_by_id_not_found(self, test_client, mock_session_async, mock_employee_benefit_service):
        """Integration test: Get non-existent employee_benefit returns 404."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_employee_benefit_service
        mock_service_instance.get_by_id.return_value = None

        # Act
        response = test_client.get("/employee-benefits/999")

        # Assert
        assert response.status_code == 404        
        mock_service_instance.get_by_id.assert_called_once_with(999)

    def test_get_all_employee_benefit_success(self, test_client, mock_session_async, mock_employee_benefit_service, multiple_employee_benefits):
        """Integration test: Get all employee_benefit returns 200 with pagination."""
        # Arrange
        paginated_response = PaginatedResponse[EmployeeBenefitResponse](
            items=multiple_employee_benefits,
            page=1,
            size=10,
            total=len(multiple_employee_benefits)
        )

        # Unpack the mock service fixture
        _, mock_service_instance = mock_employee_benefit_service
        mock_service_instance.get_all.return_value = paginated_response

        # Act
        response = test_client.get("/employee-benefits/?page=1&size=10")

        # Assert
        assert response.status_code == 200
        mock_service_instance.get_all.assert_called_once()

    def test_search_employee_benefits_success(self, test_client, mock_session_async, mock_employee_benefit_service, multiple_employee_benefits):
        """Integration test: Search employee_benefit returns 200."""
        # Arrange
        search_filters = EmployeeBenefitFilter().model_dump(exclude_unset=True)
        
        paginated_response = PaginatedResponse[EmployeeBenefitResponse](
            items=multiple_employee_benefits,
            page=1,
            size=10,
            total=1
        )

        # Unpack the mock service fixture
        _, mock_service_instance = mock_employee_benefit_service
        mock_service_instance.search.return_value = paginated_response

        # Act
        response = test_client.post("/employee-benefits/search?page=1&size=10", json=search_filters)

        # Assert
        assert response.status_code == 200
        mock_service_instance.search.assert_called_once()

    def test_update_employee_benefit_success(self, test_client, updated_employee_benefit, mock_employee_benefit_service, updated_employee_benefit_model):
        """Integration test: Update employee_benefit returns 200."""
        # Arrange
        update_data = updated_employee_benefit.model_dump(exclude_unset=True, mode='json')
        
        updated_response = EmployeeBenefitResponse.model_validate(updated_employee_benefit_model)

        # Unpack the mock service fixture
        _, mock_service_instance = mock_employee_benefit_service
        mock_service_instance.update_by_id.return_value = updated_response

        # Act
        response = test_client.put("/employee-benefits/1", json=update_data)

        # Assert
        assert response.status_code == 200        
        mock_service_instance.update_by_id.assert_called_once_with(1, EmployeeBenefitUpdate(**update_data))

    def test_update_employee_benefit_no_fields(self, test_client):
        """Integration test: Update with no fields returns 400."""
        # Act - Empty update payload
        response = test_client.put("/employee-benefits/1", json={})

        # Assert
        assert response.status_code == 400

    def test_update_employee_benefit_not_found(self, test_client, mock_session_async, mock_employee_benefit_service, updated_employee_benefit):
        """Integration test: Update non-existent employee_benefit returns 404."""
        # Arrange
        update_data = updated_employee_benefit.model_dump(exclude_unset=True, mode='json')

        # Unpack the mock service fixture
        _, mock_service_instance = mock_employee_benefit_service
        mock_service_instance.update_by_id.return_value = None

        # Act
        response = test_client.put("/employee-benefits/999", json=update_data)

        # Assert
        assert response.status_code == 404

    def test_delete_employee_benefit_success(self, test_client, mock_session_async, mock_employee_benefit_service):
        """Integration test: Delete employee_benefit returns 200."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_employee_benefit_service
        mock_service_instance.delete_by_id.return_value = True

        # Act
        response = test_client.delete("/employee-benefits/1")

        # Assert
        assert response.status_code == 200

        mock_service_instance.delete_by_id.assert_called_once_with(1)

    def test_delete_employee_benefit_not_found(self, test_client, mock_session_async, mock_employee_benefit_service):
        """Integration test: Delete non-existent employee_benefit returns 404."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_employee_benefit_service
        mock_service_instance.delete_by_id.return_value = False

        # Act
        response = test_client.delete("/employee-benefits/999")

        # Assert
        assert response.status_code == 404
