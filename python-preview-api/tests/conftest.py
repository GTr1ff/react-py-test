"""
Shared test utilities and fixtures for all test modules.
"""
import datetime
import logging
from typing import Generator
from unittest.mock import patch, AsyncMock, MagicMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

logging.disable(logging.CRITICAL)

def get_test_time():
    """Get consistent time for testing."""
    return datetime.datetime(2025, 1, 1, 12, 0, 0, tzinfo=datetime.timezone.utc)

def get_test_date():
    """Get consistent date for testing."""
    return datetime.date(2025, 1, 1)

@pytest.fixture
def mock_db() -> MagicMock:
    """Create a mock Database instance for use as app.state.db."""
    db = MagicMock()
    db.engine = MagicMock()
    db.session_factory = MagicMock()
    db.initialize = AsyncMock()
    db.dispose = AsyncMock()
    return db

@pytest.fixture
def test_app(mock_db: MagicMock) -> Generator[FastAPI, None, None]:
    """Create a test app whose lifespan installs a mocked Database on app.state.db."""
    with patch("main.Database", return_value=mock_db):
        from main import create_app
        app = create_app()

        yield app

@pytest.fixture
def client(test_app: FastAPI) -> Generator[TestClient, None, None]:
    with TestClient(test_app, raise_server_exceptions=False) as test_client:
        yield test_client
