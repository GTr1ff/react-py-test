# ROSETIC:crud-guid


"""
Unit tests for the Tasks API router endpoints.
"""
import pytest

import base64
import datetime

from unittest.mock import AsyncMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient

from core.database import get_db
from core.pagination import PaginatedResponse, PaginatedResponse
from features.tables.tasks.schemas import TaskResponse, TaskCreate, TaskUpdate, TaskFilter
from features.tables.tasks import router as tasks_router

class TestTaskRouter:
    """Test cases for Task API router endpoints."""

    @pytest.fixture
    def app(self):
        """Create FastAPI app with tasks router for testing."""
        app = FastAPI()
        app.include_router(tasks_router.router)
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
    def expected_response(self, existing_task):
        return TaskResponse.model_validate(existing_task)

    @pytest.fixture
    def mock_task_service(self):
        """Mock TaskService for cleaner testing."""
        with patch.object(tasks_router, 'TaskService') as mock_service_class:
            mock_service_instance = AsyncMock()
            mock_service_class.return_value = mock_service_instance
            yield mock_service_class, mock_service_instance

    # ─── Integration Tests with Mocked Service ──────────────────────────────────
    def test_create_task_integration_success(self, test_client, mock_session_async, expected_response, mock_task_service, sample_data):
        """Integration test: Create task endpoint returns 200 with mocked service."""
        # Arrange
        mock_service_class, mock_service_instance = mock_task_service
        mock_service_instance.create.return_value = expected_response

        # Act
        create_data = TaskCreate(**sample_data).model_dump(mode='json')
        response = test_client.post("/tasks/", json=create_data)

        # Assert
        assert response.status_code == 201           
        # Verify service was called correctly
        mock_service_class.assert_called_once_with(session=mock_session_async)
        mock_service_instance.create.assert_called_once()

    def test_create_task_integration_validation_error(self, test_client, expected_response):
        """Integration test: Create task with invalid data returns 422."""
        # Arrange
        invalid_request_data = {
            "assigned_to": "string in int field",
            "attachment": None,
            "completed": "string in bool field",
            "due_date": None,
            "notes": 123,
            "project_id": "string in int field",
        }

        # Act - Should get validation error before service is called
        response = test_client.post("/tasks/", json=invalid_request_data)

        # Assert
        assert response.status_code == 422  # FastAPI validation error
        response_data = response.json()
        assert "detail" in response_data

            

    def test_get_task_by_id_success(self, test_client, mock_session_async, expected_response, mock_task_service):
        """Integration test: Get task by id returns 200."""
        # Unpack the mock service fixture
        mock_service_class, mock_service_instance = mock_task_service
        mock_service_instance.get_by_id.return_value = expected_response

        # Act
        response = test_client.get("/tasks/1")

        # Assert
        assert response.status_code == 200
        
        # Verify service was called correctly
        mock_service_class.assert_called_once_with(session=mock_session_async)
        mock_service_instance.get_by_id.assert_called_once_with(1)

    def test_get_task_by_id_not_found(self, test_client, mock_session_async, mock_task_service):
        """Integration test: Get non-existent task returns 404."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_task_service
        mock_service_instance.get_by_id.return_value = None

        # Act
        response = test_client.get("/tasks/999")

        # Assert
        assert response.status_code == 404        
        mock_service_instance.get_by_id.assert_called_once_with(999)

    def test_get_all_task_success(self, test_client, mock_session_async, mock_task_service, multiple_tasks):
        """Integration test: Get all task returns 200 with pagination."""
        # Arrange
        paginated_response = PaginatedResponse[TaskResponse](
            items=multiple_tasks,
            page=1,
            size=10,
            total=len(multiple_tasks)
        )

        # Unpack the mock service fixture
        _, mock_service_instance = mock_task_service
        mock_service_instance.get_all.return_value = paginated_response

        # Act
        response = test_client.get("/tasks/?page=1&size=10")

        # Assert
        assert response.status_code == 200
        mock_service_instance.get_all.assert_called_once()

    def test_search_tasks_success(self, test_client, mock_session_async, mock_task_service, multiple_tasks):
        """Integration test: Search task returns 200."""
        # Arrange
        search_filters = TaskFilter().model_dump(exclude_unset=True)
        
        paginated_response = PaginatedResponse[TaskResponse](
            items=multiple_tasks,
            page=1,
            size=10,
            total=1
        )

        # Unpack the mock service fixture
        _, mock_service_instance = mock_task_service
        mock_service_instance.search.return_value = paginated_response

        # Act
        response = test_client.post("/tasks/search?page=1&size=10", json=search_filters)

        # Assert
        assert response.status_code == 200
        mock_service_instance.search.assert_called_once()

    def test_update_task_success(self, test_client, updated_task, mock_task_service, updated_task_model):
        """Integration test: Update task returns 200."""
        # Arrange
        update_data = updated_task.model_dump(exclude_unset=True, mode='json')
        
        updated_response = TaskResponse.model_validate(updated_task_model)

        # Unpack the mock service fixture
        _, mock_service_instance = mock_task_service
        mock_service_instance.update_by_id.return_value = updated_response

        # Act
        response = test_client.put("/tasks/1", json=update_data)

        # Assert
        assert response.status_code == 200        
        mock_service_instance.update_by_id.assert_called_once_with(1, TaskUpdate(**update_data))

    def test_update_task_no_fields(self, test_client):
        """Integration test: Update with no fields returns 400."""
        # Act - Empty update payload
        response = test_client.put("/tasks/1", json={})

        # Assert
        assert response.status_code == 400

    def test_update_task_not_found(self, test_client, mock_session_async, mock_task_service, updated_task):
        """Integration test: Update non-existent task returns 404."""
        # Arrange
        update_data = updated_task.model_dump(exclude_unset=True, mode='json')

        # Unpack the mock service fixture
        _, mock_service_instance = mock_task_service
        mock_service_instance.update_by_id.return_value = None

        # Act
        response = test_client.put("/tasks/999", json=update_data)

        # Assert
        assert response.status_code == 404

    def test_delete_task_success(self, test_client, mock_session_async, mock_task_service):
        """Integration test: Delete task returns 200."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_task_service
        mock_service_instance.delete_by_id.return_value = True

        # Act
        response = test_client.delete("/tasks/1")

        # Assert
        assert response.status_code == 200

        mock_service_instance.delete_by_id.assert_called_once_with(1)

    def test_delete_task_not_found(self, test_client, mock_session_async, mock_task_service):
        """Integration test: Delete non-existent task returns 404."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_task_service
        mock_service_instance.delete_by_id.return_value = False

        # Act
        response = test_client.delete("/tasks/999")

        # Assert
        assert response.status_code == 404
