# ROSETIC:crud-guid


"""
Unit tests for the Projects API router endpoints.
"""
import pytest


import datetime
from decimal import Decimal
from unittest.mock import AsyncMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient

from core.database import get_db
from core.pagination import PaginatedResponse, PaginatedResponse
from features.tables.projects.schemas import ProjectResponse, ProjectCreate, ProjectUpdate, ProjectFilter
from features.tables.projects import router as projects_router

class TestProjectRouter:
    """Test cases for Project API router endpoints."""

    @pytest.fixture
    def app(self):
        """Create FastAPI app with projects router for testing."""
        app = FastAPI()
        app.include_router(projects_router.router)
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
    def expected_response(self, existing_project):
        return ProjectResponse.model_validate(existing_project)

    @pytest.fixture
    def mock_project_service(self):
        """Mock ProjectService for cleaner testing."""
        with patch.object(projects_router, 'ProjectService') as mock_service_class:
            mock_service_instance = AsyncMock()
            mock_service_class.return_value = mock_service_instance
            yield mock_service_class, mock_service_instance

    # ─── Integration Tests with Mocked Service ──────────────────────────────────
    def test_create_project_integration_success(self, test_client, mock_session_async, expected_response, mock_project_service, sample_data):
        """Integration test: Create project endpoint returns 200 with mocked service."""
        # Arrange
        mock_service_class, mock_service_instance = mock_project_service
        mock_service_instance.create.return_value = expected_response

        # Act
        create_data = ProjectCreate(**sample_data).model_dump(mode='json')
        response = test_client.post("/projects/", json=create_data)

        # Assert
        assert response.status_code == 201           
        # Verify service was called correctly
        mock_service_class.assert_called_once_with(session=mock_session_async)
        mock_service_instance.create.assert_called_once()

    def test_create_project_integration_validation_error(self, test_client, expected_response):
        """Integration test: Create project with invalid data returns 422."""
        # Arrange
        invalid_request_data = {
            "budget": "string in int field",
            "created_at": None,
            "end_date": None,
            "project_name": 123,
            "start_date": None,
            "status": 123,
            "tags": None,
        }

        # Act - Should get validation error before service is called
        response = test_client.post("/projects/", json=invalid_request_data)

        # Assert
        assert response.status_code == 422  # FastAPI validation error
        response_data = response.json()
        assert "detail" in response_data

            

    def test_get_project_by_id_success(self, test_client, mock_session_async, expected_response, mock_project_service):
        """Integration test: Get project by id returns 200."""
        # Unpack the mock service fixture
        mock_service_class, mock_service_instance = mock_project_service
        mock_service_instance.get_by_id.return_value = expected_response

        # Act
        response = test_client.get("/projects/1")

        # Assert
        assert response.status_code == 200
        
        # Verify service was called correctly
        mock_service_class.assert_called_once_with(session=mock_session_async)
        mock_service_instance.get_by_id.assert_called_once_with(1)

    def test_get_project_by_id_not_found(self, test_client, mock_session_async, mock_project_service):
        """Integration test: Get non-existent project returns 404."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_project_service
        mock_service_instance.get_by_id.return_value = None

        # Act
        response = test_client.get("/projects/999")

        # Assert
        assert response.status_code == 404        
        mock_service_instance.get_by_id.assert_called_once_with(999)

    def test_get_all_project_success(self, test_client, mock_session_async, mock_project_service, multiple_projects):
        """Integration test: Get all project returns 200 with pagination."""
        # Arrange
        paginated_response = PaginatedResponse[ProjectResponse](
            items=multiple_projects,
            page=1,
            size=10,
            total=len(multiple_projects)
        )

        # Unpack the mock service fixture
        _, mock_service_instance = mock_project_service
        mock_service_instance.get_all.return_value = paginated_response

        # Act
        response = test_client.get("/projects/?page=1&size=10")

        # Assert
        assert response.status_code == 200
        mock_service_instance.get_all.assert_called_once()

    def test_search_projects_success(self, test_client, mock_session_async, mock_project_service, multiple_projects):
        """Integration test: Search project returns 200."""
        # Arrange
        search_filters = ProjectFilter().model_dump(exclude_unset=True)
        
        paginated_response = PaginatedResponse[ProjectResponse](
            items=multiple_projects,
            page=1,
            size=10,
            total=1
        )

        # Unpack the mock service fixture
        _, mock_service_instance = mock_project_service
        mock_service_instance.search.return_value = paginated_response

        # Act
        response = test_client.post("/projects/search?page=1&size=10", json=search_filters)

        # Assert
        assert response.status_code == 200
        mock_service_instance.search.assert_called_once()

    def test_update_project_success(self, test_client, updated_project, mock_project_service, updated_project_model):
        """Integration test: Update project returns 200."""
        # Arrange
        update_data = updated_project.model_dump(exclude_unset=True, mode='json')
        
        updated_response = ProjectResponse.model_validate(updated_project_model)

        # Unpack the mock service fixture
        _, mock_service_instance = mock_project_service
        mock_service_instance.update_by_id.return_value = updated_response

        # Act
        response = test_client.put("/projects/1", json=update_data)

        # Assert
        assert response.status_code == 200        
        mock_service_instance.update_by_id.assert_called_once_with(1, ProjectUpdate(**update_data))

    def test_update_project_no_fields(self, test_client):
        """Integration test: Update with no fields returns 400."""
        # Act - Empty update payload
        response = test_client.put("/projects/1", json={})

        # Assert
        assert response.status_code == 400

    def test_update_project_not_found(self, test_client, mock_session_async, mock_project_service, updated_project):
        """Integration test: Update non-existent project returns 404."""
        # Arrange
        update_data = updated_project.model_dump(exclude_unset=True, mode='json')

        # Unpack the mock service fixture
        _, mock_service_instance = mock_project_service
        mock_service_instance.update_by_id.return_value = None

        # Act
        response = test_client.put("/projects/999", json=update_data)

        # Assert
        assert response.status_code == 404

    def test_delete_project_success(self, test_client, mock_session_async, mock_project_service):
        """Integration test: Delete project returns 200."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_project_service
        mock_service_instance.delete_by_id.return_value = True

        # Act
        response = test_client.delete("/projects/1")

        # Assert
        assert response.status_code == 200

        mock_service_instance.delete_by_id.assert_called_once_with(1)

    def test_delete_project_not_found(self, test_client, mock_session_async, mock_project_service):
        """Integration test: Delete non-existent project returns 404."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_project_service
        mock_service_instance.delete_by_id.return_value = False

        # Act
        response = test_client.delete("/projects/999")

        # Assert
        assert response.status_code == 404
