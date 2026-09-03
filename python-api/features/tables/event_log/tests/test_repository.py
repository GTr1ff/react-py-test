# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c



"""
Unit tests for the EventLogRepository CRUD operations.
"""
import pytest


import datetime

from unittest.mock import AsyncMock, MagicMock, patch
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, DataError, OperationalError, SQLAlchemyError

from tests.conftest import get_test_time, get_test_date
from core.exceptions import DatabaseException
from core.pagination import PaginationRequest
from features.tables.event_log.models import EventLogModel
from features.tables.event_log.schemas import EventLogFilter
from features.tables.event_log.repository import EventLogRepository

class TestEventLogRepository:
    """Test cases for EventLogRepository CRUD operations."""

    # ─── Create operations tests ──────────────────────────────────
    @pytest.mark.asyncio
    async def test_create_event_log_success(self, mock_session_async, sample_data, event_log_repository):
        """Test successful EventLog creation."""
        
        # Arrange
        new_item = EventLogModel(**sample_data)       
        
        # Act
        result = await event_log_repository.create(new_item)
        
        # Assert
        assert isinstance(result, EventLogModel)
        mock_session_async.add.assert_called_once_with(new_item)
        mock_session_async.commit.assert_called_once()
        mock_session_async.refresh.assert_called_once_with(new_item)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("exception_type,expected_status,expected_message", [
        (IntegrityError, 409, "Integrity constraint violated"),
        (DataError, 400, "Invalid data format"),
        (OperationalError, 500, "Database operational error"),
        (SQLAlchemyError, 500, "General database error")
    ])
    async def test_create_event_log_database_errors(self, mock_session_async, exception_type, expected_status, expected_message, event_log_repository):
        """Test EventLog creation with various database errors."""        
        # Mock the database error
        mock_session_async.commit.side_effect = exception_type(None, None, None)

        with pytest.raises(DatabaseException) as e:
            await event_log_repository.create(EventLogModel())
        
        # Verify the custom exception details
        assert e.value.status_code == expected_status
        assert expected_message in str(e.value)

    # ─── Read operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_get_event_log_by_id_success(self, mock_session_async, existing_event_log, event_log_repository):
        """Test successful retrieval of EventLog by ID."""
        
        # Arrange
        expected_result = existing_event_log
        mock_result = MagicMock()
        mock_result.unique.return_value.scalars.return_value.first.return_value = expected_result
        mock_session_async.execute.return_value = mock_result
        
        # Act
        result = await event_log_repository.get_by_id(1)
        
        # Assert
        assert result == expected_result
        mock_session_async.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_event_log_by_id_not_found(self, mock_session_async, event_log_repository):
        """Test retrieval of non-existent EventLog."""
        
        # Arrange
        mock_result = MagicMock()
        mock_result.unique.return_value.scalars.return_value.first.return_value = None
        mock_session_async.execute.return_value = mock_result
        
        # Act
        result = await event_log_repository.get_by_id(999)
        
        # Assert
        assert result is None
        mock_session_async.execute.assert_called_once()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("exception_type,expected_status,expected_message", [
        (IntegrityError, 409, "Integrity constraint violated"),
        (DataError, 400, "Invalid data format"),
        (OperationalError, 500, "Database operational error"),
        (SQLAlchemyError, 500, "General database error")
    ])
    async def test_get_event_log_by_id_database_errors(self, mock_session_async, exception_type, expected_status, expected_message, event_log_repository):
        """Test get_event_log_by_id with various database errors."""
        
        # Mock the database error
        mock_session_async.execute.side_effect = exception_type(None, None, None)

        with pytest.raises(DatabaseException) as e:
            await event_log_repository.get_by_id(1)
        
        # Verify the custom exception details
        assert e.value.status_code == expected_status
        assert expected_message in str(e.value)

    @pytest.mark.asyncio
    async def test_get_all_success(self, mock_session_async, multiple_event_log, pagination_request, event_log_repository):
        """Test successful retrieval of all EventLog."""
        
        # Arrange
        mock_session_async.scalar.return_value = len(multiple_event_log)
        
        mock_execute_result = MagicMock()
        mock_execute_result.unique.return_value.scalars.return_value.all.return_value = multiple_event_log
        mock_session_async.execute.return_value = mock_execute_result
        
        # Act
        results, total = await event_log_repository.get_all(pagination_request)
        
        # Assert
        assert results == multiple_event_log
        assert total == len(multiple_event_log)
        assert mock_session_async.scalar.call_count == 1 
        assert mock_session_async.execute.call_count == 1

    @pytest.mark.asyncio
    @pytest.mark.parametrize("exception_type,expected_status,expected_message", [
        (IntegrityError, 409, "Integrity constraint violated"),
        (DataError, 400, "Invalid data format"),
        (OperationalError, 500, "Database operational error"),
        (SQLAlchemyError, 500, "General database error")
    ])
    async def test_get_all_database_errors(self, mock_session_async, pagination_request, exception_type, expected_status, expected_message, event_log_repository):
        """Test get_all with various database errors."""
        
        # Mock the database error
        mock_session_async.scalar.side_effect = exception_type(None, None, None)

        with pytest.raises(DatabaseException) as e:
            await event_log_repository.get_all(pagination_request)
        
        # Verify the custom exception details
        assert e.value.status_code == expected_status
        assert expected_message in str(e.value)

    @pytest.mark.asyncio
    async def test_search_success(self, mock_session_async, multiple_event_log, pagination_request, event_log_repository):
        """Test successful search with filters."""
        
        # Arrange
        filters = EventLogFilter()
        
        mock_session_async.scalar.return_value = len(multiple_event_log) # Total count
        mock_execute_result = MagicMock()
        mock_execute_result.unique.return_value.scalars.return_value.all.return_value = multiple_event_log
        mock_session_async.execute.return_value = mock_execute_result
        
        # Act
        results, total = await event_log_repository.search(filters, pagination_request)
        
        # Assert
        assert results == multiple_event_log
        assert total == len(multiple_event_log)
        assert mock_session_async.scalar.call_count == 1
        assert mock_session_async.execute.call_count == 1

    @pytest.mark.asyncio
    @pytest.mark.parametrize("exception_type,expected_status,expected_message", [
        (IntegrityError, 409, "Integrity constraint violated"),
        (DataError, 400, "Invalid data format"),
        (OperationalError, 500, "Database operational error"),
        (SQLAlchemyError, 500, "General database error")
    ])
    async def test_search_database_errors(self, mock_session_async, pagination_request, exception_type, expected_status, expected_message, event_log_repository):
        """Test search with various database errors."""
        
        # Mock the database error
        mock_session_async.scalar.side_effect = exception_type(None, None, None)

        with pytest.raises(DatabaseException) as e:
            await event_log_repository.search(EventLogFilter(), pagination_request)
        
        # Verify the custom exception details
        assert e.value.status_code == expected_status
        assert expected_message in str(e.value)

    # ─── Update operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_update_by_id_success(self, mock_session_async, existing_event_log, updated_event_log, event_log_repository):
        """Test successful EventLog update."""
        
        # Arrange
        
        mock_execute_result = MagicMock()
        mock_execute_result.unique.return_value.scalars.return_value.first.return_value = existing_event_log
        
        mock_session_async.execute.return_value = mock_execute_result

        updates = updated_event_log.model_dump(exclude_unset=True)
        # Act
        result = await event_log_repository.update_by_id(1, updates)
        
        # Assert
        for key, value in updates.items():
            assert getattr(result, key) == value
        mock_session_async.execute.assert_called_once()
        mock_session_async.commit.assert_called_once()
        mock_session_async.refresh.assert_called_once_with(existing_event_log)

    @pytest.mark.asyncio
    async def test_update_by_id_not_found(self, mock_session_async, event_log_repository):
        """Test update of non-existent EventLog."""
        
        # Arrange
        updates = {}
        mock_execute_result = MagicMock()
        mock_execute_result.unique.return_value.scalars.return_value.first.return_value = None
        mock_session_async.execute.return_value = mock_execute_result
        
        # Act
        result = await event_log_repository.update_by_id(999, updates)
        
        # Assert
        assert result is None
        mock_session_async.execute.assert_called_once()
        mock_session_async.commit.assert_not_called()
        mock_session_async.refresh.assert_not_called()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("exception_type,expected_status,expected_message", [
        (IntegrityError, 409, "Integrity constraint violated"),
        (DataError, 400, "Invalid data format"),
        (OperationalError, 500, "Database operational error"),
        (SQLAlchemyError, 500, "General database error")
    ])
    async def test_update_by_id_database_errors(self, mock_session_async, exception_type, expected_status, expected_message, event_log_repository):
        """Test update_by_id with various database errors."""
        
        # Arrange
        updates = {}
        mock_session_async.execute.side_effect = exception_type(None, None, None)

        # Act
        with pytest.raises(DatabaseException) as e:
            await event_log_repository.update_by_id(1, updates)
        
        # Assert
        assert e.value.status_code == expected_status
        assert expected_message in str(e.value)

    # ─── Delete operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_delete_by_id_success(self, mock_session_async, existing_event_log, event_log_repository):
        """Test successful EventLog deletion."""
        
        # Arrange
        mock_execute_result = MagicMock()
        mock_execute_result.unique.return_value.scalars.return_value.first.return_value = existing_event_log
        mock_session_async.execute.return_value = mock_execute_result
        
        # Act
        result = await event_log_repository.delete_by_id(1)
        
        # Assert
        assert result is True
        mock_session_async.execute.assert_called_once()
        mock_session_async.delete.assert_called_once_with(existing_event_log)
        mock_session_async.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_by_id_not_found(self, mock_session_async, event_log_repository):
        """Test deletion of non-existent EventLog."""
        
        # Arrange
        mock_execute_result = MagicMock()
        mock_execute_result.unique.return_value.scalars.return_value.first.return_value = None
        mock_session_async.execute.return_value = mock_execute_result
        
        # Act
        result = await event_log_repository.delete_by_id(999)
        
        # Assert
        assert result is False
        mock_session_async.execute.assert_called_once()
        mock_session_async.delete.assert_not_called()
        mock_session_async.commit.assert_not_called()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("exception_type,expected_status,expected_message", [
        (IntegrityError, 409, "Integrity constraint violated"),
        (DataError, 400, "Invalid data format"),
        (OperationalError, 500, "Database operational error"),
        (SQLAlchemyError, 500, "General database error")
    ])
    async def test_delete_by_id_database_errors(self, mock_session_async, exception_type, expected_status, expected_message, event_log_repository):
        """Test delete_by_id with various database errors."""
        
        # Arrange
        mock_session_async.execute.side_effect = exception_type(None, None, None)

        # Act
        with pytest.raises(DatabaseException) as e:
            await event_log_repository.delete_by_id(1)
        
        # Assert
        assert e.value.status_code == expected_status
        assert expected_message in str(e.value)
