# ROSETIC:crud-guid



from typing import Any
from core.logging.repository_logger import log_repository_call
from core.db_exception_handler import handle_db_exceptions_async
from core.pagination import PaginationRequest, apply_filters, apply_pagination_filter
from features.tables.leaves.models import LeafModel
from features.tables.leaves.schemas import LeafFilter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

class LeafRepository:
    """Repository layer for all Leaf-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
    
    # ─── Create operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Leaf")
    async def create(self, leaf_record: LeafModel) -> LeafModel | None:
        """
        Create a new Leaf

        Args:
            data: New Leaf data
            
        Returns:
            Leaf data if created successfully, None if Leaf already exists
        """
        
        # Create new Leaf
        self.session.add(leaf_record)
        await self.session.commit()
        await self.session.refresh(leaf_record)

        return leaf_record

    
    # ─── Read operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Leaf")
    async def get_by_id(self, id: int) -> LeafModel | None:
        """
        Get leaves by id
        
        Args:
            id: The id to search for
            
        Returns:
            Leaf if found, None otherwise
        """
        stmt = select(LeafModel).where(LeafModel.leave_id == id)
        result = await self.session.execute(stmt)
        return result.unique().scalars().first()

    @handle_db_exceptions_async
    @log_repository_call("Leaf")
    async def get_all(self, pagination: PaginationRequest) -> tuple[list[LeafModel], int]:
        """
        Get all leaves
        
        Returns:
            List of all leaves
        """
        stmt = select(LeafModel)

        total = await self.session.scalar(select(func.count(LeafModel.leave_id)))
        stmt = apply_pagination_filter(stmt, pagination, LeafModel)

        result = await self.session.execute(stmt)
        records = result.unique().scalars().all()
        return records, total
    
    @handle_db_exceptions_async
    @log_repository_call("Leaf")
    async def search(self, filters: LeafFilter, pagination: PaginationRequest) -> tuple[list[LeafModel], int]:
        stmt = select(LeafModel)
        stmt = apply_filters(stmt, filters, LeafModel)

        total = await self.session.scalar(select(func.count()).select_from(stmt.subquery()))
        stmt = apply_pagination_filter(stmt, pagination, LeafModel)

        results = await self.session.execute(stmt)
        records = results.unique().scalars().all()
        return records, total


    # ─── Update operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Leaf")
    async def update_by_id(self, id: int, updates: dict[str, Any]) -> LeafModel | None:
        """
        Update Leaf information
        
        Args:
            id: id of Leaf to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated Leaf if successful, None if Leaf not found
        """
        stmt = select(LeafModel).where(LeafModel.leave_id == id)
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
    @log_repository_call("Leaf")
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a Leaf
        
        Args:
            id: id of Leaf to delete
            
        Returns:
            True if user was deleted, False if user not found
        """
        stmt = select(LeafModel).where(LeafModel.leave_id == id)
        result = await self.session.execute(stmt)
        record = result.unique().scalars().first()
        if record:
            await self.session.delete(record)
            await self.session.commit()
            return True
        return False
