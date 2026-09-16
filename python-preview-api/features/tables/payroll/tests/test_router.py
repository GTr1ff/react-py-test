# ROSETIC:crud-guid


"""
Unit tests for the Payroll API router endpoints.
"""
import pytest


import datetime
from decimal import Decimal
from unittest.mock import AsyncMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient

from core.database import get_db
from core.pagination import PaginatedResponse, PaginatedResponse
from features.tables.payroll.schemas import PayrollResponse, PayrollCreate, PayrollUpdate, PayrollFilter
from features.tables.payroll import router as payroll_router

class TestPayrollRouter:
    """Test cases for Payroll API router endpoints."""

    @pytest.fixture
    def app(self):
        """Create FastAPI app with payroll router for testing."""
        app = FastAPI()
        app.include_router(payroll_router.router)
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
    def expected_response(self, existing_payroll):
        return PayrollResponse.model_validate(existing_payroll)

    @pytest.fixture
    def mock_payroll_service(self):
        """Mock PayrollService for cleaner testing."""
        with patch.object(payroll_router, 'PayrollService') as mock_service_class:
            mock_service_instance = AsyncMock()
            mock_service_class.return_value = mock_service_instance
            yield mock_service_class, mock_service_instance

    # ─── Integration Tests with Mocked Service ──────────────────────────────────
    def test_create_payroll_integration_success(self, test_client, mock_session_async, expected_response, mock_payroll_service, sample_data):
        """Integration test: Create payroll endpoint returns 200 with mocked service."""
        # Arrange
        mock_service_class, mock_service_instance = mock_payroll_service
        mock_service_instance.create.return_value = expected_response

        # Act
        create_data = PayrollCreate(**sample_data).model_dump(mode='json')
        response = test_client.post("/payroll/", json=create_data)

        # Assert
        assert response.status_code == 201           
        # Verify service was called correctly
        mock_service_class.assert_called_once_with(session=mock_session_async)
        mock_service_instance.create.assert_called_once()

    def test_create_payroll_integration_validation_error(self, test_client, expected_response):
        """Integration test: Create payroll with invalid data returns 422."""
        # Arrange
        invalid_request_data = {
            "employee_id": "string in int field",
            "hours_worked": "string in int field",
            "pay_period_end": None,
            "pay_period_start": None,
            "wages": "string in int field",
        }

        # Act - Should get validation error before service is called
        response = test_client.post("/payroll/", json=invalid_request_data)

        # Assert
        assert response.status_code == 422  # FastAPI validation error
        response_data = response.json()
        assert "detail" in response_data

            

    def test_get_payroll_by_id_success(self, test_client, mock_session_async, expected_response, mock_payroll_service):
        """Integration test: Get payroll by id returns 200."""
        # Unpack the mock service fixture
        mock_service_class, mock_service_instance = mock_payroll_service
        mock_service_instance.get_by_id.return_value = expected_response

        # Act
        response = test_client.get("/payroll/1")

        # Assert
        assert response.status_code == 200
        
        # Verify service was called correctly
        mock_service_class.assert_called_once_with(session=mock_session_async)
        mock_service_instance.get_by_id.assert_called_once_with(1)

    def test_get_payroll_by_id_not_found(self, test_client, mock_session_async, mock_payroll_service):
        """Integration test: Get non-existent payroll returns 404."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_payroll_service
        mock_service_instance.get_by_id.return_value = None

        # Act
        response = test_client.get("/payroll/999")

        # Assert
        assert response.status_code == 404        
        mock_service_instance.get_by_id.assert_called_once_with(999)

    def test_get_all_payroll_success(self, test_client, mock_session_async, mock_payroll_service, multiple_payroll):
        """Integration test: Get all payroll returns 200 with pagination."""
        # Arrange
        paginated_response = PaginatedResponse[PayrollResponse](
            items=multiple_payroll,
            page=1,
            size=10,
            total=len(multiple_payroll)
        )

        # Unpack the mock service fixture
        _, mock_service_instance = mock_payroll_service
        mock_service_instance.get_all.return_value = paginated_response

        # Act
        response = test_client.get("/payroll/?page=1&size=10")

        # Assert
        assert response.status_code == 200
        mock_service_instance.get_all.assert_called_once()

    def test_search_payroll_success(self, test_client, mock_session_async, mock_payroll_service, multiple_payroll):
        """Integration test: Search payroll returns 200."""
        # Arrange
        search_filters = PayrollFilter().model_dump(exclude_unset=True)
        
        paginated_response = PaginatedResponse[PayrollResponse](
            items=multiple_payroll,
            page=1,
            size=10,
            total=1
        )

        # Unpack the mock service fixture
        _, mock_service_instance = mock_payroll_service
        mock_service_instance.search.return_value = paginated_response

        # Act
        response = test_client.post("/payroll/search?page=1&size=10", json=search_filters)

        # Assert
        assert response.status_code == 200
        mock_service_instance.search.assert_called_once()

    def test_update_payroll_success(self, test_client, updated_payroll, mock_payroll_service, updated_payroll_model):
        """Integration test: Update payroll returns 200."""
        # Arrange
        update_data = updated_payroll.model_dump(exclude_unset=True, mode='json')
        
        updated_response = PayrollResponse.model_validate(updated_payroll_model)

        # Unpack the mock service fixture
        _, mock_service_instance = mock_payroll_service
        mock_service_instance.update_by_id.return_value = updated_response

        # Act
        response = test_client.put("/payroll/1", json=update_data)

        # Assert
        assert response.status_code == 200        
        mock_service_instance.update_by_id.assert_called_once_with(1, PayrollUpdate(**update_data))

    def test_update_payroll_no_fields(self, test_client):
        """Integration test: Update with no fields returns 400."""
        # Act - Empty update payload
        response = test_client.put("/payroll/1", json={})

        # Assert
        assert response.status_code == 400

    def test_update_payroll_not_found(self, test_client, mock_session_async, mock_payroll_service, updated_payroll):
        """Integration test: Update non-existent payroll returns 404."""
        # Arrange
        update_data = updated_payroll.model_dump(exclude_unset=True, mode='json')

        # Unpack the mock service fixture
        _, mock_service_instance = mock_payroll_service
        mock_service_instance.update_by_id.return_value = None

        # Act
        response = test_client.put("/payroll/999", json=update_data)

        # Assert
        assert response.status_code == 404

    def test_delete_payroll_success(self, test_client, mock_session_async, mock_payroll_service):
        """Integration test: Delete payroll returns 200."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_payroll_service
        mock_service_instance.delete_by_id.return_value = True

        # Act
        response = test_client.delete("/payroll/1")

        # Assert
        assert response.status_code == 200

        mock_service_instance.delete_by_id.assert_called_once_with(1)

    def test_delete_payroll_not_found(self, test_client, mock_session_async, mock_payroll_service):
        """Integration test: Delete non-existent payroll returns 404."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_payroll_service
        mock_service_instance.delete_by_id.return_value = False

        # Act
        response = test_client.delete("/payroll/999")

        # Assert
        assert response.status_code == 404
