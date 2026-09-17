# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c



from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from core.pagination import PaginatedResponse, PaginationRequest
from features.tables.event_log.models import EventLogModel
from features.tables.event_log.schemas import EventLogResponse, EventLogCreate, EventLogUpdate, EventLogFilter
from features.tables.event_log.repository import EventLogRepository

class EventLogService:
    """Service layer for all EventLog-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = EventLogRepository(session)

    
    # ─── Read operations ──────────────────────────────────id
    async def get_by_id(self, id: int) -> EventLogResponse | None:
        """
        Get event_log by id
        
        Args:
            id: The id to search for
            
        Returns:
            EventLogResponse if found, None if not found
        """
        result = await self.repo.get_by_id(id)
        return EventLogResponse.model_validate(result) if result else None

    async def get_all(self, pagination: PaginationRequest) -> PaginatedResponse[EventLogResponse]:
        """
        Get all event_log
        
        Returns:
            List of all event_log
        """
        result, total = await self.repo.get_all(pagination)

        return PaginatedResponse[EventLogResponse](
            items=[EventLogResponse.model_validate(record) for record in result],
            **pagination.model_dump(),
            total=total
        )

    async def search(self, filters: EventLogFilter, pagination: PaginationRequest) -> PaginatedResponse[EventLogResponse]:
        results, total = await self.repo.search(filters, pagination)
        return PaginatedResponse[EventLogResponse](
            items=[EventLogResponse.model_validate(record) for record in results],
            **pagination.model_dump(),
            total=total
        )


    # ─── Create operations ──────────────────────────────────
    async def create(self, data: EventLogCreate) -> EventLogResponse:
        """
        Create a new EventLog

        Args:
            data: New EventLog data
            
        Returns:
            EventLogResponse if created successfully, None if EventLog already exists
        """

        # Check if unique fields already exist
        eventlog_model = EventLogModel(**data.model_dump())
        
        # Create
        result = await self.repo.create(eventlog_model)

        return EventLogResponse.model_validate(result)

    # ─── Update operations ──────────────────────────────────
    async def update_by_id(self, id: int, updates: EventLogUpdate) -> EventLogResponse | None:
        """
        Update EventLog information
        
        Args:
            id: id of EventLog to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated EventLogResponse if successful, None if EventLog not found
        """    
        result = await self.repo.update_by_id(id, updates.model_dump(exclude_unset=True))
        return EventLogResponse.model_validate(result) if result else None
    
    # ─── Delete operations ──────────────────────────────────
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a EventLog
        
        Args:
            id: id of EventLog to delete
            
        Returns:
            True if EventLog was deleted, False if EventLog not found
        """
        return await self.repo.delete_by_id(id)
