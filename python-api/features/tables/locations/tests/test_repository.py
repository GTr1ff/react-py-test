# ROSETIC:crud-guid



"""
Unit tests for the LocationRepository CRUD operations.
"""
import pytest




from unittest.mock import AsyncMock, MagicMock, patch
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, DataError, OperationalError, SQLAlchemyError

from core.exceptions import DatabaseException
from core.pagination import PaginationRequest
from features.tables.locations.models import LocationModel
from features.tables.locations.schemas import LocationFilter
from features.tables.locations.repository import LocationRepository

class TestLocationRepository:
    """Test cases for LocationRepository CRUD operations."""

    # ─── Create operations tests ──────────────────────────────────
    @pytest.mark.asyncio
    async def test_create_location_success(self, mock_session_async, sample_data, location_repository):
        """Test successful Location creation."""
        
        # Arrange
        new_item = LocationModel(**sample_data)       
        
        # Act
        result = await location_repository.create(new_item)
        
        # Assert
        assert isinstance(result, LocationModel)
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
    async def test_create_location_database_errors(self, mock_session_async, exception_type, expected_status, expected_message, location_repository):
        """Test Location creation with various database errors."""        
        # Mock the database error
        mock_session_async.commit.side_effect = exception_type(None, None, None)

        with pytest.raises(DatabaseException) as e:
            await location_repository.create(LocationModel())
        
        # Verify the custom exception details
        assert e.value.status_code == expected_status
        assert expected_message in str(e.value)

    # ─── Read operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_get_location_by_id_success(self, mock_session_async, existing_location, location_repository):
        """Test successful retrieval of Location by ID."""
        
        # Arrange
        expected_result = existing_location
        mock_result = MagicMock()
        mock_result.unique.return_value.scalars.return_value.first.return_value = expected_result
        mock_session_async.execute.return_value = mock_result
        
        # Act
        result = await location_repository.get_by_id(1)
        
        # Assert
        assert result == expected_result
        mock_session_async.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_location_by_id_not_found(self, mock_session_async, location_repository):
        """Test retrieval of non-existent Location."""
        
        # Arrange
        mock_result = MagicMock()
        mock_result.unique.return_value.scalars.return_value.first.return_value = None
        mock_session_async.execute.return_value = mock_result
        
        # Act
        result = await location_repository.get_by_id(999)
        
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
    async def test_get_location_by_id_database_errors(self, mock_session_async, exception_type, expected_status, expected_message, location_repository):
        """Test get_location_by_id with various database errors."""
        
        # Mock the database error
        mock_session_async.execute.side_effect = exception_type(None, None, None)

        with pytest.raises(DatabaseException) as e:
            await location_repository.get_by_id(1)
        
        # Verify the custom exception details
        assert e.value.status_code == expected_status
        assert expected_message in str(e.value)

    @pytest.mark.asyncio
    async def test_get_all_success(self, mock_session_async, multiple_locations, pagination_request, location_repository):
        """Test successful retrieval of all Location."""
        
        # Arrange
        mock_session_async.scalar.return_value = len(multiple_locations)
        
        mock_execute_result = MagicMock()
        mock_execute_result.unique.return_value.scalars.return_value.all.return_value = multiple_locations
        mock_session_async.execute.return_value = mock_execute_result
        
        # Act
        results, total = await location_repository.get_all(pagination_request)
        
        # Assert
        assert results == multiple_locations
        assert total == len(multiple_locations)
        assert mock_session_async.scalar.call_count == 1 
        assert mock_session_async.execute.call_count == 1

    @pytest.mark.asyncio
    @pytest.mark.parametrize("exception_type,expected_status,expected_message", [
        (IntegrityError, 409, "Integrity constraint violated"),
        (DataError, 400, "Invalid data format"),
        (OperationalError, 500, "Database operational error"),
        (SQLAlchemyError, 500, "General database error")
    ])
    async def test_get_all_database_errors(self, mock_session_async, pagination_request, exception_type, expected_status, expected_message, location_repository):
        """Test get_all with various database errors."""
        
        # Mock the database error
        mock_session_async.scalar.side_effect = exception_type(None, None, None)

        with pytest.raises(DatabaseException) as e:
            await location_repository.get_all(pagination_request)
        
        # Verify the custom exception details
        assert e.value.status_code == expected_status
        assert expected_message in str(e.value)

    @pytest.mark.asyncio
    async def test_search_success(self, mock_session_async, multiple_locations, pagination_request, location_repository):
        """Test successful search with filters."""
        
        # Arrange
        filters = LocationFilter()
        
        mock_session_async.scalar.return_value = len(multiple_locations) # Total count
        mock_execute_result = MagicMock()
        mock_execute_result.unique.return_value.scalars.return_value.all.return_value = multiple_locations
        mock_session_async.execute.return_value = mock_execute_result
        
        # Act
        results, total = await location_repository.search(filters, pagination_request)
        
        # Assert
        assert results == multiple_locations
        assert total == len(multiple_locations)
        assert mock_session_async.scalar.call_count == 1
        assert mock_session_async.execute.call_count == 1

    @pytest.mark.asyncio
    @pytest.mark.parametrize("exception_type,expected_status,expected_message", [
        (IntegrityError, 409, "Integrity constraint violated"),
        (DataError, 400, "Invalid data format"),
        (OperationalError, 500, "Database operational error"),
        (SQLAlchemyError, 500, "General database error")
    ])
    async def test_search_database_errors(self, mock_session_async, pagination_request, exception_type, expected_status, expected_message, location_repository):
        """Test search with various database errors."""
        
        # Mock the database error
        mock_session_async.scalar.side_effect = exception_type(None, None, None)

        with pytest.raises(DatabaseException) as e:
            await location_repository.search(LocationFilter(), pagination_request)
        
        # Verify the custom exception details
        assert e.value.status_code == expected_status
        assert expected_message in str(e.value)

    # ─── Update operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_update_by_id_success(self, mock_session_async, existing_location, updated_location, location_repository):
        """Test successful Location update."""
        
        # Arrange
        
        mock_execute_result = MagicMock()
        mock_execute_result.unique.return_value.scalars.return_value.first.return_value = existing_location
        
        mock_session_async.execute.return_value = mock_execute_result

        updates = updated_location.model_dump(exclude_unset=True)
        # Act
        result = await location_repository.update_by_id(1, updates)
        
        # Assert
        for key, value in updates.items():
            assert getattr(result, key) == value
        mock_session_async.execute.assert_called_once()
        mock_session_async.commit.assert_called_once()
        mock_session_async.refresh.assert_called_once_with(existing_location)

    @pytest.mark.asyncio
    async def test_update_by_id_not_found(self, mock_session_async, location_repository):
        """Test update of non-existent Location."""
        
        # Arrange
        updates = {}
        mock_execute_result = MagicMock()
        mock_execute_result.unique.return_value.scalars.return_value.first.return_value = None
        mock_session_async.execute.return_value = mock_execute_result
        
        # Act
        result = await location_repository.update_by_id(999, updates)
        
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
    async def test_update_by_id_database_errors(self, mock_session_async, exception_type, expected_status, expected_message, location_repository):
        """Test update_by_id with various database errors."""
        
        # Arrange
        updates = {}
        mock_session_async.execute.side_effect = exception_type(None, None, None)

        # Act
        with pytest.raises(DatabaseException) as e:
            await location_repository.update_by_id(1, updates)
        
        # Assert
        assert e.value.status_code == expected_status
        assert expected_message in str(e.value)

    # ─── Delete operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_delete_by_id_success(self, mock_session_async, existing_location, location_repository):
        """Test successful Location deletion."""
        
        # Arrange
        mock_execute_result = MagicMock()
        mock_execute_result.unique.return_value.scalars.return_value.first.return_value = existing_location
        mock_session_async.execute.return_value = mock_execute_result
        
        # Act
        result = await location_repository.delete_by_id(1)
        
        # Assert
        assert result is True
        mock_session_async.execute.assert_called_once()
        mock_session_async.delete.assert_called_once_with(existing_location)
        mock_session_async.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_by_id_not_found(self, mock_session_async, location_repository):
        """Test deletion of non-existent Location."""
        
        # Arrange
        mock_execute_result = MagicMock()
        mock_execute_result.unique.return_value.scalars.return_value.first.return_value = None
        mock_session_async.execute.return_value = mock_execute_result
        
        # Act
        result = await location_repository.delete_by_id(999)
        
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
    async def test_delete_by_id_database_errors(self, mock_session_async, exception_type, expected_status, expected_message, location_repository):
        """Test delete_by_id with various database errors."""
        
        # Arrange
        mock_session_async.execute.side_effect = exception_type(None, None, None)

        # Act
        with pytest.raises(DatabaseException) as e:
            await location_repository.delete_by_id(1)
        
        # Assert
        assert e.value.status_code == expected_status
        assert expected_message in str(e.value)
