# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c



from typing import Any
from core.logging.repository_logger import log_repository_call
from core.db_exception_handler import handle_db_exceptions_async
from core.pagination import PaginationRequest, apply_filters, apply_pagination_filter
from features.tables.shopping_list_item.models import ShoppingListItemModel
from features.tables.shopping_list_item.schemas import ShoppingListItemFilter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

class ShoppingListItemRepository:
    """Repository layer for all ShoppingListItem-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
    
    # ─── Create operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("ShoppingListItem")
    async def create(self, shoppinglistitem_record: ShoppingListItemModel) -> ShoppingListItemModel | None:
        """
        Create a new ShoppingListItem

        Args:
            data: New ShoppingListItem data
            
        Returns:
            ShoppingListItem data if created successfully, None if ShoppingListItem already exists
        """
        
        # Create new ShoppingListItem
        self.session.add(shoppinglistitem_record)
        await self.session.commit()
        await self.session.refresh(shoppinglistitem_record)

        return shoppinglistitem_record

    
    # ─── Read operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("ShoppingListItem")
    async def get_by_id(self, id: int) -> ShoppingListItemModel | None:
        """
        Get shopping_list_item by id
        
        Args:
            id: The id to search for
            
        Returns:
            ShoppingListItem if found, None otherwise
        """
        stmt = select(ShoppingListItemModel).where(ShoppingListItemModel.id == id)
        result = await self.session.execute(stmt)
        return result.unique().scalars().first()

    @handle_db_exceptions_async
    @log_repository_call("ShoppingListItem")
    async def get_all(self, pagination: PaginationRequest) -> tuple[list[ShoppingListItemModel], int]:
        """
        Get all shopping_list_item
        
        Returns:
            List of all shopping_list_item
        """
        stmt = select(ShoppingListItemModel)

        total = await self.session.scalar(select(func.count(ShoppingListItemModel.id)))
        stmt = apply_pagination_filter(stmt, pagination, ShoppingListItemModel)

        result = await self.session.execute(stmt)
        records = result.unique().scalars().all()
        return records, total
    
    @handle_db_exceptions_async
    @log_repository_call("ShoppingListItem")
    async def search(self, filters: ShoppingListItemFilter, pagination: PaginationRequest) -> tuple[list[ShoppingListItemModel], int]:
        stmt = select(ShoppingListItemModel)
        stmt = apply_filters(stmt, filters, ShoppingListItemModel)

        total = await self.session.scalar(select(func.count()).select_from(stmt.subquery()))
        stmt = apply_pagination_filter(stmt, pagination, ShoppingListItemModel)

        results = await self.session.execute(stmt)
        records = results.unique().scalars().all()
        return records, total


    # ─── Update operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("ShoppingListItem")
    async def update_by_id(self, id: int, updates: dict[str, Any]) -> ShoppingListItemModel | None:
        """
        Update ShoppingListItem information
        
        Args:
            id: id of ShoppingListItem to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated ShoppingListItem if successful, None if ShoppingListItem not found
        """
        stmt = select(ShoppingListItemModel).where(ShoppingListItemModel.id == id)
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
    @log_repository_call("ShoppingListItem")
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a ShoppingListItem
        
        Args:
            id: id of ShoppingListItem to delete
            
        Returns:
            True if user was deleted, False if user not found
        """
        stmt = select(ShoppingListItemModel).where(ShoppingListItemModel.id == id)
        result = await self.session.execute(stmt)
        record = result.unique().scalars().first()
        if record:
            await self.session.delete(record)
            await self.session.commit()
            return True
        return False
