# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c



from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from core.pagination import PaginatedResponse, PaginationRequest
from features.tables.recipe.models import RecipeModel
from features.tables.recipe.schemas import RecipeResponse, RecipeCreate, RecipeUpdate, RecipeFilter
from features.tables.recipe.repository import RecipeRepository

class RecipeService:
    """Service layer for all Recipe-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = RecipeRepository(session)

    
    # ─── Read operations ──────────────────────────────────id
    async def get_by_id(self, id: int) -> RecipeResponse | None:
        """
        Get recipe by id
        
        Args:
            id: The id to search for
            
        Returns:
            RecipeResponse if found, None if not found
        """
        result = await self.repo.get_by_id(id)
        return RecipeResponse.model_validate(result) if result else None

    async def get_all(self, pagination: PaginationRequest) -> PaginatedResponse[RecipeResponse]:
        """
        Get all recipe
        
        Returns:
            List of all recipe
        """
        result, total = await self.repo.get_all(pagination)

        return PaginatedResponse[RecipeResponse](
            items=[RecipeResponse.model_validate(record) for record in result],
            **pagination.model_dump(),
            total=total
        )

    async def search(self, filters: RecipeFilter, pagination: PaginationRequest) -> PaginatedResponse[RecipeResponse]:
        results, total = await self.repo.search(filters, pagination)
        return PaginatedResponse[RecipeResponse](
            items=[RecipeResponse.model_validate(record) for record in results],
            **pagination.model_dump(),
            total=total
        )


    # ─── Create operations ──────────────────────────────────
    async def create(self, data: RecipeCreate) -> RecipeResponse:
        """
        Create a new Recipe

        Args:
            data: New Recipe data
            
        Returns:
            RecipeResponse if created successfully, None if Recipe already exists
        """

        # Check if unique fields already exist
        recipe_model = RecipeModel(**data.model_dump())
        
        # Create
        result = await self.repo.create(recipe_model)

        return RecipeResponse.model_validate(result)

    # ─── Update operations ──────────────────────────────────
    async def update_by_id(self, id: int, updates: RecipeUpdate) -> RecipeResponse | None:
        """
        Update Recipe information
        
        Args:
            id: id of Recipe to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated RecipeResponse if successful, None if Recipe not found
        """    
        result = await self.repo.update_by_id(id, updates.model_dump(exclude_unset=True))
        return RecipeResponse.model_validate(result) if result else None
    
    # ─── Delete operations ──────────────────────────────────
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a Recipe
        
        Args:
            id: id of Recipe to delete
            
        Returns:
            True if Recipe was deleted, False if Recipe not found
        """
        return await self.repo.delete_by_id(id)
