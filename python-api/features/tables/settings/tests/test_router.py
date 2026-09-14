# ROSETIC:crud-guid


"""
Unit tests for the Settings API router endpoints.
"""
import pytest


import datetime

from unittest.mock import AsyncMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient

from core.database import get_db
from core.pagination import PaginatedResponse, PaginatedResponse
from features.tables.settings.schemas import SettingResponse, SettingCreate, SettingUpdate, SettingFilter
from features.tables.settings import router as settings_router

class TestSettingRouter:
    """Test cases for Setting API router endpoints."""

    @pytest.fixture
    def app(self):
        """Create FastAPI app with settings router for testing."""
        app = FastAPI()
        app.include_router(settings_router.router)
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
    def expected_response(self, existing_setting):
        return SettingResponse.model_validate(existing_setting)

    @pytest.fixture
    def mock_setting_service(self):
        """Mock SettingService for cleaner testing."""
        with patch.object(settings_router, 'SettingService') as mock_service_class:
            mock_service_instance = AsyncMock()
            mock_service_class.return_value = mock_service_instance
            yield mock_service_class, mock_service_instance

    # ─── Integration Tests with Mocked Service ──────────────────────────────────
    def test_create_setting_integration_success(self, test_client, mock_session_async, expected_response, mock_setting_service, sample_data):
        """Integration test: Create setting endpoint returns 200 with mocked service."""
        # Arrange
        mock_service_class, mock_service_instance = mock_setting_service
        mock_service_instance.create.return_value = expected_response

        # Act
        create_data = SettingCreate(**sample_data).model_dump(mode='json')
        response = test_client.post("/settings/", json=create_data)

        # Assert
        assert response.status_code == 201           
        # Verify service was called correctly
        mock_service_class.assert_called_once_with(session=mock_session_async)
        mock_service_instance.create.assert_called_once()

    def test_create_setting_integration_validation_error(self, test_client, expected_response):
        """Integration test: Create setting with invalid data returns 422."""
        # Arrange
        invalid_request_data = {
            "setting_key": 123,
            "setting_value": None,
            "updated_at": None,
        }

        # Act - Should get validation error before service is called
        response = test_client.post("/settings/", json=invalid_request_data)

        # Assert
        assert response.status_code == 422  # FastAPI validation error
        response_data = response.json()
        assert "detail" in response_data

            

    def test_get_setting_by_id_success(self, test_client, mock_session_async, expected_response, mock_setting_service):
        """Integration test: Get setting by id returns 200."""
        # Unpack the mock service fixture
        mock_service_class, mock_service_instance = mock_setting_service
        mock_service_instance.get_by_id.return_value = expected_response

        # Act
        response = test_client.get("/settings/1")

        # Assert
        assert response.status_code == 200
        
        # Verify service was called correctly
        mock_service_class.assert_called_once_with(session=mock_session_async)
        mock_service_instance.get_by_id.assert_called_once_with(1)

    def test_get_setting_by_id_not_found(self, test_client, mock_session_async, mock_setting_service):
        """Integration test: Get non-existent setting returns 404."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_setting_service
        mock_service_instance.get_by_id.return_value = None

        # Act
        response = test_client.get("/settings/999")

        # Assert
        assert response.status_code == 404        
        mock_service_instance.get_by_id.assert_called_once_with(999)

    def test_get_all_setting_success(self, test_client, mock_session_async, mock_setting_service, multiple_settings):
        """Integration test: Get all setting returns 200 with pagination."""
        # Arrange
        paginated_response = PaginatedResponse[SettingResponse](
            items=multiple_settings,
            page=1,
            size=10,
            total=len(multiple_settings)
        )

        # Unpack the mock service fixture
        _, mock_service_instance = mock_setting_service
        mock_service_instance.get_all.return_value = paginated_response

        # Act
        response = test_client.get("/settings/?page=1&size=10")

        # Assert
        assert response.status_code == 200
        mock_service_instance.get_all.assert_called_once()

    def test_search_settings_success(self, test_client, mock_session_async, mock_setting_service, multiple_settings):
        """Integration test: Search setting returns 200."""
        # Arrange
        search_filters = SettingFilter().model_dump(exclude_unset=True)
        
        paginated_response = PaginatedResponse[SettingResponse](
            items=multiple_settings,
            page=1,
            size=10,
            total=1
        )

        # Unpack the mock service fixture
        _, mock_service_instance = mock_setting_service
        mock_service_instance.search.return_value = paginated_response

        # Act
        response = test_client.post("/settings/search?page=1&size=10", json=search_filters)

        # Assert
        assert response.status_code == 200
        mock_service_instance.search.assert_called_once()

    def test_update_setting_success(self, test_client, updated_setting, mock_setting_service, updated_setting_model):
        """Integration test: Update setting returns 200."""
        # Arrange
        update_data = updated_setting.model_dump(exclude_unset=True, mode='json')
        
        updated_response = SettingResponse.model_validate(updated_setting_model)

        # Unpack the mock service fixture
        _, mock_service_instance = mock_setting_service
        mock_service_instance.update_by_id.return_value = updated_response

        # Act
        response = test_client.put("/settings/1", json=update_data)

        # Assert
        assert response.status_code == 200        
        mock_service_instance.update_by_id.assert_called_once_with(1, SettingUpdate(**update_data))

    def test_update_setting_no_fields(self, test_client):
        """Integration test: Update with no fields returns 400."""
        # Act - Empty update payload
        response = test_client.put("/settings/1", json={})

        # Assert
        assert response.status_code == 400

    def test_update_setting_not_found(self, test_client, mock_session_async, mock_setting_service, updated_setting):
        """Integration test: Update non-existent setting returns 404."""
        # Arrange
        update_data = updated_setting.model_dump(exclude_unset=True, mode='json')

        # Unpack the mock service fixture
        _, mock_service_instance = mock_setting_service
        mock_service_instance.update_by_id.return_value = None

        # Act
        response = test_client.put("/settings/999", json=update_data)

        # Assert
        assert response.status_code == 404

    def test_delete_setting_success(self, test_client, mock_session_async, mock_setting_service):
        """Integration test: Delete setting returns 200."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_setting_service
        mock_service_instance.delete_by_id.return_value = True

        # Act
        response = test_client.delete("/settings/1")

        # Assert
        assert response.status_code == 200

        mock_service_instance.delete_by_id.assert_called_once_with(1)

    def test_delete_setting_not_found(self, test_client, mock_session_async, mock_setting_service):
        """Integration test: Delete non-existent setting returns 404."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_setting_service
        mock_service_instance.delete_by_id.return_value = False

        # Act
        response = test_client.delete("/settings/999")

        # Assert
        assert response.status_code == 404
