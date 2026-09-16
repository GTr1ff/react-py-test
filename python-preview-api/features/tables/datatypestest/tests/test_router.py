# ROSETIC:crud-guid


"""
Unit tests for the Datatypestest API router endpoints.
"""
import pytest
import uuid
import base64
import datetime
from decimal import Decimal
from unittest.mock import AsyncMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient

from core.database import get_db
from core.pagination import PaginatedResponse, PaginatedResponse
from features.tables.datatypestest.schemas import DatatypestestResponse, DatatypestestCreate, DatatypestestUpdate, DatatypestestFilter
from features.tables.datatypestest import router as datatypestest_router

class TestDatatypestestRouter:
    """Test cases for Datatypestest API router endpoints."""

    @pytest.fixture
    def app(self):
        """Create FastAPI app with datatypestest router for testing."""
        app = FastAPI()
        app.include_router(datatypestest_router.router)
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
    def expected_response(self, existing_datatypestest):
        return DatatypestestResponse.model_validate(existing_datatypestest)

    @pytest.fixture
    def mock_datatypestest_service(self):
        """Mock DatatypestestService for cleaner testing."""
        with patch.object(datatypestest_router, 'DatatypestestService') as mock_service_class:
            mock_service_instance = AsyncMock()
            mock_service_class.return_value = mock_service_instance
            yield mock_service_class, mock_service_instance

    # ─── Integration Tests with Mocked Service ──────────────────────────────────
    def test_create_datatypestest_integration_success(self, test_client, mock_session_async, expected_response, mock_datatypestest_service, sample_data):
        """Integration test: Create datatypestest endpoint returns 200 with mocked service."""
        # Arrange
        mock_service_class, mock_service_instance = mock_datatypestest_service
        mock_service_instance.create.return_value = expected_response

        # Act
        create_data = DatatypestestCreate(**sample_data).model_dump(mode='json')
        response = test_client.post("/datatypestest/", json=create_data)

        # Assert
        assert response.status_code == 201           
        # Verify service was called correctly
        mock_service_class.assert_called_once_with(session=mock_session_async)
        mock_service_instance.create.assert_called_once()

    def test_create_datatypestest_integration_validation_error(self, test_client, expected_response):
        """Integration test: Create datatypestest with invalid data returns 422."""
        # Arrange
        invalid_request_data = {
            "set_col": 123,
            "boolean_col": "string in bool field",
            "bytea_col": None,
            "character_col": 123,
            "date_col": None,
            "numeric_col": "string in int field",
            "double_precision_col": "string in int field",
            "int_array_col": None,
            "integer_col": "string in int field",
            "real_col": "string in int field",
            "smallint_col": "string in int field",
            "text_array_col": None,
            "text_col": 123,
            "time_col": None,
            "timestamp_col": None,
            "timestamptz_col": None,
            "timetz_col": None,
            "character_varying_col": 123,
            "enum_col": 123,
            "ntext_col": 123,
            "tinytext_col": 123,
            "mediumtext_col": 123,
            "longtext_col": 123,
            "char_col": 123,
            "nchar_col": 123,
            "varchar_col": 123,
            "nvarchar_col": 123,
            "xml_col": None,
            "tinyint_col": "string in int field",
            "mediumint_col": "string in int field",
            "year_col": "string in int field",
            "decimal_col": "string in int field",
            "bigdecimal_col": "string in int field",
            "money_col": "string in int field",
            "smallmoney_col": "string in int field",
            "datetime2_col": None,
            "blob_col": None,
            "longblob_col": None,
            "mediumblob_col": None,
            "tinyblob_col": None,
            "binary_col": None,
            "varbinary_col": None,
            "image_col": None,
            "uuid_col": None,
            "uniqueidentifier_col": None,
        }

        # Act - Should get validation error before service is called
        response = test_client.post("/datatypestest/", json=invalid_request_data)

        # Assert
        assert response.status_code == 422  # FastAPI validation error
        response_data = response.json()
        assert "detail" in response_data

            

    def test_get_datatypestest_by_keykey_success(self, test_client, mock_session_async, expected_response, mock_datatypestest_service):
        """Integration test: Get datatypestest by keykey returns 200."""
        # Unpack the mock service fixture
        mock_service_class, mock_service_instance = mock_datatypestest_service
        mock_service_instance.get_by_keykey.return_value = expected_response

        # Act
        response = test_client.get("/datatypestest/1")

        # Assert
        assert response.status_code == 200
        
        # Verify service was called correctly
        mock_service_class.assert_called_once_with(session=mock_session_async)
        mock_service_instance.get_by_keykey.assert_called_once_with(1)

    def test_get_datatypestest_by_keykey_not_found(self, test_client, mock_session_async, mock_datatypestest_service):
        """Integration test: Get non-existent datatypestest returns 404."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_datatypestest_service
        mock_service_instance.get_by_keykey.return_value = None

        # Act
        response = test_client.get("/datatypestest/999")

        # Assert
        assert response.status_code == 404        
        mock_service_instance.get_by_keykey.assert_called_once_with(999)

    def test_get_all_datatypestest_success(self, test_client, mock_session_async, mock_datatypestest_service, multiple_datatypestest):
        """Integration test: Get all datatypestest returns 200 with pagination."""
        # Arrange
        paginated_response = PaginatedResponse[DatatypestestResponse](
            items=multiple_datatypestest,
            page=1,
            size=10,
            total=len(multiple_datatypestest)
        )

        # Unpack the mock service fixture
        _, mock_service_instance = mock_datatypestest_service
        mock_service_instance.get_all.return_value = paginated_response

        # Act
        response = test_client.get("/datatypestest/?page=1&size=10")

        # Assert
        assert response.status_code == 200
        mock_service_instance.get_all.assert_called_once()

    def test_search_datatypestest_success(self, test_client, mock_session_async, mock_datatypestest_service, multiple_datatypestest):
        """Integration test: Search datatypestest returns 200."""
        # Arrange
        search_filters = DatatypestestFilter().model_dump(exclude_unset=True)
        
        paginated_response = PaginatedResponse[DatatypestestResponse](
            items=multiple_datatypestest,
            page=1,
            size=10,
            total=1
        )

        # Unpack the mock service fixture
        _, mock_service_instance = mock_datatypestest_service
        mock_service_instance.search.return_value = paginated_response

        # Act
        response = test_client.post("/datatypestest/search?page=1&size=10", json=search_filters)

        # Assert
        assert response.status_code == 200
        mock_service_instance.search.assert_called_once()

    def test_update_datatypestest_success(self, test_client, updated_datatypestest, mock_datatypestest_service, updated_datatypestest_model):
        """Integration test: Update datatypestest returns 200."""
        # Arrange
        update_data = updated_datatypestest.model_dump(exclude_unset=True, mode='json')
        
        updated_response = DatatypestestResponse.model_validate(updated_datatypestest_model)

        # Unpack the mock service fixture
        _, mock_service_instance = mock_datatypestest_service
        mock_service_instance.update_by_keykey.return_value = updated_response

        # Act
        response = test_client.put("/datatypestest/1", json=update_data)

        # Assert
        assert response.status_code == 200        
        mock_service_instance.update_by_keykey.assert_called_once_with(1, DatatypestestUpdate(**update_data))

    def test_update_datatypestest_no_fields(self, test_client):
        """Integration test: Update with no fields returns 400."""
        # Act - Empty update payload
        response = test_client.put("/datatypestest/1", json={})

        # Assert
        assert response.status_code == 400

    def test_update_datatypestest_not_found(self, test_client, mock_session_async, mock_datatypestest_service, updated_datatypestest):
        """Integration test: Update non-existent datatypestest returns 404."""
        # Arrange
        update_data = updated_datatypestest.model_dump(exclude_unset=True, mode='json')

        # Unpack the mock service fixture
        _, mock_service_instance = mock_datatypestest_service
        mock_service_instance.update_by_keykey.return_value = None

        # Act
        response = test_client.put("/datatypestest/999", json=update_data)

        # Assert
        assert response.status_code == 404

    def test_delete_datatypestest_success(self, test_client, mock_session_async, mock_datatypestest_service):
        """Integration test: Delete datatypestest returns 200."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_datatypestest_service
        mock_service_instance.delete_by_keykey.return_value = True

        # Act
        response = test_client.delete("/datatypestest/1")

        # Assert
        assert response.status_code == 200

        mock_service_instance.delete_by_keykey.assert_called_once_with(1)

    def test_delete_datatypestest_not_found(self, test_client, mock_session_async, mock_datatypestest_service):
        """Integration test: Delete non-existent datatypestest returns 404."""
        # Unpack the mock service fixture
        _, mock_service_instance = mock_datatypestest_service
        mock_service_instance.delete_by_keykey.return_value = False

        # Act
        response = test_client.delete("/datatypestest/999")

        # Assert
        assert response.status_code == 404
