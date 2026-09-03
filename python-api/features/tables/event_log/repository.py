# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c



from typing import Any
from core.logging.repository_logger import log_repository_call
from core.db_exception_handler import handle_db_exceptions_async
from core.pagination import PaginationRequest, apply_filters, apply_pagination_filter
from features.tables.event_log.models import EventLogModel
from features.tables.event_log.schemas import EventLogFilter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

class EventLogRepository:
    """Repository layer for all EventLog-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
    
    # ─── Create operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("EventLog")
    async def create(self, eventlog_record: EventLogModel) -> EventLogModel | None:
        """
        Create a new EventLog

        Args:
            data: New EventLog data
            
        Returns:
            EventLog data if created successfully, None if EventLog already exists
        """
        
        # Create new EventLog
        self.session.add(eventlog_record)
        await self.session.commit()
        await self.session.refresh(eventlog_record)

        return eventlog_record

    
    # ─── Read operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("EventLog")
    async def get_by_id(self, id: int) -> EventLogModel | None:
        """
        Get event_log by id
        
        Args:
            id: The id to search for
            
        Returns:
            EventLog if found, None otherwise
        """
        stmt = select(EventLogModel).where(EventLogModel.id == id)
        result = await self.session.execute(stmt)
        return result.unique().scalars().first()

    @handle_db_exceptions_async
    @log_repository_call("EventLog")
    async def get_all(self, pagination: PaginationRequest) -> tuple[list[EventLogModel], int]:
        """
        Get all event_log
        
        Returns:
            List of all event_log
        """
        stmt = select(EventLogModel)

        total = await self.session.scalar(select(func.count(EventLogModel.id)))
        stmt = apply_pagination_filter(stmt, pagination, EventLogModel)

        result = await self.session.execute(stmt)
        records = result.unique().scalars().all()
        return records, total
    
    @handle_db_exceptions_async
    @log_repository_call("EventLog")
    async def search(self, filters: EventLogFilter, pagination: PaginationRequest) -> tuple[list[EventLogModel], int]:
        stmt = select(EventLogModel)
        stmt = apply_filters(stmt, filters, EventLogModel)

        total = await self.session.scalar(select(func.count()).select_from(stmt.subquery()))
        stmt = apply_pagination_filter(stmt, pagination, EventLogModel)

        results = await self.session.execute(stmt)
        records = results.unique().scalars().all()
        return records, total


    # ─── Update operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("EventLog")
    async def update_by_id(self, id: int, updates: dict[str, Any]) -> EventLogModel | None:
        """
        Update EventLog information
        
        Args:
            id: id of EventLog to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated EventLog if successful, None if EventLog not found
        """
        stmt = select(EventLogModel).where(EventLogModel.id == id)
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
    @log_repository_call("EventLog")
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a EventLog
        
        Args:
            id: id of EventLog to delete
            
        Returns:
            True if user was deleted, False if user not found
        """
        stmt = select(EventLogModel).where(EventLogModel.id == id)
        result = await self.session.execute(stmt)
        record = result.unique().scalars().first()
        if record:
            await self.session.delete(record)
            await self.session.commit()
            return True
        return False
