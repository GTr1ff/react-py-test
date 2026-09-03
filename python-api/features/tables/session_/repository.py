# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c



from typing import Any
from core.logging.repository_logger import log_repository_call
from core.db_exception_handler import handle_db_exceptions_async
from core.pagination import PaginationRequest, apply_filters, apply_pagination_filter
from features.tables.session_.models import SessionModel
from features.tables.session_.schemas import SessionFilter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

class SessionRepository:
    """Repository layer for all Session-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
    
    # ─── Create operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Session")
    async def create(self, session_record: SessionModel) -> SessionModel | None:
        """
        Create a new Session

        Args:
            data: New Session data
            
        Returns:
            Session data if created successfully, None if Session already exists
        """
        
        # Create new Session
        self.session.add(session_record)
        await self.session.commit()
        await self.session.refresh(session_record)

        return session_record

    
    # ─── Read operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Session")
    async def get_by_id(self, id: int) -> SessionModel | None:
        """
        Get session by id
        
        Args:
            id: The id to search for
            
        Returns:
            Session if found, None otherwise
        """
        stmt = select(SessionModel).where(SessionModel.id == id)
        result = await self.session.execute(stmt)
        return result.unique().scalars().first()

    @handle_db_exceptions_async
    @log_repository_call("Session")
    async def get_all(self, pagination: PaginationRequest) -> tuple[list[SessionModel], int]:
        """
        Get all session
        
        Returns:
            List of all session
        """
        stmt = select(SessionModel)

        total = await self.session.scalar(select(func.count(SessionModel.id)))
        stmt = apply_pagination_filter(stmt, pagination, SessionModel)

        result = await self.session.execute(stmt)
        records = result.unique().scalars().all()
        return records, total
    
    @handle_db_exceptions_async
    @log_repository_call("Session")
    async def search(self, filters: SessionFilter, pagination: PaginationRequest) -> tuple[list[SessionModel], int]:
        stmt = select(SessionModel)
        stmt = apply_filters(stmt, filters, SessionModel)

        total = await self.session.scalar(select(func.count()).select_from(stmt.subquery()))
        stmt = apply_pagination_filter(stmt, pagination, SessionModel)

        results = await self.session.execute(stmt)
        records = results.unique().scalars().all()
        return records, total


    # ─── Update operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Session")
    async def update_by_id(self, id: int, updates: dict[str, Any]) -> SessionModel | None:
        """
        Update Session information
        
        Args:
            id: id of Session to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated Session if successful, None if Session not found
        """
        stmt = select(SessionModel).where(SessionModel.id == id)
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
    @log_repository_call("Session")
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a Session
        
        Args:
            id: id of Session to delete
            
        Returns:
            True if user was deleted, False if user not found
        """
        stmt = select(SessionModel).where(SessionModel.id == id)
        result = await self.session.execute(stmt)
        record = result.unique().scalars().first()
        if record:
            await self.session.delete(record)
            await self.session.commit()
            return True
        return False
