# ROSETIC:crud-guid


"""
Unit tests for the HolidayCalendarService layer.
"""

from pydantic import ValidationError
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from decimal import Decimal
from sqlalchemy.exc import SQLAlchemyError

from core.pagination import PaginatedResponse
from features.tables.holiday_calendar.models import HolidayCalendarModel
from features.tables.holiday_calendar.schemas import HolidayCalendarResponse, HolidayCalendarCreate, HolidayCalendarUpdate, HolidayCalendarFilter
from features.tables.holiday_calendar.service import HolidayCalendarService
from features.tables.holiday_calendar.repository import HolidayCalendarRepository

class TestHolidayCalendarService:
    """Test cases for HolidayCalendarService layer."""


    @pytest.fixture
    def mock_repository(self):
        """Create a mock HolidayCalendarRepository."""
        return AsyncMock(spec=HolidayCalendarRepository)

    @pytest.fixture
    def service_with_mock_repo(self, mock_session_async, mock_repository):
        """Create HolidayCalendarService with mocked repository."""
        service = HolidayCalendarService(mock_session_async)
        service.repo = mock_repository
        return service

    # ─── Create operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_create_holiday_calendar_success(self, service_with_mock_repo, mock_repository, sample_data, existing_holiday_calendar):
        """Test successful holiday_calendar creation through service."""
        # Arrange
        new_item = HolidayCalendarCreate(**sample_data)
        mock_repository.create.return_value = existing_holiday_calendar
        
        # Act
        result = await service_with_mock_repo.create(new_item)
        
        # Assert
        assert isinstance(result, HolidayCalendarResponse)
        mock_repository.create.assert_called_once()

    # # ─── Read operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_get_holiday_calendar_by_id_success(self, service_with_mock_repo, mock_repository, existing_holiday_calendar):
        """Test successful retrieval of holiday_calendar by ID."""
        # Arrange
        mock_repository.get_by_id.return_value = existing_holiday_calendar
        
        # Act
        result = await service_with_mock_repo.get_by_id(1)
        
        # Assert
        assert isinstance(result, HolidayCalendarResponse)
        mock_repository.get_by_id.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_get_holiday_calendar_by_id_not_found(self, service_with_mock_repo, mock_repository):
        """Test retrieval of non-existent holiday_calendar."""
        # Arrange
        mock_repository.get_by_id.return_value = None
        
        # Act
        result = await service_with_mock_repo.get_by_id(999)
        
        # Assert
        assert result is None
        mock_repository.get_by_id.assert_called_once_with(999)

    @pytest.mark.asyncio
    async def test_get_all_success(self, service_with_mock_repo, mock_repository, multiple_holiday_calendar, pagination_request):
        """Test successful retrieval of all holiday_calendar."""
        # Arrange
        mock_repository.get_all.return_value = (multiple_holiday_calendar, len(multiple_holiday_calendar))
        
        # Act
        result = await service_with_mock_repo.get_all(pagination_request)
        
        # Assert
        assert isinstance(result, PaginatedResponse)
        assert len(result.items) == len(multiple_holiday_calendar)
        assert result.total == len(multiple_holiday_calendar)
        mock_repository.get_all.assert_called_once_with(pagination_request)

    

    @pytest.mark.asyncio
    async def test_search_success(self, service_with_mock_repo, mock_repository, multiple_holiday_calendar, pagination_request):
        """Test successful search with filters."""
        # Arrange
        filters = HolidayCalendarFilter()
        mock_repository.search.return_value = (multiple_holiday_calendar, len(multiple_holiday_calendar))
        
        # Act
        result = await service_with_mock_repo.search(filters, pagination_request)
        
        # Assert
        assert isinstance(result, PaginatedResponse)
        assert len(result.items) == len(multiple_holiday_calendar)
        assert result.total == len(multiple_holiday_calendar)
        
        # Verify repository was called with correct filter dict
        mock_repository.search.assert_called_once_with(filters, pagination_request)

    @pytest.mark.asyncio
    async def test_search_empty_results(self, service_with_mock_repo, mock_repository, pagination_request):
        """Test search with no matching results."""
        # Arrange
        filters = HolidayCalendarFilter()
        mock_repository.search.return_value = ([], 0)
        
        # Act
        result = await service_with_mock_repo.search(filters, pagination_request)
        
        # Assert
        assert isinstance(result, PaginatedResponse)
        assert len(result.items) == 0
        assert result.total == 0
        mock_repository.search.assert_called_once_with(filters, pagination_request)

    # # ─── Update operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_update_holiday_calendar_by_id_success(self, service_with_mock_repo, mock_repository, updated_holiday_calendar_model):
        """Test successful holiday_calendar update."""
        # Arrange
        mock_repository.update_by_id.return_value = updated_holiday_calendar_model
        
        # Act
        result = await service_with_mock_repo.update_by_id(1, HolidayCalendarUpdate())
        
        # Assert
        assert isinstance(result, HolidayCalendarResponse)
        mock_repository.update_by_id.assert_called_once_with(1, HolidayCalendarUpdate().model_dump(exclude_unset=True))

    # # ─── Delete operations tests ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_delete_by_id_success(self, service_with_mock_repo, mock_repository):
        """Test successful holiday_calendar deletion."""
        # Arrange
        mock_repository.delete_by_id.return_value = True
        
        # Act
        result = await service_with_mock_repo.delete_by_id(1)
        
        # Assert
        assert result is True
        mock_repository.delete_by_id.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_delete_by_id_not_found(self, service_with_mock_repo, mock_repository):
        """Test deletion of non-existent holiday_calendar."""
        # Arrange
        mock_repository.delete_by_id.return_value = False
        
        # Act
        result = await service_with_mock_repo.delete_by_id(999)
        
        # Assert
        assert result is False
        mock_repository.delete_by_id.assert_called_once_with(999)
