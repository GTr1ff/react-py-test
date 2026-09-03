# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c



from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from core.pagination import PaginatedResponse, PaginationRequest
from features.tables.ingredient.models import IngredientModel
from features.tables.ingredient.schemas import IngredientResponse, IngredientCreate, IngredientUpdate, IngredientFilter
from features.tables.ingredient.repository import IngredientRepository

class IngredientService:
    """Service layer for all Ingredient-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = IngredientRepository(session)

    
    # ─── Read operations ──────────────────────────────────id
    async def get_by_id(self, id: int) -> IngredientResponse | None:
        """
        Get ingredient by id
        
        Args:
            id: The id to search for
            
        Returns:
            IngredientResponse if found, None if not found
        """
        result = await self.repo.get_by_id(id)
        return IngredientResponse.model_validate(result) if result else None

    async def get_all(self, pagination: PaginationRequest) -> PaginatedResponse[IngredientResponse]:
        """
        Get all ingredient
        
        Returns:
            List of all ingredient
        """
        result, total = await self.repo.get_all(pagination)

        return PaginatedResponse[IngredientResponse](
            items=[IngredientResponse.model_validate(record) for record in result],
            **pagination.model_dump(),
            total=total
        )

    async def search(self, filters: IngredientFilter, pagination: PaginationRequest) -> PaginatedResponse[IngredientResponse]:
        results, total = await self.repo.search(filters, pagination)
        return PaginatedResponse[IngredientResponse](
            items=[IngredientResponse.model_validate(record) for record in results],
            **pagination.model_dump(),
            total=total
        )


    # ─── Create operations ──────────────────────────────────
    async def create(self, data: IngredientCreate) -> IngredientResponse:
        """
        Create a new Ingredient

        Args:
            data: New Ingredient data
            
        Returns:
            IngredientResponse if created successfully, None if Ingredient already exists
        """

        # Check if unique fields already exist
        ingredient_model = IngredientModel(**data.model_dump())
        
        # Create
        result = await self.repo.create(ingredient_model)

        return IngredientResponse.model_validate(result)

    # ─── Update operations ──────────────────────────────────
    async def update_by_id(self, id: int, updates: IngredientUpdate) -> IngredientResponse | None:
        """
        Update Ingredient information
        
        Args:
            id: id of Ingredient to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated IngredientResponse if successful, None if Ingredient not found
        """    
        result = await self.repo.update_by_id(id, updates.model_dump(exclude_unset=True))
        return IngredientResponse.model_validate(result) if result else None
    
    # ─── Delete operations ──────────────────────────────────
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a Ingredient
        
        Args:
            id: id of Ingredient to delete
            
        Returns:
            True if Ingredient was deleted, False if Ingredient not found
        """
        return await self.repo.delete_by_id(id)
