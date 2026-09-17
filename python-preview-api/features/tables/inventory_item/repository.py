# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c



from typing import Any
from core.logging.repository_logger import log_repository_call
from core.db_exception_handler import handle_db_exceptions_async
from core.pagination import PaginationRequest, apply_filters, apply_pagination_filter
from features.tables.inventory_item.models import InventoryItemModel
from features.tables.inventory_item.schemas import InventoryItemFilter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

class InventoryItemRepository:
    """Repository layer for all InventoryItem-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
    
    # ─── Create operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("InventoryItem")
    async def create(self, inventoryitem_record: InventoryItemModel) -> InventoryItemModel | None:
        """
        Create a new InventoryItem

        Args:
            data: New InventoryItem data
            
        Returns:
            InventoryItem data if created successfully, None if InventoryItem already exists
        """
        
        # Create new InventoryItem
        self.session.add(inventoryitem_record)
        await self.session.commit()
        await self.session.refresh(inventoryitem_record)

        return inventoryitem_record

    
    # ─── Read operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("InventoryItem")
    async def get_by_id(self, id: int) -> InventoryItemModel | None:
        """
        Get inventory_item by id
        
        Args:
            id: The id to search for
            
        Returns:
            InventoryItem if found, None otherwise
        """
        stmt = select(InventoryItemModel).where(InventoryItemModel.id == id)
        result = await self.session.execute(stmt)
        return result.unique().scalars().first()

    @handle_db_exceptions_async
    @log_repository_call("InventoryItem")
    async def get_all(self, pagination: PaginationRequest) -> tuple[list[InventoryItemModel], int]:
        """
        Get all inventory_item
        
        Returns:
            List of all inventory_item
        """
        stmt = select(InventoryItemModel)

        total = await self.session.scalar(select(func.count(InventoryItemModel.id)))
        stmt = apply_pagination_filter(stmt, pagination, InventoryItemModel)

        result = await self.session.execute(stmt)
        records = result.unique().scalars().all()
        return records, total
    
    @handle_db_exceptions_async
    @log_repository_call("InventoryItem")
    async def search(self, filters: InventoryItemFilter, pagination: PaginationRequest) -> tuple[list[InventoryItemModel], int]:
        stmt = select(InventoryItemModel)
        stmt = apply_filters(stmt, filters, InventoryItemModel)

        total = await self.session.scalar(select(func.count()).select_from(stmt.subquery()))
        stmt = apply_pagination_filter(stmt, pagination, InventoryItemModel)

        results = await self.session.execute(stmt)
        records = results.unique().scalars().all()
        return records, total


    # ─── Update operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("InventoryItem")
    async def update_by_id(self, id: int, updates: dict[str, Any]) -> InventoryItemModel | None:
        """
        Update InventoryItem information
        
        Args:
            id: id of InventoryItem to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated InventoryItem if successful, None if InventoryItem not found
        """
        stmt = select(InventoryItemModel).where(InventoryItemModel.id == id)
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
    @log_repository_call("InventoryItem")
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a InventoryItem
        
        Args:
            id: id of InventoryItem to delete
            
        Returns:
            True if user was deleted, False if user not found
        """
        stmt = select(InventoryItemModel).where(InventoryItemModel.id == id)
        result = await self.session.execute(stmt)
        record = result.unique().scalars().first()
        if record:
            await self.session.delete(record)
            await self.session.commit()
            return True
        return False
