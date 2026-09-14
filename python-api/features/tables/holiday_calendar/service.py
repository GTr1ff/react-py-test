# ROSETIC:crud-guid



from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from core.pagination import PaginatedResponse, PaginationRequest
from features.tables.holiday_calendar.models import HolidayCalendarModel
from features.tables.holiday_calendar.schemas import HolidayCalendarResponse, HolidayCalendarCreate, HolidayCalendarUpdate, HolidayCalendarFilter
from features.tables.holiday_calendar.repository import HolidayCalendarRepository

class HolidayCalendarService:
    """Service layer for all HolidayCalendar-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = HolidayCalendarRepository(session)

    
    # ─── Read operations ──────────────────────────────────id
    async def get_by_id(self, id: int) -> HolidayCalendarResponse | None:
        """
        Get holiday_calendar by id
        
        Args:
            id: The id to search for
            
        Returns:
            HolidayCalendarResponse if found, None if not found
        """
        result = await self.repo.get_by_id(id)
        return HolidayCalendarResponse.model_validate(result) if result else None

    async def get_all(self, pagination: PaginationRequest) -> PaginatedResponse[HolidayCalendarResponse]:
        """
        Get all holiday_calendar
        
        Returns:
            List of all holiday_calendar
        """
        result, total = await self.repo.get_all(pagination)

        return PaginatedResponse[HolidayCalendarResponse](
            items=[HolidayCalendarResponse.model_validate(record) for record in result],
            **pagination.model_dump(),
            total=total
        )

    async def search(self, filters: HolidayCalendarFilter, pagination: PaginationRequest) -> PaginatedResponse[HolidayCalendarResponse]:
        results, total = await self.repo.search(filters, pagination)
        return PaginatedResponse[HolidayCalendarResponse](
            items=[HolidayCalendarResponse.model_validate(record) for record in results],
            **pagination.model_dump(),
            total=total
        )


    # ─── Create operations ──────────────────────────────────
    async def create(self, data: HolidayCalendarCreate) -> HolidayCalendarResponse:
        """
        Create a new HolidayCalendar

        Args:
            data: New HolidayCalendar data
            
        Returns:
            HolidayCalendarResponse if created successfully, None if HolidayCalendar already exists
        """

        # Check if unique fields already exist
        holidaycalendar_model = HolidayCalendarModel(**data.model_dump())
        
        # Create
        result = await self.repo.create(holidaycalendar_model)

        return HolidayCalendarResponse.model_validate(result)

    # ─── Update operations ──────────────────────────────────
    async def update_by_id(self, id: int, updates: HolidayCalendarUpdate) -> HolidayCalendarResponse | None:
        """
        Update HolidayCalendar information
        
        Args:
            id: id of HolidayCalendar to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated HolidayCalendarResponse if successful, None if HolidayCalendar not found
        """    
        result = await self.repo.update_by_id(id, updates.model_dump(exclude_unset=True))
        return HolidayCalendarResponse.model_validate(result) if result else None
    
    # ─── Delete operations ──────────────────────────────────
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a HolidayCalendar
        
        Args:
            id: id of HolidayCalendar to delete
            
        Returns:
            True if HolidayCalendar was deleted, False if HolidayCalendar not found
        """
        return await self.repo.delete_by_id(id)
