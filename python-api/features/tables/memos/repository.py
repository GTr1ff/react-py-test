# ROSETIC:crud-guid



from typing import Any
from core.logging.repository_logger import log_repository_call
from core.db_exception_handler import handle_db_exceptions_async
from core.pagination import PaginationRequest, apply_filters, apply_pagination_filter
from features.tables.memos.models import MemoModel
from features.tables.memos.schemas import MemoFilter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

class MemoRepository:
    """Repository layer for all Memo-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
    
    # ─── Create operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Memo")
    async def create(self, memo_record: MemoModel) -> MemoModel | None:
        """
        Create a new Memo

        Args:
            data: New Memo data
            
        Returns:
            Memo data if created successfully, None if Memo already exists
        """
        
        # Create new Memo
        self.session.add(memo_record)
        await self.session.commit()
        await self.session.refresh(memo_record)

        return memo_record

    
    # ─── Read operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Memo")
    async def get_by_id(self, id: int) -> MemoModel | None:
        """
        Get memos by id
        
        Args:
            id: The id to search for
            
        Returns:
            Memo if found, None otherwise
        """
        stmt = select(MemoModel).where(MemoModel.memo_id == id)
        result = await self.session.execute(stmt)
        return result.unique().scalars().first()

    @handle_db_exceptions_async
    @log_repository_call("Memo")
    async def get_all(self, pagination: PaginationRequest) -> tuple[list[MemoModel], int]:
        """
        Get all memos
        
        Returns:
            List of all memos
        """
        stmt = select(MemoModel)

        total = await self.session.scalar(select(func.count(MemoModel.memo_id)))
        stmt = apply_pagination_filter(stmt, pagination, MemoModel)

        result = await self.session.execute(stmt)
        records = result.unique().scalars().all()
        return records, total
    
    @handle_db_exceptions_async
    @log_repository_call("Memo")
    async def search(self, filters: MemoFilter, pagination: PaginationRequest) -> tuple[list[MemoModel], int]:
        stmt = select(MemoModel)
        stmt = apply_filters(stmt, filters, MemoModel)

        total = await self.session.scalar(select(func.count()).select_from(stmt.subquery()))
        stmt = apply_pagination_filter(stmt, pagination, MemoModel)

        results = await self.session.execute(stmt)
        records = results.unique().scalars().all()
        return records, total


    # ─── Update operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Memo")
    async def update_by_id(self, id: int, updates: dict[str, Any]) -> MemoModel | None:
        """
        Update Memo information
        
        Args:
            id: id of Memo to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated Memo if successful, None if Memo not found
        """
        stmt = select(MemoModel).where(MemoModel.memo_id == id)
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
    @log_repository_call("Memo")
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a Memo
        
        Args:
            id: id of Memo to delete
            
        Returns:
            True if user was deleted, False if user not found
        """
        stmt = select(MemoModel).where(MemoModel.memo_id == id)
        result = await self.session.execute(stmt)
        record = result.unique().scalars().first()
        if record:
            await self.session.delete(record)
            await self.session.commit()
            return True
        return False
