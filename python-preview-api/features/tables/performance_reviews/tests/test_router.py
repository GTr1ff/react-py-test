# ROSETIC:crud-guid


"""
Unit tests for the Performance_reviews API router endpoints.
"""
import pytest


import datetime

from unittest.mock import AsyncMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient

from core.database import get_db
from core.pagination import PaginatedResponse, PaginatedResponse
from features.tables.performance_reviews.schemas import PerformanceReviewResponse, PerformanceReviewCreate, PerformanceReviewUpdate, PerformanceReviewFilter
from features.tables.performance_reviews import router as performance_reviews_router

class TestPerformanceReviewRouter:
    """Test cases for PerformanceReview API router endpoints."""

    @pytest.fixture
    def app(self):
        """Create FastAPI app with performance_reviews router for testing."""
        app = FastAPI()
        app.include_router(performance_reviews_router.router)
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
    def expected_response(self, existing_performance_review):
        return PerformanceReviewResponse.model_validate(existing_performance_review)

    @pytest.fixture
    def mock_performance_review_service(self):
        """Mock PerformanceReviewService for cleaner testing."""
        with patch.object(performance_reviews_router, 'PerformanceReviewService') as mock_service_class:
            mock_service_instance = AsyncMock()
            mock_service_class.return_value = mock_service_instance
            yield mock_service_class, mock_service_instance

    # ─── Integration Tests with Mocked Service ──────────────────────────────────
    def test_create_performance_review_integration_success(self, test_client, mock_session_async, expected_response, mock_performance_review_service, sample_data):
        """Integration test: Create performance_review endpoint returns 200 with mocked service."""
        # Arrange
        mock_service_class, mock_service_instance = mock_performance_review_service
        mock_service_instance.create.return_value = expected_response

        # Act
        create_data = PerformanceReviewCreate(**sample_data).model_dump(mode='json')
        response = test_client.post("/performance-reviews/", json=create_data)

        # Assert
        assert response.status_code == 201           
        # Verify service was called correctly
        mock_service_class.assert_called_once_with(session=mock_session_async)
        mock_service_instance.create.assert_called_once()

    def test_create_performance_review_integration_validation_error(self, test_client, expected_response):
        """Integration test: Create performance_review with invalid data returns 422."""
        # Arrange
        invalid_request_data = {
            "details": None,
            "employee_id": "string in int field",
            "review_date": None,
        }

        # Act - Should get validation error before service is called
        response = test_client.post("/performance-reviews/", json=invalid_request_data)

        # Assert
        assert response.status_code == 422  # FastAPI validation error
        response_data = response.json()
        assert "detail" in response_data

            

    def test_get_performance_review_by_id_success(self, test_client, mock_session_async, expected_response, mock_performance_review_service):
        """Integration test: Get performance_review by id returns 200."""
        # Unpack the mock service fixture
        mock_service_class, mock_service_instance = mock_performance_review_service
        mock_service_instance.get_by_id.return_value = expected_response

        # Act
        response = test_client.get("/performance-reviews/1")

        # Assert
        assert response.status_code == 200
        
        # Verify service was called correctly
        mock_service_class.assert_called_once_with(session=mock_session_async)
        mock_service_instance.get_by_id.assert_called_once_with(1)

    def test_get_performance_review_by_id_not_found(self, test_client, mock_session_async, mock_performance_review_service):
        """Integration test: Get non-existent performance_review returns 404."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_performance_review_service
        mock_service_instance.get_by_id.return_value = None

        # Act
        response = test_client.get("/performance-reviews/999")

        # Assert
        assert response.status_code == 404        
        mock_service_instance.get_by_id.assert_called_once_with(999)

    def test_get_all_performance_review_success(self, test_client, mock_session_async, mock_performance_review_service, multiple_performance_reviews):
        """Integration test: Get all performance_review returns 200 with pagination."""
        # Arrange
        paginated_response = PaginatedResponse[PerformanceReviewResponse](
            items=multiple_performance_reviews,
            page=1,
            size=10,
            total=len(multiple_performance_reviews)
        )

        # Unpack the mock service fixture
        _, mock_service_instance = mock_performance_review_service
        mock_service_instance.get_all.return_value = paginated_response

        # Act
        response = test_client.get("/performance-reviews/?page=1&size=10")

        # Assert
        assert response.status_code == 200
        mock_service_instance.get_all.assert_called_once()

    def test_search_performance_reviews_success(self, test_client, mock_session_async, mock_performance_review_service, multiple_performance_reviews):
        """Integration test: Search performance_review returns 200."""
        # Arrange
        search_filters = PerformanceReviewFilter().model_dump(exclude_unset=True)
        
        paginated_response = PaginatedResponse[PerformanceReviewResponse](
            items=multiple_performance_reviews,
            page=1,
            size=10,
            total=1
        )

        # Unpack the mock service fixture
        _, mock_service_instance = mock_performance_review_service
        mock_service_instance.search.return_value = paginated_response

        # Act
        response = test_client.post("/performance-reviews/search?page=1&size=10", json=search_filters)

        # Assert
        assert response.status_code == 200
        mock_service_instance.search.assert_called_once()

    def test_update_performance_review_success(self, test_client, updated_performance_review, mock_performance_review_service, updated_performance_review_model):
        """Integration test: Update performance_review returns 200."""
        # Arrange
        update_data = updated_performance_review.model_dump(exclude_unset=True, mode='json')
        
        updated_response = PerformanceReviewResponse.model_validate(updated_performance_review_model)

        # Unpack the mock service fixture
        _, mock_service_instance = mock_performance_review_service
        mock_service_instance.update_by_id.return_value = updated_response

        # Act
        response = test_client.put("/performance-reviews/1", json=update_data)

        # Assert
        assert response.status_code == 200        
        mock_service_instance.update_by_id.assert_called_once_with(1, PerformanceReviewUpdate(**update_data))

    def test_update_performance_review_no_fields(self, test_client):
        """Integration test: Update with no fields returns 400."""
        # Act - Empty update payload
        response = test_client.put("/performance-reviews/1", json={})

        # Assert
        assert response.status_code == 400

    def test_update_performance_review_not_found(self, test_client, mock_session_async, mock_performance_review_service, updated_performance_review):
        """Integration test: Update non-existent performance_review returns 404."""
        # Arrange
        update_data = updated_performance_review.model_dump(exclude_unset=True, mode='json')

        # Unpack the mock service fixture
        _, mock_service_instance = mock_performance_review_service
        mock_service_instance.update_by_id.return_value = None

        # Act
        response = test_client.put("/performance-reviews/999", json=update_data)

        # Assert
        assert response.status_code == 404

    def test_delete_performance_review_success(self, test_client, mock_session_async, mock_performance_review_service):
        """Integration test: Delete performance_review returns 200."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_performance_review_service
        mock_service_instance.delete_by_id.return_value = True

        # Act
        response = test_client.delete("/performance-reviews/1")

        # Assert
        assert response.status_code == 200

        mock_service_instance.delete_by_id.assert_called_once_with(1)

    def test_delete_performance_review_not_found(self, test_client, mock_session_async, mock_performance_review_service):
        """Integration test: Delete non-existent performance_review returns 404."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_performance_review_service
        mock_service_instance.delete_by_id.return_value = False

        # Act
        response = test_client.delete("/performance-reviews/999")

        # Assert
        assert response.status_code == 404
