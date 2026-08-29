# ROSETIC:crud-guid



from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from core.pagination import PaginatedResponse, PaginationRequest
from features.tables.time_logs.models import TimeLogModel
from features.tables.time_logs.schemas import TimeLogResponse, TimeLogCreate, TimeLogUpdate, TimeLogFilter
from features.tables.time_logs.repository import TimeLogRepository

class TimeLogService:
    """Service layer for all TimeLog-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = TimeLogRepository(session)

    
    # ─── Read operations ──────────────────────────────────id
    async def get_by_id(self, id: int) -> TimeLogResponse | None:
        """
        Get time_logs by id
        
        Args:
            id: The id to search for
            
        Returns:
            TimeLogResponse if found, None if not found
        """
        result = await self.repo.get_by_id(id)
        return TimeLogResponse.model_validate(result) if result else None

    async def get_all(self, pagination: PaginationRequest) -> PaginatedResponse[TimeLogResponse]:
        """
        Get all time_logs
        
        Returns:
            List of all time_logs
        """
        result, total = await self.repo.get_all(pagination)

        return PaginatedResponse[TimeLogResponse](
            items=[TimeLogResponse.model_validate(record) for record in result],
            **pagination.model_dump(),
            total=total
        )

    async def search(self, filters: TimeLogFilter, pagination: PaginationRequest) -> PaginatedResponse[TimeLogResponse]:
        results, total = await self.repo.search(filters, pagination)
        return PaginatedResponse[TimeLogResponse](
            items=[TimeLogResponse.model_validate(record) for record in results],
            **pagination.model_dump(),
            total=total
        )


    # ─── Create operations ──────────────────────────────────
    async def create(self, data: TimeLogCreate) -> TimeLogResponse:
        """
        Create a new TimeLog

        Args:
            data: New TimeLog data
            
        Returns:
            TimeLogResponse if created successfully, None if TimeLog already exists
        """

        # Check if unique fields already exist
        timelog_model = TimeLogModel(**data.model_dump())
        
        # Create
        result = await self.repo.create(timelog_model)

        return TimeLogResponse.model_validate(result)

    # ─── Update operations ──────────────────────────────────
    async def update_by_id(self, id: int, updates: TimeLogUpdate) -> TimeLogResponse | None:
        """
        Update TimeLog information
        
        Args:
            id: id of TimeLog to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated TimeLogResponse if successful, None if TimeLog not found
        """    
        result = await self.repo.update_by_id(id, updates.model_dump(exclude_unset=True))
        return TimeLogResponse.model_validate(result) if result else None
    
    # ─── Delete operations ──────────────────────────────────
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a TimeLog
        
        Args:
            id: id of TimeLog to delete
            
        Returns:
            True if TimeLog was deleted, False if TimeLog not found
        """
        return await self.repo.delete_by_id(id)
