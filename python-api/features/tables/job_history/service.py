# ROSETIC:crud-guid



from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from core.pagination import PaginatedResponse, PaginationRequest
from features.tables.job_history.models import JobHistoryModel
from features.tables.job_history.schemas import JobHistoryResponse, JobHistoryCreate, JobHistoryUpdate, JobHistoryFilter
from features.tables.job_history.repository import JobHistoryRepository

class JobHistoryService:
    """Service layer for all JobHistory-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = JobHistoryRepository(session)

    
    # ─── Read operations ──────────────────────────────────id
    async def get_by_id(self, id: int) -> JobHistoryResponse | None:
        """
        Get job_history by id
        
        Args:
            id: The id to search for
            
        Returns:
            JobHistoryResponse if found, None if not found
        """
        result = await self.repo.get_by_id(id)
        return JobHistoryResponse.model_validate(result) if result else None

    async def get_all(self, pagination: PaginationRequest) -> PaginatedResponse[JobHistoryResponse]:
        """
        Get all job_history
        
        Returns:
            List of all job_history
        """
        result, total = await self.repo.get_all(pagination)

        return PaginatedResponse[JobHistoryResponse](
            items=[JobHistoryResponse.model_validate(record) for record in result],
            **pagination.model_dump(),
            total=total
        )

    async def search(self, filters: JobHistoryFilter, pagination: PaginationRequest) -> PaginatedResponse[JobHistoryResponse]:
        results, total = await self.repo.search(filters, pagination)
        return PaginatedResponse[JobHistoryResponse](
            items=[JobHistoryResponse.model_validate(record) for record in results],
            **pagination.model_dump(),
            total=total
        )


    # ─── Create operations ──────────────────────────────────
    async def create(self, data: JobHistoryCreate) -> JobHistoryResponse:
        """
        Create a new JobHistory

        Args:
            data: New JobHistory data
            
        Returns:
            JobHistoryResponse if created successfully, None if JobHistory already exists
        """

        # Check if unique fields already exist
        jobhistory_model = JobHistoryModel(**data.model_dump())
        
        # Create
        result = await self.repo.create(jobhistory_model)

        return JobHistoryResponse.model_validate(result)

    # ─── Update operations ──────────────────────────────────
    async def update_by_id(self, id: int, updates: JobHistoryUpdate) -> JobHistoryResponse | None:
        """
        Update JobHistory information
        
        Args:
            id: id of JobHistory to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated JobHistoryResponse if successful, None if JobHistory not found
        """    
        result = await self.repo.update_by_id(id, updates.model_dump(exclude_unset=True))
        return JobHistoryResponse.model_validate(result) if result else None
    
    # ─── Delete operations ──────────────────────────────────
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a JobHistory
        
        Args:
            id: id of JobHistory to delete
            
        Returns:
            True if JobHistory was deleted, False if JobHistory not found
        """
        return await self.repo.delete_by_id(id)
