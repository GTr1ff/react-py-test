from fastapi import FastAPI
from fastapi.testclient import TestClient
from core.exceptions import DatabaseException

class TestMainApp:
    """Test main FastAPI application configuration and behavior."""
     
    def test_database_exception_handler(self, test_app: FastAPI, client: TestClient):
        """Test the custom database exception handler."""
        # Arrange
        @test_app.get("/test-db-error")
        async def test_db_error():
            raise DatabaseException("Test database error", status_code=500)

        # Act
        response = client.get("/test-db-error")

        # Assert
        assert response.status_code == 500
        assert response.json() == {"error": "Test database error"}
    
    def test_app_has_exception_handlers(self, test_app: FastAPI):
        """Test that exception handlers are properly registered."""
        # Assert
        assert DatabaseException in test_app.exception_handlers
        assert callable(test_app.exception_handlers[DatabaseException])

    def test_app_metadata(self, test_app: FastAPI):
        """Test that app metadata is properly set."""
        assert test_app.title == "Tastebot2"
        assert test_app.version == "1.0.0"
        assert "FOA architecture" in test_app.description
