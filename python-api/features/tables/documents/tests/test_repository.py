# ROSETIC:crud-guid



"""
Unit tests for the DocumentRepository CRUD operations.
"""
import pytest

import base64


from unittest.mock import AsyncMock, MagicMock, patch
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, DataError, OperationalError, SQLAlchemyError

from core.exceptions import DatabaseException
from core.pagination import PaginationRequest
from features.tables.documents.models import DocumentModel
from features.tables.documents.schemas import DocumentFilter
from features.tables.documents.repository import DocumentRepository

class TestDocumentRepository:
    """Test cases for DocumentRepository CRUD operations."""

    # ─── Create operations tests ──────────────────────────────────
    @pytest.mark.asyncio
    async def test_create_document_success(self, mock_session_async, sample_data, document_repository):
        """Test successful Document creation."""
        
        # Arrange
        new_item = DocumentModel(**sample_data)       
        
        # Act
        result = await document_repository.create(new_item)
        
        # Assert
        assert isinstance(result, DocumentModel)
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
    async def test_create_document_database_errors(self, mock_session_async, exception_type, expected_status, expected_message, document_repository):
        """Test Document creation with various database errors."""        
        # Mock the database error
        mock_session_async.commit.side_effect = exception_type(None, None, None)

        with pytest.raises(DatabaseException) as e:
            await document_repository.create(DocumentModel())
        
        # Verify the custom exception details
        assert e.value.status_code == expected_status
        assert expected_message in str(e.value)

    # ─── Read operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_get_document_by_id_success(self, mock_session_async, existing_document, document_repository):
        """Test successful retrieval of Document by ID."""
        
        # Arrange
        expected_result = existing_document
        mock_result = MagicMock()
        mock_result.unique.return_value.scalars.return_value.first.return_value = expected_result
        mock_session_async.execute.return_value = mock_result
        
        # Act
        result = await document_repository.get_by_id(1)
        
        # Assert
        assert result == expected_result
        mock_session_async.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_document_by_id_not_found(self, mock_session_async, document_repository):
        """Test retrieval of non-existent Document."""
        
        # Arrange
        mock_result = MagicMock()
        mock_result.unique.return_value.scalars.return_value.first.return_value = None
        mock_session_async.execute.return_value = mock_result
        
        # Act
        result = await document_repository.get_by_id(999)
        
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
    async def test_get_document_by_id_database_errors(self, mock_session_async, exception_type, expected_status, expected_message, document_repository):
        """Test get_document_by_id with various database errors."""
        
        # Mock the database error
        mock_session_async.execute.side_effect = exception_type(None, None, None)

        with pytest.raises(DatabaseException) as e:
            await document_repository.get_by_id(1)
        
        # Verify the custom exception details
        assert e.value.status_code == expected_status
        assert expected_message in str(e.value)

    @pytest.mark.asyncio
    async def test_get_all_success(self, mock_session_async, multiple_documents, pagination_request, document_repository):
        """Test successful retrieval of all Document."""
        
        # Arrange
        mock_session_async.scalar.return_value = len(multiple_documents)
        
        mock_execute_result = MagicMock()
        mock_execute_result.unique.return_value.scalars.return_value.all.return_value = multiple_documents
        mock_session_async.execute.return_value = mock_execute_result
        
        # Act
        results, total = await document_repository.get_all(pagination_request)
        
        # Assert
        assert results == multiple_documents
        assert total == len(multiple_documents)
        assert mock_session_async.scalar.call_count == 1 
        assert mock_session_async.execute.call_count == 1

    @pytest.mark.asyncio
    @pytest.mark.parametrize("exception_type,expected_status,expected_message", [
        (IntegrityError, 409, "Integrity constraint violated"),
        (DataError, 400, "Invalid data format"),
        (OperationalError, 500, "Database operational error"),
        (SQLAlchemyError, 500, "General database error")
    ])
    async def test_get_all_database_errors(self, mock_session_async, pagination_request, exception_type, expected_status, expected_message, document_repository):
        """Test get_all with various database errors."""
        
        # Mock the database error
        mock_session_async.scalar.side_effect = exception_type(None, None, None)

        with pytest.raises(DatabaseException) as e:
            await document_repository.get_all(pagination_request)
        
        # Verify the custom exception details
        assert e.value.status_code == expected_status
        assert expected_message in str(e.value)

    @pytest.mark.asyncio
    async def test_search_success(self, mock_session_async, multiple_documents, pagination_request, document_repository):
        """Test successful search with filters."""
        
        # Arrange
        filters = DocumentFilter()
        
        mock_session_async.scalar.return_value = len(multiple_documents) # Total count
        mock_execute_result = MagicMock()
        mock_execute_result.unique.return_value.scalars.return_value.all.return_value = multiple_documents
        mock_session_async.execute.return_value = mock_execute_result
        
        # Act
        results, total = await document_repository.search(filters, pagination_request)
        
        # Assert
        assert results == multiple_documents
        assert total == len(multiple_documents)
        assert mock_session_async.scalar.call_count == 1
        assert mock_session_async.execute.call_count == 1

    @pytest.mark.asyncio
    @pytest.mark.parametrize("exception_type,expected_status,expected_message", [
        (IntegrityError, 409, "Integrity constraint violated"),
        (DataError, 400, "Invalid data format"),
        (OperationalError, 500, "Database operational error"),
        (SQLAlchemyError, 500, "General database error")
    ])
    async def test_search_database_errors(self, mock_session_async, pagination_request, exception_type, expected_status, expected_message, document_repository):
        """Test search with various database errors."""
        
        # Mock the database error
        mock_session_async.scalar.side_effect = exception_type(None, None, None)

        with pytest.raises(DatabaseException) as e:
            await document_repository.search(DocumentFilter(), pagination_request)
        
        # Verify the custom exception details
        assert e.value.status_code == expected_status
        assert expected_message in str(e.value)

    # ─── Update operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_update_by_id_success(self, mock_session_async, existing_document, updated_document, document_repository):
        """Test successful Document update."""
        
        # Arrange
        
        mock_execute_result = MagicMock()
        mock_execute_result.unique.return_value.scalars.return_value.first.return_value = existing_document
        
        mock_session_async.execute.return_value = mock_execute_result

        updates = updated_document.model_dump(exclude_unset=True)
        # Act
        result = await document_repository.update_by_id(1, updates)
        
        # Assert
        for key, value in updates.items():
            assert getattr(result, key) == value
        mock_session_async.execute.assert_called_once()
        mock_session_async.commit.assert_called_once()
        mock_session_async.refresh.assert_called_once_with(existing_document)

    @pytest.mark.asyncio
    async def test_update_by_id_not_found(self, mock_session_async, document_repository):
        """Test update of non-existent Document."""
        
        # Arrange
        updates = {}
        mock_execute_result = MagicMock()
        mock_execute_result.unique.return_value.scalars.return_value.first.return_value = None
        mock_session_async.execute.return_value = mock_execute_result
        
        # Act
        result = await document_repository.update_by_id(999, updates)
        
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
    async def test_update_by_id_database_errors(self, mock_session_async, exception_type, expected_status, expected_message, document_repository):
        """Test update_by_id with various database errors."""
        
        # Arrange
        updates = {}
        mock_session_async.execute.side_effect = exception_type(None, None, None)

        # Act
        with pytest.raises(DatabaseException) as e:
            await document_repository.update_by_id(1, updates)
        
        # Assert
        assert e.value.status_code == expected_status
        assert expected_message in str(e.value)

    # ─── Delete operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_delete_by_id_success(self, mock_session_async, existing_document, document_repository):
        """Test successful Document deletion."""
        
        # Arrange
        mock_execute_result = MagicMock()
        mock_execute_result.unique.return_value.scalars.return_value.first.return_value = existing_document
        mock_session_async.execute.return_value = mock_execute_result
        
        # Act
        result = await document_repository.delete_by_id(1)
        
        # Assert
        assert result is True
        mock_session_async.execute.assert_called_once()
        mock_session_async.delete.assert_called_once_with(existing_document)
        mock_session_async.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_by_id_not_found(self, mock_session_async, document_repository):
        """Test deletion of non-existent Document."""
        
        # Arrange
        mock_execute_result = MagicMock()
        mock_execute_result.unique.return_value.scalars.return_value.first.return_value = None
        mock_session_async.execute.return_value = mock_execute_result
        
        # Act
        result = await document_repository.delete_by_id(999)
        
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
    async def test_delete_by_id_database_errors(self, mock_session_async, exception_type, expected_status, expected_message, document_repository):
        """Test delete_by_id with various database errors."""
        
        # Arrange
        mock_session_async.execute.side_effect = exception_type(None, None, None)

        # Act
        with pytest.raises(DatabaseException) as e:
            await document_repository.delete_by_id(1)
        
        # Assert
        assert e.value.status_code == expected_status
        assert expected_message in str(e.value)
