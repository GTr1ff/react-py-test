# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c



from typing import Any
from core.logging.repository_logger import log_repository_call
from core.db_exception_handler import handle_db_exceptions_async
from core.pagination import PaginationRequest, apply_filters, apply_pagination_filter
from features.tables.category.models import CategoryModel
from features.tables.category.schemas import CategoryFilter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

class CategoryRepository:
    """Repository layer for all Category-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
    
    # ─── Create operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Category")
    async def create(self, category_record: CategoryModel) -> CategoryModel | None:
        """
        Create a new Category

        Args:
            data: New Category data
            
        Returns:
            Category data if created successfully, None if Category already exists
        """
        
        # Create new Category
        self.session.add(category_record)
        await self.session.commit()
        await self.session.refresh(category_record)

        return category_record

    
    # ─── Read operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Category")
    async def get_by_id(self, id: int) -> CategoryModel | None:
        """
        Get category by id
        
        Args:
            id: The id to search for
            
        Returns:
            Category if found, None otherwise
        """
        stmt = select(CategoryModel).where(CategoryModel.id == id)
        result = await self.session.execute(stmt)
        return result.unique().scalars().first()

    @handle_db_exceptions_async
    @log_repository_call("Category")
    async def get_all(self, pagination: PaginationRequest) -> tuple[list[CategoryModel], int]:
        """
        Get all category
        
        Returns:
            List of all category
        """
        stmt = select(CategoryModel)

        total = await self.session.scalar(select(func.count(CategoryModel.id)))
        stmt = apply_pagination_filter(stmt, pagination, CategoryModel)

        result = await self.session.execute(stmt)
        records = result.unique().scalars().all()
        return records, total
    
    @handle_db_exceptions_async
    @log_repository_call("Category")
    async def search(self, filters: CategoryFilter, pagination: PaginationRequest) -> tuple[list[CategoryModel], int]:
        stmt = select(CategoryModel)
        stmt = apply_filters(stmt, filters, CategoryModel)

        total = await self.session.scalar(select(func.count()).select_from(stmt.subquery()))
        stmt = apply_pagination_filter(stmt, pagination, CategoryModel)

        results = await self.session.execute(stmt)
        records = results.unique().scalars().all()
        return records, total


    # ─── Update operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Category")
    async def update_by_id(self, id: int, updates: dict[str, Any]) -> CategoryModel | None:
        """
        Update Category information
        
        Args:
            id: id of Category to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated Category if successful, None if Category not found
        """
        stmt = select(CategoryModel).where(CategoryModel.id == id)
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
    @log_repository_call("Category")
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a Category
        
        Args:
            id: id of Category to delete
            
        Returns:
            True if user was deleted, False if user not found
        """
        stmt = select(CategoryModel).where(CategoryModel.id == id)
        result = await self.session.execute(stmt)
        record = result.unique().scalars().first()
        if record:
            await self.session.delete(record)
            await self.session.commit()
            return True
        return False
