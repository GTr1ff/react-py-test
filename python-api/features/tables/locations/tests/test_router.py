# ROSETIC:crud-guid


"""
Unit tests for the Locations API router endpoints.
"""
import pytest




from unittest.mock import AsyncMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient

from core.database import get_db
from core.pagination import PaginatedResponse, PaginatedResponse
from features.tables.locations.schemas import LocationResponse, LocationCreate, LocationUpdate, LocationFilter
from features.tables.locations import router as locations_router

class TestLocationRouter:
    """Test cases for Location API router endpoints."""

    @pytest.fixture
    def app(self):
        """Create FastAPI app with locations router for testing."""
        app = FastAPI()
        app.include_router(locations_router.router)
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
    def expected_response(self, existing_location):
        return LocationResponse.model_validate(existing_location)

    @pytest.fixture
    def mock_location_service(self):
        """Mock LocationService for cleaner testing."""
        with patch.object(locations_router, 'LocationService') as mock_service_class:
            mock_service_instance = AsyncMock()
            mock_service_class.return_value = mock_service_instance
            yield mock_service_class, mock_service_instance

    # ─── Integration Tests with Mocked Service ──────────────────────────────────
    def test_create_location_integration_success(self, test_client, mock_session_async, expected_response, mock_location_service, sample_data):
        """Integration test: Create location endpoint returns 200 with mocked service."""
        # Arrange
        mock_service_class, mock_service_instance = mock_location_service
        mock_service_instance.create.return_value = expected_response

        # Act
        create_data = LocationCreate(**sample_data).model_dump(mode='json')
        response = test_client.post("/locations/", json=create_data)

        # Assert
        assert response.status_code == 201           
        # Verify service was called correctly
        mock_service_class.assert_called_once_with(session=mock_session_async)
        mock_service_instance.create.assert_called_once()

    def test_create_location_integration_validation_error(self, test_client, expected_response):
        """Integration test: Create location with invalid data returns 422."""
        # Arrange
        invalid_request_data = {
            "address_line_1": 123,
            "address_line_2": 123,
            "city": 123,
            "country": 123,
            "location_name": 123,
            "state": 123,
            "zip_code": 123,
        }

        # Act - Should get validation error before service is called
        response = test_client.post("/locations/", json=invalid_request_data)

        # Assert
        assert response.status_code == 422  # FastAPI validation error
        response_data = response.json()
        assert "detail" in response_data

            

    def test_get_location_by_id_success(self, test_client, mock_session_async, expected_response, mock_location_service):
        """Integration test: Get location by id returns 200."""
        # Unpack the mock service fixture
        mock_service_class, mock_service_instance = mock_location_service
        mock_service_instance.get_by_id.return_value = expected_response

        # Act
        response = test_client.get("/locations/1")

        # Assert
        assert response.status_code == 200
        
        # Verify service was called correctly
        mock_service_class.assert_called_once_with(session=mock_session_async)
        mock_service_instance.get_by_id.assert_called_once_with(1)

    def test_get_location_by_id_not_found(self, test_client, mock_session_async, mock_location_service):
        """Integration test: Get non-existent location returns 404."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_location_service
        mock_service_instance.get_by_id.return_value = None

        # Act
        response = test_client.get("/locations/999")

        # Assert
        assert response.status_code == 404        
        mock_service_instance.get_by_id.assert_called_once_with(999)

    def test_get_all_location_success(self, test_client, mock_session_async, mock_location_service, multiple_locations):
        """Integration test: Get all location returns 200 with pagination."""
        # Arrange
        paginated_response = PaginatedResponse[LocationResponse](
            items=multiple_locations,
            page=1,
            size=10,
            total=len(multiple_locations)
        )

        # Unpack the mock service fixture
        _, mock_service_instance = mock_location_service
        mock_service_instance.get_all.return_value = paginated_response

        # Act
        response = test_client.get("/locations/?page=1&size=10")

        # Assert
        assert response.status_code == 200
        mock_service_instance.get_all.assert_called_once()

    def test_search_locations_success(self, test_client, mock_session_async, mock_location_service, multiple_locations):
        """Integration test: Search location returns 200."""
        # Arrange
        search_filters = LocationFilter().model_dump(exclude_unset=True)
        
        paginated_response = PaginatedResponse[LocationResponse](
            items=multiple_locations,
            page=1,
            size=10,
            total=1
        )

        # Unpack the mock service fixture
        _, mock_service_instance = mock_location_service
        mock_service_instance.search.return_value = paginated_response

        # Act
        response = test_client.post("/locations/search?page=1&size=10", json=search_filters)

        # Assert
        assert response.status_code == 200
        mock_service_instance.search.assert_called_once()

    def test_update_location_success(self, test_client, updated_location, mock_location_service, updated_location_model):
        """Integration test: Update location returns 200."""
        # Arrange
        update_data = updated_location.model_dump(exclude_unset=True, mode='json')
        
        updated_response = LocationResponse.model_validate(updated_location_model)

        # Unpack the mock service fixture
        _, mock_service_instance = mock_location_service
        mock_service_instance.update_by_id.return_value = updated_response

        # Act
        response = test_client.put("/locations/1", json=update_data)

        # Assert
        assert response.status_code == 200        
        mock_service_instance.update_by_id.assert_called_once_with(1, LocationUpdate(**update_data))

    def test_update_location_no_fields(self, test_client):
        """Integration test: Update with no fields returns 400."""
        # Act - Empty update payload
        response = test_client.put("/locations/1", json={})

        # Assert
        assert response.status_code == 400

    def test_update_location_not_found(self, test_client, mock_session_async, mock_location_service, updated_location):
        """Integration test: Update non-existent location returns 404."""
        # Arrange
        update_data = updated_location.model_dump(exclude_unset=True, mode='json')

        # Unpack the mock service fixture
        _, mock_service_instance = mock_location_service
        mock_service_instance.update_by_id.return_value = None

        # Act
        response = test_client.put("/locations/999", json=update_data)

        # Assert
        assert response.status_code == 404

    def test_delete_location_success(self, test_client, mock_session_async, mock_location_service):
        """Integration test: Delete location returns 200."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_location_service
        mock_service_instance.delete_by_id.return_value = True

        # Act
        response = test_client.delete("/locations/1")

        # Assert
        assert response.status_code == 200

        mock_service_instance.delete_by_id.assert_called_once_with(1)

    def test_delete_location_not_found(self, test_client, mock_session_async, mock_location_service):
        """Integration test: Delete non-existent location returns 404."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_location_service
        mock_service_instance.delete_by_id.return_value = False

        # Act
        response = test_client.delete("/locations/999")

        # Assert
        assert response.status_code == 404
