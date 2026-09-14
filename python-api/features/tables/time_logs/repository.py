# ROSETIC:crud-guid



from typing import Any
from core.logging.repository_logger import log_repository_call
from core.db_exception_handler import handle_db_exceptions_async
from core.pagination import PaginationRequest, apply_filters, apply_pagination_filter
from features.tables.time_logs.models import TimeLogModel
from features.tables.time_logs.schemas import TimeLogFilter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

class TimeLogRepository:
    """Repository layer for all TimeLog-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
    
    # ─── Create operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("TimeLog")
    async def create(self, timelog_record: TimeLogModel) -> TimeLogModel | None:
        """
        Create a new TimeLog

        Args:
            data: New TimeLog data
            
        Returns:
            TimeLog data if created successfully, None if TimeLog already exists
        """
        
        # Create new TimeLog
        self.session.add(timelog_record)
        await self.session.commit()
        await self.session.refresh(timelog_record)

        return timelog_record

    
    # ─── Read operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("TimeLog")
    async def get_by_id(self, id: int) -> TimeLogModel | None:
        """
        Get time_logs by id
        
        Args:
            id: The id to search for
            
        Returns:
            TimeLog if found, None otherwise
        """
        stmt = select(TimeLogModel).where(TimeLogModel.time_log_id == id)
        result = await self.session.execute(stmt)
        return result.unique().scalars().first()

    @handle_db_exceptions_async
    @log_repository_call("TimeLog")
    async def get_all(self, pagination: PaginationRequest) -> tuple[list[TimeLogModel], int]:
        """
        Get all time_logs
        
        Returns:
            List of all time_logs
        """
        stmt = select(TimeLogModel)

        total = await self.session.scalar(select(func.count(TimeLogModel.time_log_id)))
        stmt = apply_pagination_filter(stmt, pagination, TimeLogModel)

        result = await self.session.execute(stmt)
        records = result.unique().scalars().all()
        return records, total
    
    @handle_db_exceptions_async
    @log_repository_call("TimeLog")
    async def search(self, filters: TimeLogFilter, pagination: PaginationRequest) -> tuple[list[TimeLogModel], int]:
        stmt = select(TimeLogModel)
        stmt = apply_filters(stmt, filters, TimeLogModel)

        total = await self.session.scalar(select(func.count()).select_from(stmt.subquery()))
        stmt = apply_pagination_filter(stmt, pagination, TimeLogModel)

        results = await self.session.execute(stmt)
        records = results.unique().scalars().all()
        return records, total


    # ─── Update operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("TimeLog")
    async def update_by_id(self, id: int, updates: dict[str, Any]) -> TimeLogModel | None:
        """
        Update TimeLog information
        
        Args:
            id: id of TimeLog to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated TimeLog if successful, None if TimeLog not found
        """
        stmt = select(TimeLogModel).where(TimeLogModel.time_log_id == id)
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
    @log_repository_call("TimeLog")
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a TimeLog
        
        Args:
            id: id of TimeLog to delete
            
        Returns:
            True if user was deleted, False if user not found
        """
        stmt = select(TimeLogModel).where(TimeLogModel.time_log_id == id)
        result = await self.session.execute(stmt)
        record = result.unique().scalars().first()
        if record:
            await self.session.delete(record)
            await self.session.commit()
            return True
        return False
