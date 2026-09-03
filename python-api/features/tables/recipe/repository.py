# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c



from typing import Any
from core.logging.repository_logger import log_repository_call
from core.db_exception_handler import handle_db_exceptions_async
from core.pagination import PaginationRequest, apply_filters, apply_pagination_filter
from features.tables.recipe.models import RecipeModel
from features.tables.recipe.schemas import RecipeFilter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

class RecipeRepository:
    """Repository layer for all Recipe-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
    
    # ─── Create operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Recipe")
    async def create(self, recipe_record: RecipeModel) -> RecipeModel | None:
        """
        Create a new Recipe

        Args:
            data: New Recipe data
            
        Returns:
            Recipe data if created successfully, None if Recipe already exists
        """
        
        # Create new Recipe
        self.session.add(recipe_record)
        await self.session.commit()
        await self.session.refresh(recipe_record)

        return recipe_record

    
    # ─── Read operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Recipe")
    async def get_by_id(self, id: int) -> RecipeModel | None:
        """
        Get recipe by id
        
        Args:
            id: The id to search for
            
        Returns:
            Recipe if found, None otherwise
        """
        stmt = select(RecipeModel).where(RecipeModel.id == id)
        result = await self.session.execute(stmt)
        return result.unique().scalars().first()

    @handle_db_exceptions_async
    @log_repository_call("Recipe")
    async def get_all(self, pagination: PaginationRequest) -> tuple[list[RecipeModel], int]:
        """
        Get all recipe
        
        Returns:
            List of all recipe
        """
        stmt = select(RecipeModel)

        total = await self.session.scalar(select(func.count(RecipeModel.id)))
        stmt = apply_pagination_filter(stmt, pagination, RecipeModel)

        result = await self.session.execute(stmt)
        records = result.unique().scalars().all()
        return records, total
    
    @handle_db_exceptions_async
    @log_repository_call("Recipe")
    async def search(self, filters: RecipeFilter, pagination: PaginationRequest) -> tuple[list[RecipeModel], int]:
        stmt = select(RecipeModel)
        stmt = apply_filters(stmt, filters, RecipeModel)

        total = await self.session.scalar(select(func.count()).select_from(stmt.subquery()))
        stmt = apply_pagination_filter(stmt, pagination, RecipeModel)

        results = await self.session.execute(stmt)
        records = results.unique().scalars().all()
        return records, total


    # ─── Update operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Recipe")
    async def update_by_id(self, id: int, updates: dict[str, Any]) -> RecipeModel | None:
        """
        Update Recipe information
        
        Args:
            id: id of Recipe to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated Recipe if successful, None if Recipe not found
        """
        stmt = select(RecipeModel).where(RecipeModel.id == id)
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
    @log_repository_call("Recipe")
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a Recipe
        
        Args:
            id: id of Recipe to delete
            
        Returns:
            True if user was deleted, False if user not found
        """
        stmt = select(RecipeModel).where(RecipeModel.id == id)
        result = await self.session.execute(stmt)
        record = result.unique().scalars().first()
        if record:
            await self.session.delete(record)
            await self.session.commit()
            return True
        return False
