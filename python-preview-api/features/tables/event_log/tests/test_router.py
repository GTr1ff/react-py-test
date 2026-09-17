# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c


"""
Unit tests for the Event_log API router endpoints.
"""
import pytest


import datetime

from unittest.mock import AsyncMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient

from core.database import get_db
from core.pagination import PaginatedResponse, PaginatedResponse
from features.tables.event_log.schemas import EventLogResponse, EventLogCreate, EventLogUpdate, EventLogFilter
from features.tables.event_log import router as event_log_router

class TestEventLogRouter:
    """Test cases for EventLog API router endpoints."""

    @pytest.fixture
    def app(self):
        """Create FastAPI app with event_log router for testing."""
        app = FastAPI()
        app.include_router(event_log_router.router)
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
    def expected_response(self, existing_event_log):
        return EventLogResponse.model_validate(existing_event_log)

    @pytest.fixture
    def mock_event_log_service(self):
        """Mock EventLogService for cleaner testing."""
        with patch.object(event_log_router, 'EventLogService') as mock_service_class:
            mock_service_instance = AsyncMock()
            mock_service_class.return_value = mock_service_instance
            yield mock_service_class, mock_service_instance

    # ─── Integration Tests with Mocked Service ──────────────────────────────────
    def test_create_event_log_integration_success(self, test_client, mock_session_async, expected_response, mock_event_log_service, sample_data):
        """Integration test: Create event_log endpoint returns 200 with mocked service."""
        # Arrange
        mock_service_class, mock_service_instance = mock_event_log_service
        mock_service_instance.create.return_value = expected_response

        # Act
        create_data = EventLogCreate(**sample_data).model_dump(mode='json')
        response = test_client.post("/event-log/", json=create_data)

        # Assert
        assert response.status_code == 201           
        # Verify service was called correctly
        mock_service_class.assert_called_once_with(session=mock_session_async)
        mock_service_instance.create.assert_called_once()

    def test_create_event_log_integration_validation_error(self, test_client, expected_response):
        """Integration test: Create event_log with invalid data returns 422."""
        # Arrange
        invalid_request_data = {
            "user_id": "string in int field",
            "event_type": 123,
            "event_timestamp": None,
            "event_data": None,
            "created_at": None,
            "updated_at": None,
        }

        # Act - Should get validation error before service is called
        response = test_client.post("/event-log/", json=invalid_request_data)

        # Assert
        assert response.status_code == 422  # FastAPI validation error
        response_data = response.json()
        assert "detail" in response_data

            

    def test_get_event_log_by_id_success(self, test_client, mock_session_async, expected_response, mock_event_log_service):
        """Integration test: Get event_log by id returns 200."""
        # Unpack the mock service fixture
        mock_service_class, mock_service_instance = mock_event_log_service
        mock_service_instance.get_by_id.return_value = expected_response

        # Act
        response = test_client.get("/event-log/1")

        # Assert
        assert response.status_code == 200
        
        # Verify service was called correctly
        mock_service_class.assert_called_once_with(session=mock_session_async)
        mock_service_instance.get_by_id.assert_called_once_with(1)

    def test_get_event_log_by_id_not_found(self, test_client, mock_session_async, mock_event_log_service):
        """Integration test: Get non-existent event_log returns 404."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_event_log_service
        mock_service_instance.get_by_id.return_value = None

        # Act
        response = test_client.get("/event-log/999")

        # Assert
        assert response.status_code == 404        
        mock_service_instance.get_by_id.assert_called_once_with(999)

    def test_get_all_event_log_success(self, test_client, mock_session_async, mock_event_log_service, multiple_event_log):
        """Integration test: Get all event_log returns 200 with pagination."""
        # Arrange
        paginated_response = PaginatedResponse[EventLogResponse](
            items=multiple_event_log,
            page=1,
            size=10,
            total=len(multiple_event_log)
        )

        # Unpack the mock service fixture
        _, mock_service_instance = mock_event_log_service
        mock_service_instance.get_all.return_value = paginated_response

        # Act
        response = test_client.get("/event-log/?page=1&size=10")

        # Assert
        assert response.status_code == 200
        mock_service_instance.get_all.assert_called_once()

    def test_search_event_log_success(self, test_client, mock_session_async, mock_event_log_service, multiple_event_log):
        """Integration test: Search event_log returns 200."""
        # Arrange
        search_filters = EventLogFilter().model_dump(exclude_unset=True)
        
        paginated_response = PaginatedResponse[EventLogResponse](
            items=multiple_event_log,
            page=1,
            size=10,
            total=1
        )

        # Unpack the mock service fixture
        _, mock_service_instance = mock_event_log_service
        mock_service_instance.search.return_value = paginated_response

        # Act
        response = test_client.post("/event-log/search?page=1&size=10", json=search_filters)

        # Assert
        assert response.status_code == 200
        mock_service_instance.search.assert_called_once()

    def test_update_event_log_success(self, test_client, updated_event_log, mock_event_log_service, updated_event_log_model):
        """Integration test: Update event_log returns 200."""
        # Arrange
        update_data = updated_event_log.model_dump(exclude_unset=True, mode='json')
        
        updated_response = EventLogResponse.model_validate(updated_event_log_model)

        # Unpack the mock service fixture
        _, mock_service_instance = mock_event_log_service
        mock_service_instance.update_by_id.return_value = updated_response

        # Act
        response = test_client.put("/event-log/1", json=update_data)

        # Assert
        assert response.status_code == 200        
        mock_service_instance.update_by_id.assert_called_once_with(1, EventLogUpdate(**update_data))

    def test_update_event_log_no_fields(self, test_client):
        """Integration test: Update with no fields returns 400."""
        # Act - Empty update payload
        response = test_client.put("/event-log/1", json={})

        # Assert
        assert response.status_code == 400

    def test_update_event_log_not_found(self, test_client, mock_session_async, mock_event_log_service, updated_event_log):
        """Integration test: Update non-existent event_log returns 404."""
        # Arrange
        update_data = updated_event_log.model_dump(exclude_unset=True, mode='json')

        # Unpack the mock service fixture
        _, mock_service_instance = mock_event_log_service
        mock_service_instance.update_by_id.return_value = None

        # Act
        response = test_client.put("/event-log/999", json=update_data)

        # Assert
        assert response.status_code == 404

    def test_delete_event_log_success(self, test_client, mock_session_async, mock_event_log_service):
        """Integration test: Delete event_log returns 200."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_event_log_service
        mock_service_instance.delete_by_id.return_value = True

        # Act
        response = test_client.delete("/event-log/1")

        # Assert
        assert response.status_code == 200

        mock_service_instance.delete_by_id.assert_called_once_with(1)

    def test_delete_event_log_not_found(self, test_client, mock_session_async, mock_event_log_service):
        """Integration test: Delete non-existent event_log returns 404."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_event_log_service
        mock_service_instance.delete_by_id.return_value = False

        # Act
        response = test_client.delete("/event-log/999")

        # Assert
        assert response.status_code == 404
