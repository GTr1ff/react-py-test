# ROSETIC:crud-guid



from typing import Any
from core.logging.repository_logger import log_repository_call
from core.db_exception_handler import handle_db_exceptions_async
from core.pagination import PaginationRequest, apply_filters, apply_pagination_filter
from features.tables.holiday_calendar.models import HolidayCalendarModel
from features.tables.holiday_calendar.schemas import HolidayCalendarFilter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

class HolidayCalendarRepository:
    """Repository layer for all HolidayCalendar-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
    
    # ─── Create operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("HolidayCalendar")
    async def create(self, holidaycalendar_record: HolidayCalendarModel) -> HolidayCalendarModel | None:
        """
        Create a new HolidayCalendar

        Args:
            data: New HolidayCalendar data
            
        Returns:
            HolidayCalendar data if created successfully, None if HolidayCalendar already exists
        """
        
        # Create new HolidayCalendar
        self.session.add(holidaycalendar_record)
        await self.session.commit()
        await self.session.refresh(holidaycalendar_record)

        return holidaycalendar_record

    
    # ─── Read operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("HolidayCalendar")
    async def get_by_id(self, id: int) -> HolidayCalendarModel | None:
        """
        Get holiday_calendar by id
        
        Args:
            id: The id to search for
            
        Returns:
            HolidayCalendar if found, None otherwise
        """
        stmt = select(HolidayCalendarModel).where(HolidayCalendarModel.holiday_id == id)
        result = await self.session.execute(stmt)
        return result.unique().scalars().first()

    @handle_db_exceptions_async
    @log_repository_call("HolidayCalendar")
    async def get_all(self, pagination: PaginationRequest) -> tuple[list[HolidayCalendarModel], int]:
        """
        Get all holiday_calendar
        
        Returns:
            List of all holiday_calendar
        """
        stmt = select(HolidayCalendarModel)

        total = await self.session.scalar(select(func.count(HolidayCalendarModel.holiday_id)))
        stmt = apply_pagination_filter(stmt, pagination, HolidayCalendarModel)

        result = await self.session.execute(stmt)
        records = result.unique().scalars().all()
        return records, total
    
    @handle_db_exceptions_async
    @log_repository_call("HolidayCalendar")
    async def search(self, filters: HolidayCalendarFilter, pagination: PaginationRequest) -> tuple[list[HolidayCalendarModel], int]:
        stmt = select(HolidayCalendarModel)
        stmt = apply_filters(stmt, filters, HolidayCalendarModel)

        total = await self.session.scalar(select(func.count()).select_from(stmt.subquery()))
        stmt = apply_pagination_filter(stmt, pagination, HolidayCalendarModel)

        results = await self.session.execute(stmt)
        records = results.unique().scalars().all()
        return records, total


    # ─── Update operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("HolidayCalendar")
    async def update_by_id(self, id: int, updates: dict[str, Any]) -> HolidayCalendarModel | None:
        """
        Update HolidayCalendar information
        
        Args:
            id: id of HolidayCalendar to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated HolidayCalendar if successful, None if HolidayCalendar not found
        """
        stmt = select(HolidayCalendarModel).where(HolidayCalendarModel.holiday_id == id)
        result = await self.session.execute(stmt)
        record = result.unique().scalars().first()
        if record:
            for key, value in updates.items():
                setattr(record, key, value)
            await self.session.commit()
            await self.session.refresh(record)

        return record
    
    # ─── Delete operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("HolidayCalendar")
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a HolidayCalendar
        
        Args:
            id: id of HolidayCalendar to delete
            
        Returns:
            True if user was deleted, False if user not found
        """
        stmt = select(HolidayCalendarModel).where(HolidayCalendarModel.holiday_id == id)
        result = await self.session.execute(stmt)
        record = result.unique().scalars().first()
        if record:
            await self.session.delete(record)
            await self.session.commit()
            return True
        return False
