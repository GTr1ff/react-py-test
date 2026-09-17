# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c



from typing import Any
from core.logging.repository_logger import log_repository_call
from core.db_exception_handler import handle_db_exceptions_async
from core.pagination import PaginationRequest, apply_filters, apply_pagination_filter
from features.tables.ingredient.models import IngredientModel
from features.tables.ingredient.schemas import IngredientFilter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

class IngredientRepository:
    """Repository layer for all Ingredient-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
    
    # ─── Create operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Ingredient")
    async def create(self, ingredient_record: IngredientModel) -> IngredientModel | None:
        """
        Create a new Ingredient

        Args:
            data: New Ingredient data
            
        Returns:
            Ingredient data if created successfully, None if Ingredient already exists
        """
        
        # Create new Ingredient
        self.session.add(ingredient_record)
        await self.session.commit()
        await self.session.refresh(ingredient_record)

        return ingredient_record

    
    # ─── Read operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Ingredient")
    async def get_by_id(self, id: int) -> IngredientModel | None:
        """
        Get ingredient by id
        
        Args:
            id: The id to search for
            
        Returns:
            Ingredient if found, None otherwise
        """
        stmt = select(IngredientModel).where(IngredientModel.id == id)
        result = await self.session.execute(stmt)
        return result.unique().scalars().first()

    @handle_db_exceptions_async
    @log_repository_call("Ingredient")
    async def get_all(self, pagination: PaginationRequest) -> tuple[list[IngredientModel], int]:
        """
        Get all ingredient
        
        Returns:
            List of all ingredient
        """
        stmt = select(IngredientModel)

        total = await self.session.scalar(select(func.count(IngredientModel.id)))
        stmt = apply_pagination_filter(stmt, pagination, IngredientModel)

        result = await self.session.execute(stmt)
        records = result.unique().scalars().all()
        return records, total
    
    @handle_db_exceptions_async
    @log_repository_call("Ingredient")
    async def search(self, filters: IngredientFilter, pagination: PaginationRequest) -> tuple[list[IngredientModel], int]:
        stmt = select(IngredientModel)
        stmt = apply_filters(stmt, filters, IngredientModel)

        total = await self.session.scalar(select(func.count()).select_from(stmt.subquery()))
        stmt = apply_pagination_filter(stmt, pagination, IngredientModel)

        results = await self.session.execute(stmt)
        records = results.unique().scalars().all()
        return records, total


    # ─── Update operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Ingredient")
    async def update_by_id(self, id: int, updates: dict[str, Any]) -> IngredientModel | None:
        """
        Update Ingredient information
        
        Args:
            id: id of Ingredient to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated Ingredient if successful, None if Ingredient not found
        """
        stmt = select(IngredientModel).where(IngredientModel.id == id)
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
    @log_repository_call("Ingredient")
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a Ingredient
        
        Args:
            id: id of Ingredient to delete
            
        Returns:
            True if user was deleted, False if user not found
        """
        stmt = select(IngredientModel).where(IngredientModel.id == id)
        result = await self.session.execute(stmt)
        record = result.unique().scalars().first()
        if record:
            await self.session.delete(record)
            await self.session.commit()
            return True
        return False
