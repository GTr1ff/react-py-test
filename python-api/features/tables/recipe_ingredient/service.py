# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c



from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from core.pagination import PaginatedResponse, PaginationRequest
from features.tables.recipe_ingredient.models import RecipeIngredientModel
from features.tables.recipe_ingredient.schemas import RecipeIngredientResponse, RecipeIngredientCreate, RecipeIngredientUpdate, RecipeIngredientFilter
from features.tables.recipe_ingredient.repository import RecipeIngredientRepository

class RecipeIngredientService:
    """Service layer for all RecipeIngredient-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = RecipeIngredientRepository(session)

    
    # ─── Read operations ──────────────────────────────────id
    async def get_by_id(self, id: int) -> RecipeIngredientResponse | None:
        """
        Get recipe_ingredient by id
        
        Args:
            id: The id to search for
            
        Returns:
            RecipeIngredientResponse if found, None if not found
        """
        result = await self.repo.get_by_id(id)
        return RecipeIngredientResponse.model_validate(result) if result else None

    async def get_all(self, pagination: PaginationRequest) -> PaginatedResponse[RecipeIngredientResponse]:
        """
        Get all recipe_ingredient
        
        Returns:
            List of all recipe_ingredient
        """
        result, total = await self.repo.get_all(pagination)

        return PaginatedResponse[RecipeIngredientResponse](
            items=[RecipeIngredientResponse.model_validate(record) for record in result],
            **pagination.model_dump(),
            total=total
        )

    async def search(self, filters: RecipeIngredientFilter, pagination: PaginationRequest) -> PaginatedResponse[RecipeIngredientResponse]:
        results, total = await self.repo.search(filters, pagination)
        return PaginatedResponse[RecipeIngredientResponse](
            items=[RecipeIngredientResponse.model_validate(record) for record in results],
            **pagination.model_dump(),
            total=total
        )


    # ─── Create operations ──────────────────────────────────
    async def create(self, data: RecipeIngredientCreate) -> RecipeIngredientResponse:
        """
        Create a new RecipeIngredient

        Args:
            data: New RecipeIngredient data
            
        Returns:
            RecipeIngredientResponse if created successfully, None if RecipeIngredient already exists
        """

        # Check if unique fields already exist
        recipeingredient_model = RecipeIngredientModel(**data.model_dump())
        
        # Create
        result = await self.repo.create(recipeingredient_model)

        return RecipeIngredientResponse.model_validate(result)

    # ─── Update operations ──────────────────────────────────
    async def update_by_id(self, id: int, updates: RecipeIngredientUpdate) -> RecipeIngredientResponse | None:
        """
        Update RecipeIngredient information
        
        Args:
            id: id of RecipeIngredient to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated RecipeIngredientResponse if successful, None if RecipeIngredient not found
        """    
        result = await self.repo.update_by_id(id, updates.model_dump(exclude_unset=True))
        return RecipeIngredientResponse.model_validate(result) if result else None
    
    # ─── Delete operations ──────────────────────────────────
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a RecipeIngredient
        
        Args:
            id: id of RecipeIngredient to delete
            
        Returns:
            True if RecipeIngredient was deleted, False if RecipeIngredient not found
        """
        return await self.repo.delete_by_id(id)
