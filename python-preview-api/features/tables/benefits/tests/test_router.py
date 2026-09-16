# ROSETIC:crud-guid


"""
Unit tests for the Benefits API router endpoints.
"""
import pytest


import datetime
from decimal import Decimal
from unittest.mock import AsyncMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient

from core.database import get_db
from core.pagination import PaginatedResponse, PaginatedResponse
from features.tables.benefits.schemas import BenefitResponse, BenefitCreate, BenefitUpdate, BenefitFilter
from features.tables.benefits import router as benefits_router

class TestBenefitRouter:
    """Test cases for Benefit API router endpoints."""

    @pytest.fixture
    def app(self):
        """Create FastAPI app with benefits router for testing."""
        app = FastAPI()
        app.include_router(benefits_router.router)
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
    def expected_response(self, existing_benefit):
        return BenefitResponse.model_validate(existing_benefit)

    @pytest.fixture
    def mock_benefit_service(self):
        """Mock BenefitService for cleaner testing."""
        with patch.object(benefits_router, 'BenefitService') as mock_service_class:
            mock_service_instance = AsyncMock()
            mock_service_class.return_value = mock_service_instance
            yield mock_service_class, mock_service_instance

    # ─── Integration Tests with Mocked Service ──────────────────────────────────
    def test_create_benefit_integration_success(self, test_client, mock_session_async, expected_response, mock_benefit_service, sample_data):
        """Integration test: Create benefit endpoint returns 200 with mocked service."""
        # Arrange
        mock_service_class, mock_service_instance = mock_benefit_service
        mock_service_instance.create.return_value = expected_response

        # Act
        create_data = BenefitCreate(**sample_data).model_dump(mode='json')
        response = test_client.post("/benefits/", json=create_data)

        # Assert
        assert response.status_code == 201           
        # Verify service was called correctly
        mock_service_class.assert_called_once_with(session=mock_session_async)
        mock_service_instance.create.assert_called_once()

    def test_create_benefit_integration_validation_error(self, test_client, expected_response):
        """Integration test: Create benefit with invalid data returns 422."""
        # Arrange
        invalid_request_data = {
            "benefit_name": 123,
            "benefit_type": 123,
            "coverage_details": None,
            "created_at": None,
            "monthly_cost": "string in int field",
        }

        # Act - Should get validation error before service is called
        response = test_client.post("/benefits/", json=invalid_request_data)

        # Assert
        assert response.status_code == 422  # FastAPI validation error
        response_data = response.json()
        assert "detail" in response_data

            

    def test_get_benefit_by_id_success(self, test_client, mock_session_async, expected_response, mock_benefit_service):
        """Integration test: Get benefit by id returns 200."""
        # Unpack the mock service fixture
        mock_service_class, mock_service_instance = mock_benefit_service
        mock_service_instance.get_by_id.return_value = expected_response

        # Act
        response = test_client.get("/benefits/1")

        # Assert
        assert response.status_code == 200
        
        # Verify service was called correctly
        mock_service_class.assert_called_once_with(session=mock_session_async)
        mock_service_instance.get_by_id.assert_called_once_with(1)

    def test_get_benefit_by_id_not_found(self, test_client, mock_session_async, mock_benefit_service):
        """Integration test: Get non-existent benefit returns 404."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_benefit_service
        mock_service_instance.get_by_id.return_value = None

        # Act
        response = test_client.get("/benefits/999")

        # Assert
        assert response.status_code == 404        
        mock_service_instance.get_by_id.assert_called_once_with(999)

    def test_get_all_benefit_success(self, test_client, mock_session_async, mock_benefit_service, multiple_benefits):
        """Integration test: Get all benefit returns 200 with pagination."""
        # Arrange
        paginated_response = PaginatedResponse[BenefitResponse](
            items=multiple_benefits,
            page=1,
            size=10,
            total=len(multiple_benefits)
        )

        # Unpack the mock service fixture
        _, mock_service_instance = mock_benefit_service
        mock_service_instance.get_all.return_value = paginated_response

        # Act
        response = test_client.get("/benefits/?page=1&size=10")

        # Assert
        assert response.status_code == 200
        mock_service_instance.get_all.assert_called_once()

    def test_search_benefits_success(self, test_client, mock_session_async, mock_benefit_service, multiple_benefits):
        """Integration test: Search benefit returns 200."""
        # Arrange
        search_filters = BenefitFilter().model_dump(exclude_unset=True)
        
        paginated_response = PaginatedResponse[BenefitResponse](
            items=multiple_benefits,
            page=1,
            size=10,
            total=1
        )

        # Unpack the mock service fixture
        _, mock_service_instance = mock_benefit_service
        mock_service_instance.search.return_value = paginated_response

        # Act
        response = test_client.post("/benefits/search?page=1&size=10", json=search_filters)

        # Assert
        assert response.status_code == 200
        mock_service_instance.search.assert_called_once()

    def test_update_benefit_success(self, test_client, updated_benefit, mock_benefit_service, updated_benefit_model):
        """Integration test: Update benefit returns 200."""
        # Arrange
        update_data = updated_benefit.model_dump(exclude_unset=True, mode='json')
        
        updated_response = BenefitResponse.model_validate(updated_benefit_model)

        # Unpack the mock service fixture
        _, mock_service_instance = mock_benefit_service
        mock_service_instance.update_by_id.return_value = updated_response

        # Act
        response = test_client.put("/benefits/1", json=update_data)

        # Assert
        assert response.status_code == 200        
        mock_service_instance.update_by_id.assert_called_once_with(1, BenefitUpdate(**update_data))

    def test_update_benefit_no_fields(self, test_client):
        """Integration test: Update with no fields returns 400."""
        # Act - Empty update payload
        response = test_client.put("/benefits/1", json={})

        # Assert
        assert response.status_code == 400

    def test_update_benefit_not_found(self, test_client, mock_session_async, mock_benefit_service, updated_benefit):
        """Integration test: Update non-existent benefit returns 404."""
        # Arrange
        update_data = updated_benefit.model_dump(exclude_unset=True, mode='json')

        # Unpack the mock service fixture
        _, mock_service_instance = mock_benefit_service
        mock_service_instance.update_by_id.return_value = None

        # Act
        response = test_client.put("/benefits/999", json=update_data)

        # Assert
        assert response.status_code == 404

    def test_delete_benefit_success(self, test_client, mock_session_async, mock_benefit_service):
        """Integration test: Delete benefit returns 200."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_benefit_service
        mock_service_instance.delete_by_id.return_value = True

        # Act
        response = test_client.delete("/benefits/1")

        # Assert
        assert response.status_code == 200

        mock_service_instance.delete_by_id.assert_called_once_with(1)

    def test_delete_benefit_not_found(self, test_client, mock_session_async, mock_benefit_service):
        """Integration test: Delete non-existent benefit returns 404."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_benefit_service
        mock_service_instance.delete_by_id.return_value = False

        # Act
        response = test_client.delete("/benefits/999")

        # Assert
        assert response.status_code == 404
