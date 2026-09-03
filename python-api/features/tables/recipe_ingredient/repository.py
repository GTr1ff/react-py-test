# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c



from typing import Any
from core.logging.repository_logger import log_repository_call
from core.db_exception_handler import handle_db_exceptions_async
from core.pagination import PaginationRequest, apply_filters, apply_pagination_filter
from features.tables.recipe_ingredient.models import RecipeIngredientModel
from features.tables.recipe_ingredient.schemas import RecipeIngredientFilter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

class RecipeIngredientRepository:
    """Repository layer for all RecipeIngredient-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
    
    # ─── Create operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("RecipeIngredient")
    async def create(self, recipeingredient_record: RecipeIngredientModel) -> RecipeIngredientModel | None:
        """
        Create a new RecipeIngredient

        Args:
            data: New RecipeIngredient data
            
        Returns:
            RecipeIngredient data if created successfully, None if RecipeIngredient already exists
        """
        
        # Create new RecipeIngredient
        self.session.add(recipeingredient_record)
        await self.session.commit()
        await self.session.refresh(recipeingredient_record)

        return recipeingredient_record

    
    # ─── Read operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("RecipeIngredient")
    async def get_by_id(self, id: int) -> RecipeIngredientModel | None:
        """
        Get recipe_ingredient by id
        
        Args:
            id: The id to search for
            
        Returns:
            RecipeIngredient if found, None otherwise
        """
        stmt = select(RecipeIngredientModel).where(RecipeIngredientModel.recipe_id == id)
        result = await self.session.execute(stmt)
        return result.unique().scalars().first()

    @handle_db_exceptions_async
    @log_repository_call("RecipeIngredient")
    async def get_all(self, pagination: PaginationRequest) -> tuple[list[RecipeIngredientModel], int]:
        """
        Get all recipe_ingredient
        
        Returns:
            List of all recipe_ingredient
        """
        stmt = select(RecipeIngredientModel)

        total = await self.session.scalar(select(func.count(RecipeIngredientModel.recipe_id)))
        stmt = apply_pagination_filter(stmt, pagination, RecipeIngredientModel)

        result = await self.session.execute(stmt)
        records = result.unique().scalars().all()
        return records, total
    
    @handle_db_exceptions_async
    @log_repository_call("RecipeIngredient")
    async def search(self, filters: RecipeIngredientFilter, pagination: PaginationRequest) -> tuple[list[RecipeIngredientModel], int]:
        stmt = select(RecipeIngredientModel)
        stmt = apply_filters(stmt, filters, RecipeIngredientModel)

        total = await self.session.scalar(select(func.count()).select_from(stmt.subquery()))
        stmt = apply_pagination_filter(stmt, pagination, RecipeIngredientModel)

        results = await self.session.execute(stmt)
        records = results.unique().scalars().all()
        return records, total


    # ─── Update operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("RecipeIngredient")
    async def update_by_id(self, id: int, updates: dict[str, Any]) -> RecipeIngredientModel | None:
        """
        Update RecipeIngredient information
        
        Args:
            id: id of RecipeIngredient to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated RecipeIngredient if successful, None if RecipeIngredient not found
        """
        stmt = select(RecipeIngredientModel).where(RecipeIngredientModel.recipe_id == id)
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
    @log_repository_call("RecipeIngredient")
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a RecipeIngredient
        
        Args:
            id: id of RecipeIngredient to delete
            
        Returns:
            True if user was deleted, False if user not found
        """
        stmt = select(RecipeIngredientModel).where(RecipeIngredientModel.recipe_id == id)
        result = await self.session.execute(stmt)
        record = result.unique().scalars().first()
        if record:
            await self.session.delete(record)
            await self.session.commit()
            return True
        return False
