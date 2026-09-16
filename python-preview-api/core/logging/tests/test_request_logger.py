import pytest
from unittest.mock import Mock, patch, AsyncMock

from core.logging.request_logger import (
    RequestLoggerMiddleware
)

class TestRequestLoggerMiddleware:
    """Test cases for RequestLoggingMiddleware error scenarios and integration."""
    
    @pytest.fixture
    def mock_request(self):
        """Create a mock request for testing."""
        mock_request = Mock()
        mock_request.client = Mock()
        mock_request.client.host = "192.0.2.0/24"
        mock_request.url = Mock()
        mock_request.url.hostname = "example.com"
        mock_request.url.path = "/test"
        mock_request.method = "GET"
        mock_request.headers = {"content-type": "application/json", "authorization": "Bearer 1234567890"}
        mock_request.state = Mock()
        return mock_request
    
    @pytest.fixture
    def mock_response(self):
        """Create a mock response for testing."""
        mock_response = Mock()
        mock_response.status_code = 200
        return mock_response
    
    @pytest.fixture
    def middleware(self):
        """Create middleware instance for testing."""
        mock_base_http_middleware = Mock()
        middleware = RequestLoggerMiddleware(mock_base_http_middleware)
        middleware._logger = Mock()
        return middleware
    
    @pytest.mark.asyncio
    async def test_middleware_calls_next_with_correct_request(self, middleware, mock_request, mock_response):
        """Test that middleware calls call_next with the correct request object."""
        # Arrange
        mock_request.body = AsyncMock(return_value='{"data": "test"}')
        call_next = AsyncMock(return_value=mock_response)
        
        # Act
        response = await middleware.dispatch(mock_request, call_next)
        
        # Assert
        call_next.assert_called_once_with(mock_request)
        assert response == mock_response
    