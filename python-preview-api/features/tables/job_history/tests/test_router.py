# ROSETIC:crud-guid


"""
Unit tests for the Job_history API router endpoints.
"""
import pytest


import datetime

from unittest.mock import AsyncMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient

from core.database import get_db
from core.pagination import PaginatedResponse, PaginatedResponse
from features.tables.job_history.schemas import JobHistoryResponse, JobHistoryCreate, JobHistoryUpdate, JobHistoryFilter
from features.tables.job_history import router as job_history_router

class TestJobHistoryRouter:
    """Test cases for JobHistory API router endpoints."""

    @pytest.fixture
    def app(self):
        """Create FastAPI app with job_history router for testing."""
        app = FastAPI()
        app.include_router(job_history_router.router)
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
    def expected_response(self, existing_job_history):
        return JobHistoryResponse.model_validate(existing_job_history)

    @pytest.fixture
    def mock_job_history_service(self):
        """Mock JobHistoryService for cleaner testing."""
        with patch.object(job_history_router, 'JobHistoryService') as mock_service_class:
            mock_service_instance = AsyncMock()
            mock_service_class.return_value = mock_service_instance
            yield mock_service_class, mock_service_instance

    # ─── Integration Tests with Mocked Service ──────────────────────────────────
    def test_create_job_history_integration_success(self, test_client, mock_session_async, expected_response, mock_job_history_service, sample_data):
        """Integration test: Create job_history endpoint returns 200 with mocked service."""
        # Arrange
        mock_service_class, mock_service_instance = mock_job_history_service
        mock_service_instance.create.return_value = expected_response

        # Act
        create_data = JobHistoryCreate(**sample_data).model_dump(mode='json')
        response = test_client.post("/job-history/", json=create_data)

        # Assert
        assert response.status_code == 201           
        # Verify service was called correctly
        mock_service_class.assert_called_once_with(session=mock_session_async)
        mock_service_instance.create.assert_called_once()

    def test_create_job_history_integration_validation_error(self, test_client, expected_response):
        """Integration test: Create job_history with invalid data returns 422."""
        # Arrange
        invalid_request_data = {
            "employee_id": "string in int field",
            "end_date": None,
            "role_id": "string in int field",
            "start_date": None,
        }

        # Act - Should get validation error before service is called
        response = test_client.post("/job-history/", json=invalid_request_data)

        # Assert
        assert response.status_code == 422  # FastAPI validation error
        response_data = response.json()
        assert "detail" in response_data

            

    def test_get_job_history_by_id_success(self, test_client, mock_session_async, expected_response, mock_job_history_service):
        """Integration test: Get job_history by id returns 200."""
        # Unpack the mock service fixture
        mock_service_class, mock_service_instance = mock_job_history_service
        mock_service_instance.get_by_id.return_value = expected_response

        # Act
        response = test_client.get("/job-history/1")

        # Assert
        assert response.status_code == 200
        
        # Verify service was called correctly
        mock_service_class.assert_called_once_with(session=mock_session_async)
        mock_service_instance.get_by_id.assert_called_once_with(1)

    def test_get_job_history_by_id_not_found(self, test_client, mock_session_async, mock_job_history_service):
        """Integration test: Get non-existent job_history returns 404."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_job_history_service
        mock_service_instance.get_by_id.return_value = None

        # Act
        response = test_client.get("/job-history/999")

        # Assert
        assert response.status_code == 404        
        mock_service_instance.get_by_id.assert_called_once_with(999)

    def test_get_all_job_history_success(self, test_client, mock_session_async, mock_job_history_service, multiple_job_history):
        """Integration test: Get all job_history returns 200 with pagination."""
        # Arrange
        paginated_response = PaginatedResponse[JobHistoryResponse](
            items=multiple_job_history,
            page=1,
            size=10,
            total=len(multiple_job_history)
        )

        # Unpack the mock service fixture
        _, mock_service_instance = mock_job_history_service
        mock_service_instance.get_all.return_value = paginated_response

        # Act
        response = test_client.get("/job-history/?page=1&size=10")

        # Assert
        assert response.status_code == 200
        mock_service_instance.get_all.assert_called_once()

    def test_search_job_history_success(self, test_client, mock_session_async, mock_job_history_service, multiple_job_history):
        """Integration test: Search job_history returns 200."""
        # Arrange
        search_filters = JobHistoryFilter().model_dump(exclude_unset=True)
        
        paginated_response = PaginatedResponse[JobHistoryResponse](
            items=multiple_job_history,
            page=1,
            size=10,
            total=1
        )

        # Unpack the mock service fixture
        _, mock_service_instance = mock_job_history_service
        mock_service_instance.search.return_value = paginated_response

        # Act
        response = test_client.post("/job-history/search?page=1&size=10", json=search_filters)

        # Assert
        assert response.status_code == 200
        mock_service_instance.search.assert_called_once()

    def test_update_job_history_success(self, test_client, updated_job_history, mock_job_history_service, updated_job_history_model):
        """Integration test: Update job_history returns 200."""
        # Arrange
        update_data = updated_job_history.model_dump(exclude_unset=True, mode='json')
        
        updated_response = JobHistoryResponse.model_validate(updated_job_history_model)

        # Unpack the mock service fixture
        _, mock_service_instance = mock_job_history_service
        mock_service_instance.update_by_id.return_value = updated_response

        # Act
        response = test_client.put("/job-history/1", json=update_data)

        # Assert
        assert response.status_code == 200        
        mock_service_instance.update_by_id.assert_called_once_with(1, JobHistoryUpdate(**update_data))

    def test_update_job_history_no_fields(self, test_client):
        """Integration test: Update with no fields returns 400."""
        # Act - Empty update payload
        response = test_client.put("/job-history/1", json={})

        # Assert
        assert response.status_code == 400

    def test_update_job_history_not_found(self, test_client, mock_session_async, mock_job_history_service, updated_job_history):
        """Integration test: Update non-existent job_history returns 404."""
        # Arrange
        update_data = updated_job_history.model_dump(exclude_unset=True, mode='json')

        # Unpack the mock service fixture
        _, mock_service_instance = mock_job_history_service
        mock_service_instance.update_by_id.return_value = None

        # Act
        response = test_client.put("/job-history/999", json=update_data)

        # Assert
        assert response.status_code == 404

    def test_delete_job_history_success(self, test_client, mock_session_async, mock_job_history_service):
        """Integration test: Delete job_history returns 200."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_job_history_service
        mock_service_instance.delete_by_id.return_value = True

        # Act
        response = test_client.delete("/job-history/1")

        # Assert
        assert response.status_code == 200

        mock_service_instance.delete_by_id.assert_called_once_with(1)

    def test_delete_job_history_not_found(self, test_client, mock_session_async, mock_job_history_service):
        """Integration test: Delete non-existent job_history returns 404."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_job_history_service
        mock_service_instance.delete_by_id.return_value = False

        # Act
        response = test_client.delete("/job-history/999")

        # Assert
        assert response.status_code == 404
