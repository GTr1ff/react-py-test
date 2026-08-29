# ROSETIC:crud-guid



from typing import Any
from core.logging.repository_logger import log_repository_call
from core.db_exception_handler import handle_db_exceptions_async
from core.pagination import PaginationRequest, apply_filters, apply_pagination_filter
from features.tables.job_history.models import JobHistoryModel
from features.tables.job_history.schemas import JobHistoryFilter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

class JobHistoryRepository:
    """Repository layer for all JobHistory-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
    
    # ─── Create operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("JobHistory")
    async def create(self, jobhistory_record: JobHistoryModel) -> JobHistoryModel | None:
        """
        Create a new JobHistory

        Args:
            data: New JobHistory data
            
        Returns:
            JobHistory data if created successfully, None if JobHistory already exists
        """
        
        # Create new JobHistory
        self.session.add(jobhistory_record)
        await self.session.commit()
        await self.session.refresh(jobhistory_record)

        return jobhistory_record

    
    # ─── Read operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("JobHistory")
    async def get_by_id(self, id: int) -> JobHistoryModel | None:
        """
        Get job_history by id
        
        Args:
            id: The id to search for
            
        Returns:
            JobHistory if found, None otherwise
        """
        stmt = select(JobHistoryModel).where(JobHistoryModel.job_history_id == id)
        result = await self.session.execute(stmt)
        return result.unique().scalars().first()

    @handle_db_exceptions_async
    @log_repository_call("JobHistory")
    async def get_all(self, pagination: PaginationRequest) -> tuple[list[JobHistoryModel], int]:
        """
        Get all job_history
        
        Returns:
            List of all job_history
        """
        stmt = select(JobHistoryModel)

        total = await self.session.scalar(select(func.count(JobHistoryModel.job_history_id)))
        stmt = apply_pagination_filter(stmt, pagination, JobHistoryModel)

        result = await self.session.execute(stmt)
        records = result.unique().scalars().all()
        return records, total
    
    @handle_db_exceptions_async
    @log_repository_call("JobHistory")
    async def search(self, filters: JobHistoryFilter, pagination: PaginationRequest) -> tuple[list[JobHistoryModel], int]:
        stmt = select(JobHistoryModel)
        stmt = apply_filters(stmt, filters, JobHistoryModel)

        total = await self.session.scalar(select(func.count()).select_from(stmt.subquery()))
        stmt = apply_pagination_filter(stmt, pagination, JobHistoryModel)

        results = await self.session.execute(stmt)
        records = results.unique().scalars().all()
        return records, total


    # ─── Update operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("JobHistory")
    async def update_by_id(self, id: int, updates: dict[str, Any]) -> JobHistoryModel | None:
        """
        Update JobHistory information
        
        Args:
            id: id of JobHistory to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated JobHistory if successful, None if JobHistory not found
        """
        stmt = select(JobHistoryModel).where(JobHistoryModel.job_history_id == id)
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
    @log_repository_call("JobHistory")
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a JobHistory
        
        Args:
            id: id of JobHistory to delete
            
        Returns:
            True if user was deleted, False if user not found
        """
        stmt = select(JobHistoryModel).where(JobHistoryModel.job_history_id == id)
        result = await self.session.execute(stmt)
        record = result.unique().scalars().first()
        if record:
            await self.session.delete(record)
            await self.session.commit()
            return True
        return False
