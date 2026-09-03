# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c


"""
Unit tests for the Audit_log API router endpoints.
"""
import pytest


import datetime

from unittest.mock import AsyncMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient

from core.database import get_db
from core.pagination import PaginatedResponse, PaginatedResponse
from features.tables.audit_log.schemas import AuditLogResponse, AuditLogCreate, AuditLogUpdate, AuditLogFilter
from features.tables.audit_log import router as audit_log_router

class TestAuditLogRouter:
    """Test cases for AuditLog API router endpoints."""

    @pytest.fixture
    def app(self):
        """Create FastAPI app with audit_log router for testing."""
        app = FastAPI()
        app.include_router(audit_log_router.router)
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
    def expected_response(self, existing_audit_log):
        return AuditLogResponse.model_validate(existing_audit_log)

    @pytest.fixture
    def mock_audit_log_service(self):
        """Mock AuditLogService for cleaner testing."""
        with patch.object(audit_log_router, 'AuditLogService') as mock_service_class:
            mock_service_instance = AsyncMock()
            mock_service_class.return_value = mock_service_instance
            yield mock_service_class, mock_service_instance

    # ─── Integration Tests with Mocked Service ──────────────────────────────────
    def test_create_audit_log_integration_success(self, test_client, mock_session_async, expected_response, mock_audit_log_service, sample_data):
        """Integration test: Create audit_log endpoint returns 200 with mocked service."""
        # Arrange
        mock_service_class, mock_service_instance = mock_audit_log_service
        mock_service_instance.create.return_value = expected_response

        # Act
        create_data = AuditLogCreate(**sample_data).model_dump(mode='json')
        response = test_client.post("/audit-log/", json=create_data)

        # Assert
        assert response.status_code == 201           
        # Verify service was called correctly
        mock_service_class.assert_called_once_with(session=mock_session_async)
        mock_service_instance.create.assert_called_once()

    def test_create_audit_log_integration_validation_error(self, test_client, expected_response):
        """Integration test: Create audit_log with invalid data returns 422."""
        # Arrange
        invalid_request_data = {
            "user_id": "string in int field",
            "change_type": 123,
            "changed_data": None,
            "change_timestamp": None,
            "created_at": None,
            "updated_at": None,
        }

        # Act - Should get validation error before service is called
        response = test_client.post("/audit-log/", json=invalid_request_data)

        # Assert
        assert response.status_code == 422  # FastAPI validation error
        response_data = response.json()
        assert "detail" in response_data

            

    def test_get_audit_log_by_id_success(self, test_client, mock_session_async, expected_response, mock_audit_log_service):
        """Integration test: Get audit_log by id returns 200."""
        # Unpack the mock service fixture
        mock_service_class, mock_service_instance = mock_audit_log_service
        mock_service_instance.get_by_id.return_value = expected_response

        # Act
        response = test_client.get("/audit-log/1")

        # Assert
        assert response.status_code == 200
        
        # Verify service was called correctly
        mock_service_class.assert_called_once_with(session=mock_session_async)
        mock_service_instance.get_by_id.assert_called_once_with(1)

    def test_get_audit_log_by_id_not_found(self, test_client, mock_session_async, mock_audit_log_service):
        """Integration test: Get non-existent audit_log returns 404."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_audit_log_service
        mock_service_instance.get_by_id.return_value = None

        # Act
        response = test_client.get("/audit-log/999")

        # Assert
        assert response.status_code == 404        
        mock_service_instance.get_by_id.assert_called_once_with(999)

    def test_get_all_audit_log_success(self, test_client, mock_session_async, mock_audit_log_service, multiple_audit_log):
        """Integration test: Get all audit_log returns 200 with pagination."""
        # Arrange
        paginated_response = PaginatedResponse[AuditLogResponse](
            items=multiple_audit_log,
            page=1,
            size=10,
            total=len(multiple_audit_log)
        )

        # Unpack the mock service fixture
        _, mock_service_instance = mock_audit_log_service
        mock_service_instance.get_all.return_value = paginated_response

        # Act
        response = test_client.get("/audit-log/?page=1&size=10")

        # Assert
        assert response.status_code == 200
        mock_service_instance.get_all.assert_called_once()

    def test_search_audit_log_success(self, test_client, mock_session_async, mock_audit_log_service, multiple_audit_log):
        """Integration test: Search audit_log returns 200."""
        # Arrange
        search_filters = AuditLogFilter().model_dump(exclude_unset=True)
        
        paginated_response = PaginatedResponse[AuditLogResponse](
            items=multiple_audit_log,
            page=1,
            size=10,
            total=1
        )

        # Unpack the mock service fixture
        _, mock_service_instance = mock_audit_log_service
        mock_service_instance.search.return_value = paginated_response

        # Act
        response = test_client.post("/audit-log/search?page=1&size=10", json=search_filters)

        # Assert
        assert response.status_code == 200
        mock_service_instance.search.assert_called_once()

    def test_update_audit_log_success(self, test_client, updated_audit_log, mock_audit_log_service, updated_audit_log_model):
        """Integration test: Update audit_log returns 200."""
        # Arrange
        update_data = updated_audit_log.model_dump(exclude_unset=True, mode='json')
        
        updated_response = AuditLogResponse.model_validate(updated_audit_log_model)

        # Unpack the mock service fixture
        _, mock_service_instance = mock_audit_log_service
        mock_service_instance.update_by_id.return_value = updated_response

        # Act
        response = test_client.put("/audit-log/1", json=update_data)

        # Assert
        assert response.status_code == 200        
        mock_service_instance.update_by_id.assert_called_once_with(1, AuditLogUpdate(**update_data))

    def test_update_audit_log_no_fields(self, test_client):
        """Integration test: Update with no fields returns 400."""
        # Act - Empty update payload
        response = test_client.put("/audit-log/1", json={})

        # Assert
        assert response.status_code == 400

    def test_update_audit_log_not_found(self, test_client, mock_session_async, mock_audit_log_service, updated_audit_log):
        """Integration test: Update non-existent audit_log returns 404."""
        # Arrange
        update_data = updated_audit_log.model_dump(exclude_unset=True, mode='json')

        # Unpack the mock service fixture
        _, mock_service_instance = mock_audit_log_service
        mock_service_instance.update_by_id.return_value = None

        # Act
        response = test_client.put("/audit-log/999", json=update_data)

        # Assert
        assert response.status_code == 404

    def test_delete_audit_log_success(self, test_client, mock_session_async, mock_audit_log_service):
        """Integration test: Delete audit_log returns 200."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_audit_log_service
        mock_service_instance.delete_by_id.return_value = True

        # Act
        response = test_client.delete("/audit-log/1")

        # Assert
        assert response.status_code == 200

        mock_service_instance.delete_by_id.assert_called_once_with(1)

    def test_delete_audit_log_not_found(self, test_client, mock_session_async, mock_audit_log_service):
        """Integration test: Delete non-existent audit_log returns 404."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_audit_log_service
        mock_service_instance.delete_by_id.return_value = False

        # Act
        response = test_client.delete("/audit-log/999")

        # Assert
        assert response.status_code == 404
