# ROSETIC:crud-guid


"""
Unit tests for the Holiday_calendar API router endpoints.
"""
import pytest


import datetime

from unittest.mock import AsyncMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient

from core.database import get_db
from core.pagination import PaginatedResponse, PaginatedResponse
from features.tables.holiday_calendar.schemas import HolidayCalendarResponse, HolidayCalendarCreate, HolidayCalendarUpdate, HolidayCalendarFilter
from features.tables.holiday_calendar import router as holiday_calendar_router

class TestHolidayCalendarRouter:
    """Test cases for HolidayCalendar API router endpoints."""

    @pytest.fixture
    def app(self):
        """Create FastAPI app with holiday_calendar router for testing."""
        app = FastAPI()
        app.include_router(holiday_calendar_router.router)
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
    def expected_response(self, existing_holiday_calendar):
        return HolidayCalendarResponse.model_validate(existing_holiday_calendar)

    @pytest.fixture
    def mock_holiday_calendar_service(self):
        """Mock HolidayCalendarService for cleaner testing."""
        with patch.object(holiday_calendar_router, 'HolidayCalendarService') as mock_service_class:
            mock_service_instance = AsyncMock()
            mock_service_class.return_value = mock_service_instance
            yield mock_service_class, mock_service_instance

    # ─── Integration Tests with Mocked Service ──────────────────────────────────
    def test_create_holiday_calendar_integration_success(self, test_client, mock_session_async, expected_response, mock_holiday_calendar_service, sample_data):
        """Integration test: Create holiday_calendar endpoint returns 200 with mocked service."""
        # Arrange
        mock_service_class, mock_service_instance = mock_holiday_calendar_service
        mock_service_instance.create.return_value = expected_response

        # Act
        create_data = HolidayCalendarCreate(**sample_data).model_dump(mode='json')
        response = test_client.post("/holiday-calendar/", json=create_data)

        # Assert
        assert response.status_code == 201           
        # Verify service was called correctly
        mock_service_class.assert_called_once_with(session=mock_session_async)
        mock_service_instance.create.assert_called_once()

    def test_create_holiday_calendar_integration_validation_error(self, test_client, expected_response):
        """Integration test: Create holiday_calendar with invalid data returns 422."""
        # Arrange
        invalid_request_data = {
            "holiday_date": None,
            "holiday_name": 123,
            "is_national": "string in bool field",
        }

        # Act - Should get validation error before service is called
        response = test_client.post("/holiday-calendar/", json=invalid_request_data)

        # Assert
        assert response.status_code == 422  # FastAPI validation error
        response_data = response.json()
        assert "detail" in response_data

            

    def test_get_holiday_calendar_by_id_success(self, test_client, mock_session_async, expected_response, mock_holiday_calendar_service):
        """Integration test: Get holiday_calendar by id returns 200."""
        # Unpack the mock service fixture
        mock_service_class, mock_service_instance = mock_holiday_calendar_service
        mock_service_instance.get_by_id.return_value = expected_response

        # Act
        response = test_client.get("/holiday-calendar/1")

        # Assert
        assert response.status_code == 200
        
        # Verify service was called correctly
        mock_service_class.assert_called_once_with(session=mock_session_async)
        mock_service_instance.get_by_id.assert_called_once_with(1)

    def test_get_holiday_calendar_by_id_not_found(self, test_client, mock_session_async, mock_holiday_calendar_service):
        """Integration test: Get non-existent holiday_calendar returns 404."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_holiday_calendar_service
        mock_service_instance.get_by_id.return_value = None

        # Act
        response = test_client.get("/holiday-calendar/999")

        # Assert
        assert response.status_code == 404        
        mock_service_instance.get_by_id.assert_called_once_with(999)

    def test_get_all_holiday_calendar_success(self, test_client, mock_session_async, mock_holiday_calendar_service, multiple_holiday_calendar):
        """Integration test: Get all holiday_calendar returns 200 with pagination."""
        # Arrange
        paginated_response = PaginatedResponse[HolidayCalendarResponse](
            items=multiple_holiday_calendar,
            page=1,
            size=10,
            total=len(multiple_holiday_calendar)
        )

        # Unpack the mock service fixture
        _, mock_service_instance = mock_holiday_calendar_service
        mock_service_instance.get_all.return_value = paginated_response

        # Act
        response = test_client.get("/holiday-calendar/?page=1&size=10")

        # Assert
        assert response.status_code == 200
        mock_service_instance.get_all.assert_called_once()

    def test_search_holiday_calendar_success(self, test_client, mock_session_async, mock_holiday_calendar_service, multiple_holiday_calendar):
        """Integration test: Search holiday_calendar returns 200."""
        # Arrange
        search_filters = HolidayCalendarFilter().model_dump(exclude_unset=True)
        
        paginated_response = PaginatedResponse[HolidayCalendarResponse](
            items=multiple_holiday_calendar,
            page=1,
            size=10,
            total=1
        )

        # Unpack the mock service fixture
        _, mock_service_instance = mock_holiday_calendar_service
        mock_service_instance.search.return_value = paginated_response

        # Act
        response = test_client.post("/holiday-calendar/search?page=1&size=10", json=search_filters)

        # Assert
        assert response.status_code == 200
        mock_service_instance.search.assert_called_once()

    def test_update_holiday_calendar_success(self, test_client, updated_holiday_calendar, mock_holiday_calendar_service, updated_holiday_calendar_model):
        """Integration test: Update holiday_calendar returns 200."""
        # Arrange
        update_data = updated_holiday_calendar.model_dump(exclude_unset=True, mode='json')
        
        updated_response = HolidayCalendarResponse.model_validate(updated_holiday_calendar_model)

        # Unpack the mock service fixture
        _, mock_service_instance = mock_holiday_calendar_service
        mock_service_instance.update_by_id.return_value = updated_response

        # Act
        response = test_client.put("/holiday-calendar/1", json=update_data)

        # Assert
        assert response.status_code == 200        
        mock_service_instance.update_by_id.assert_called_once_with(1, HolidayCalendarUpdate(**update_data))

    def test_update_holiday_calendar_no_fields(self, test_client):
        """Integration test: Update with no fields returns 400."""
        # Act - Empty update payload
        response = test_client.put("/holiday-calendar/1", json={})

        # Assert
        assert response.status_code == 400

    def test_update_holiday_calendar_not_found(self, test_client, mock_session_async, mock_holiday_calendar_service, updated_holiday_calendar):
        """Integration test: Update non-existent holiday_calendar returns 404."""
        # Arrange
        update_data = updated_holiday_calendar.model_dump(exclude_unset=True, mode='json')

        # Unpack the mock service fixture
        _, mock_service_instance = mock_holiday_calendar_service
        mock_service_instance.update_by_id.return_value = None

        # Act
        response = test_client.put("/holiday-calendar/999", json=update_data)

        # Assert
        assert response.status_code == 404

    def test_delete_holiday_calendar_success(self, test_client, mock_session_async, mock_holiday_calendar_service):
        """Integration test: Delete holiday_calendar returns 200."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_holiday_calendar_service
        mock_service_instance.delete_by_id.return_value = True

        # Act
        response = test_client.delete("/holiday-calendar/1")

        # Assert
        assert response.status_code == 200

        mock_service_instance.delete_by_id.assert_called_once_with(1)

    def test_delete_holiday_calendar_not_found(self, test_client, mock_session_async, mock_holiday_calendar_service):
        """Integration test: Delete non-existent holiday_calendar returns 404."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_holiday_calendar_service
        mock_service_instance.delete_by_id.return_value = False

        # Act
        response = test_client.delete("/holiday-calendar/999")

        # Assert
        assert response.status_code == 404
