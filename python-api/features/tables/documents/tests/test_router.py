# ROSETIC:crud-guid


"""
Unit tests for the Documents API router endpoints.
"""
import pytest

import base64


from unittest.mock import AsyncMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient

from core.database import get_db
from core.pagination import PaginatedResponse, PaginatedResponse
from features.tables.documents.schemas import DocumentResponse, DocumentCreate, DocumentUpdate, DocumentFilter
from features.tables.documents import router as documents_router

class TestDocumentRouter:
    """Test cases for Document API router endpoints."""

    @pytest.fixture
    def app(self):
        """Create FastAPI app with documents router for testing."""
        app = FastAPI()
        app.include_router(documents_router.router)
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
    def expected_response(self, existing_document):
        return DocumentResponse.model_validate(existing_document)

    @pytest.fixture
    def mock_document_service(self):
        """Mock DocumentService for cleaner testing."""
        with patch.object(documents_router, 'DocumentService') as mock_service_class:
            mock_service_instance = AsyncMock()
            mock_service_class.return_value = mock_service_instance
            yield mock_service_class, mock_service_instance

    # ─── Integration Tests with Mocked Service ──────────────────────────────────
    def test_create_document_integration_success(self, test_client, mock_session_async, expected_response, mock_document_service, sample_data):
        """Integration test: Create document endpoint returns 200 with mocked service."""
        # Arrange
        mock_service_class, mock_service_instance = mock_document_service
        mock_service_instance.create.return_value = expected_response

        # Act
        create_data = DocumentCreate(**sample_data).model_dump(mode='json')
        response = test_client.post("/documents/", json=create_data)

        # Assert
        assert response.status_code == 201           
        # Verify service was called correctly
        mock_service_class.assert_called_once_with(session=mock_session_async)
        mock_service_instance.create.assert_called_once()

    def test_create_document_integration_validation_error(self, test_client, expected_response):
        """Integration test: Create document with invalid data returns 422."""
        # Arrange
        invalid_request_data = {
            "doc_content": None,
            "doc_name": 123,
            "doc_type": 123,
            "employee_id": "string in int field",
        }

        # Act - Should get validation error before service is called
        response = test_client.post("/documents/", json=invalid_request_data)

        # Assert
        assert response.status_code == 422  # FastAPI validation error
        response_data = response.json()
        assert "detail" in response_data

            

    def test_get_document_by_id_success(self, test_client, mock_session_async, expected_response, mock_document_service):
        """Integration test: Get document by id returns 200."""
        # Unpack the mock service fixture
        mock_service_class, mock_service_instance = mock_document_service
        mock_service_instance.get_by_id.return_value = expected_response

        # Act
        response = test_client.get("/documents/1")

        # Assert
        assert response.status_code == 200
        
        # Verify service was called correctly
        mock_service_class.assert_called_once_with(session=mock_session_async)
        mock_service_instance.get_by_id.assert_called_once_with(1)

    def test_get_document_by_id_not_found(self, test_client, mock_session_async, mock_document_service):
        """Integration test: Get non-existent document returns 404."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_document_service
        mock_service_instance.get_by_id.return_value = None

        # Act
        response = test_client.get("/documents/999")

        # Assert
        assert response.status_code == 404        
        mock_service_instance.get_by_id.assert_called_once_with(999)

    def test_get_all_document_success(self, test_client, mock_session_async, mock_document_service, multiple_documents):
        """Integration test: Get all document returns 200 with pagination."""
        # Arrange
        paginated_response = PaginatedResponse[DocumentResponse](
            items=multiple_documents,
            page=1,
            size=10,
            total=len(multiple_documents)
        )

        # Unpack the mock service fixture
        _, mock_service_instance = mock_document_service
        mock_service_instance.get_all.return_value = paginated_response

        # Act
        response = test_client.get("/documents/?page=1&size=10")

        # Assert
        assert response.status_code == 200
        mock_service_instance.get_all.assert_called_once()

    def test_search_documents_success(self, test_client, mock_session_async, mock_document_service, multiple_documents):
        """Integration test: Search document returns 200."""
        # Arrange
        search_filters = DocumentFilter().model_dump(exclude_unset=True)
        
        paginated_response = PaginatedResponse[DocumentResponse](
            items=multiple_documents,
            page=1,
            size=10,
            total=1
        )

        # Unpack the mock service fixture
        _, mock_service_instance = mock_document_service
        mock_service_instance.search.return_value = paginated_response

        # Act
        response = test_client.post("/documents/search?page=1&size=10", json=search_filters)

        # Assert
        assert response.status_code == 200
        mock_service_instance.search.assert_called_once()

    def test_update_document_success(self, test_client, updated_document, mock_document_service, updated_document_model):
        """Integration test: Update document returns 200."""
        # Arrange
        update_data = updated_document.model_dump(exclude_unset=True, mode='json')
        
        updated_response = DocumentResponse.model_validate(updated_document_model)

        # Unpack the mock service fixture
        _, mock_service_instance = mock_document_service
        mock_service_instance.update_by_id.return_value = updated_response

        # Act
        response = test_client.put("/documents/1", json=update_data)

        # Assert
        assert response.status_code == 200        
        mock_service_instance.update_by_id.assert_called_once_with(1, DocumentUpdate(**update_data))

    def test_update_document_no_fields(self, test_client):
        """Integration test: Update with no fields returns 400."""
        # Act - Empty update payload
        response = test_client.put("/documents/1", json={})

        # Assert
        assert response.status_code == 400

    def test_update_document_not_found(self, test_client, mock_session_async, mock_document_service, updated_document):
        """Integration test: Update non-existent document returns 404."""
        # Arrange
        update_data = updated_document.model_dump(exclude_unset=True, mode='json')

        # Unpack the mock service fixture
        _, mock_service_instance = mock_document_service
        mock_service_instance.update_by_id.return_value = None

        # Act
        response = test_client.put("/documents/999", json=update_data)

        # Assert
        assert response.status_code == 404

    def test_delete_document_success(self, test_client, mock_session_async, mock_document_service):
        """Integration test: Delete document returns 200."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_document_service
        mock_service_instance.delete_by_id.return_value = True

        # Act
        response = test_client.delete("/documents/1")

        # Assert
        assert response.status_code == 200

        mock_service_instance.delete_by_id.assert_called_once_with(1)

    def test_delete_document_not_found(self, test_client, mock_session_async, mock_document_service):
        """Integration test: Delete non-existent document returns 404."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_document_service
        mock_service_instance.delete_by_id.return_value = False

        # Act
        response = test_client.delete("/documents/999")

        # Assert
        assert response.status_code == 404
