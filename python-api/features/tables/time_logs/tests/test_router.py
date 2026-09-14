# ROSETIC:crud-guid


"""
Unit tests for the Time_logs API router endpoints.
"""
import pytest


import datetime

from unittest.mock import AsyncMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient

from core.database import get_db
from core.pagination import PaginatedResponse, PaginatedResponse
from features.tables.time_logs.schemas import TimeLogResponse, TimeLogCreate, TimeLogUpdate, TimeLogFilter
from features.tables.time_logs import router as time_logs_router

class TestTimeLogRouter:
    """Test cases for TimeLog API router endpoints."""

    @pytest.fixture
    def app(self):
        """Create FastAPI app with time_logs router for testing."""
        app = FastAPI()
        app.include_router(time_logs_router.router)
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
    def expected_response(self, existing_time_log):
        return TimeLogResponse.model_validate(existing_time_log)

    @pytest.fixture
    def mock_time_log_service(self):
        """Mock TimeLogService for cleaner testing."""
        with patch.object(time_logs_router, 'TimeLogService') as mock_service_class:
            mock_service_instance = AsyncMock()
            mock_service_class.return_value = mock_service_instance
            yield mock_service_class, mock_service_instance

    # ─── Integration Tests with Mocked Service ──────────────────────────────────
    def test_create_time_log_integration_success(self, test_client, mock_session_async, expected_response, mock_time_log_service, sample_data):
        """Integration test: Create time_log endpoint returns 200 with mocked service."""
        # Arrange
        mock_service_class, mock_service_instance = mock_time_log_service
        mock_service_instance.create.return_value = expected_response

        # Act
        create_data = TimeLogCreate(**sample_data).model_dump(mode='json')
        response = test_client.post("/time-logs/", json=create_data)

        # Assert
        assert response.status_code == 201           
        # Verify service was called correctly
        mock_service_class.assert_called_once_with(session=mock_session_async)
        mock_service_instance.create.assert_called_once()

    def test_create_time_log_integration_validation_error(self, test_client, expected_response):
        """Integration test: Create time_log with invalid data returns 422."""
        # Arrange
        invalid_request_data = {
            "clock_in": None,
            "clock_out": None,
            "employee_id": "string in int field",
            "location": 123,
        }

        # Act - Should get validation error before service is called
        response = test_client.post("/time-logs/", json=invalid_request_data)

        # Assert
        assert response.status_code == 422  # FastAPI validation error
        response_data = response.json()
        assert "detail" in response_data

            

    def test_get_time_log_by_id_success(self, test_client, mock_session_async, expected_response, mock_time_log_service):
        """Integration test: Get time_log by id returns 200."""
        # Unpack the mock service fixture
        mock_service_class, mock_service_instance = mock_time_log_service
        mock_service_instance.get_by_id.return_value = expected_response

        # Act
        response = test_client.get("/time-logs/1")

        # Assert
        assert response.status_code == 200
        
        # Verify service was called correctly
        mock_service_class.assert_called_once_with(session=mock_session_async)
        mock_service_instance.get_by_id.assert_called_once_with(1)

    def test_get_time_log_by_id_not_found(self, test_client, mock_session_async, mock_time_log_service):
        """Integration test: Get non-existent time_log returns 404."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_time_log_service
        mock_service_instance.get_by_id.return_value = None

        # Act
        response = test_client.get("/time-logs/999")

        # Assert
        assert response.status_code == 404        
        mock_service_instance.get_by_id.assert_called_once_with(999)

    def test_get_all_time_log_success(self, test_client, mock_session_async, mock_time_log_service, multiple_time_logs):
        """Integration test: Get all time_log returns 200 with pagination."""
        # Arrange
        paginated_response = PaginatedResponse[TimeLogResponse](
            items=multiple_time_logs,
            page=1,
            size=10,
            total=len(multiple_time_logs)
        )

        # Unpack the mock service fixture
        _, mock_service_instance = mock_time_log_service
        mock_service_instance.get_all.return_value = paginated_response

        # Act
        response = test_client.get("/time-logs/?page=1&size=10")

        # Assert
        assert response.status_code == 200
        mock_service_instance.get_all.assert_called_once()

    def test_search_time_logs_success(self, test_client, mock_session_async, mock_time_log_service, multiple_time_logs):
        """Integration test: Search time_log returns 200."""
        # Arrange
        search_filters = TimeLogFilter().model_dump(exclude_unset=True)
        
        paginated_response = PaginatedResponse[TimeLogResponse](
            items=multiple_time_logs,
            page=1,
            size=10,
            total=1
        )

        # Unpack the mock service fixture
        _, mock_service_instance = mock_time_log_service
        mock_service_instance.search.return_value = paginated_response

        # Act
        response = test_client.post("/time-logs/search?page=1&size=10", json=search_filters)

        # Assert
        assert response.status_code == 200
        mock_service_instance.search.assert_called_once()

    def test_update_time_log_success(self, test_client, updated_time_log, mock_time_log_service, updated_time_log_model):
        """Integration test: Update time_log returns 200."""
        # Arrange
        update_data = updated_time_log.model_dump(exclude_unset=True, mode='json')
        
        updated_response = TimeLogResponse.model_validate(updated_time_log_model)

        # Unpack the mock service fixture
        _, mock_service_instance = mock_time_log_service
        mock_service_instance.update_by_id.return_value = updated_response

        # Act
        response = test_client.put("/time-logs/1", json=update_data)

        # Assert
        assert response.status_code == 200        
        mock_service_instance.update_by_id.assert_called_once_with(1, TimeLogUpdate(**update_data))

    def test_update_time_log_no_fields(self, test_client):
        """Integration test: Update with no fields returns 400."""
        # Act - Empty update payload
        response = test_client.put("/time-logs/1", json={})

        # Assert
        assert response.status_code == 400

    def test_update_time_log_not_found(self, test_client, mock_session_async, mock_time_log_service, updated_time_log):
        """Integration test: Update non-existent time_log returns 404."""
        # Arrange
        update_data = updated_time_log.model_dump(exclude_unset=True, mode='json')

        # Unpack the mock service fixture
        _, mock_service_instance = mock_time_log_service
        mock_service_instance.update_by_id.return_value = None

        # Act
        response = test_client.put("/time-logs/999", json=update_data)

        # Assert
        assert response.status_code == 404

    def test_delete_time_log_success(self, test_client, mock_session_async, mock_time_log_service):
        """Integration test: Delete time_log returns 200."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_time_log_service
        mock_service_instance.delete_by_id.return_value = True

        # Act
        response = test_client.delete("/time-logs/1")

        # Assert
        assert response.status_code == 200

        mock_service_instance.delete_by_id.assert_called_once_with(1)

    def test_delete_time_log_not_found(self, test_client, mock_session_async, mock_time_log_service):
        """Integration test: Delete non-existent time_log returns 404."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_time_log_service
        mock_service_instance.delete_by_id.return_value = False

        # Act
        response = test_client.delete("/time-logs/999")

        # Assert
        assert response.status_code == 404
