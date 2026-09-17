# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c



from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from core.pagination import PaginatedResponse, PaginationRequest
from features.tables.category.models import CategoryModel
from features.tables.category.schemas import CategoryResponse, CategoryCreate, CategoryUpdate, CategoryFilter
from features.tables.category.repository import CategoryRepository

class CategoryService:
    """Service layer for all Category-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = CategoryRepository(session)

    
    # ─── Read operations ──────────────────────────────────id
    async def get_by_id(self, id: int) -> CategoryResponse | None:
        """
        Get category by id
        
        Args:
            id: The id to search for
            
        Returns:
            CategoryResponse if found, None if not found
        """
        result = await self.repo.get_by_id(id)
        return CategoryResponse.model_validate(result) if result else None

    async def get_all(self, pagination: PaginationRequest) -> PaginatedResponse[CategoryResponse]:
        """
        Get all category
        
        Returns:
            List of all category
        """
        result, total = await self.repo.get_all(pagination)

        return PaginatedResponse[CategoryResponse](
            items=[CategoryResponse.model_validate(record) for record in result],
            **pagination.model_dump(),
            total=total
        )

    async def search(self, filters: CategoryFilter, pagination: PaginationRequest) -> PaginatedResponse[CategoryResponse]:
        results, total = await self.repo.search(filters, pagination)
        return PaginatedResponse[CategoryResponse](
            items=[CategoryResponse.model_validate(record) for record in results],
            **pagination.model_dump(),
            total=total
        )


    # ─── Create operations ──────────────────────────────────
    async def create(self, data: CategoryCreate) -> CategoryResponse:
        """
        Create a new Category

        Args:
            data: New Category data
            
        Returns:
            CategoryResponse if created successfully, None if Category already exists
        """

        # Check if unique fields already exist
        category_model = CategoryModel(**data.model_dump())
        
        # Create
        result = await self.repo.create(category_model)

        return CategoryResponse.model_validate(result)

    # ─── Update operations ──────────────────────────────────
    async def update_by_id(self, id: int, updates: CategoryUpdate) -> CategoryResponse | None:
        """
        Update Category information
        
        Args:
            id: id of Category to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated CategoryResponse if successful, None if Category not found
        """    
        result = await self.repo.update_by_id(id, updates.model_dump(exclude_unset=True))
        return CategoryResponse.model_validate(result) if result else None
    
    # ─── Delete operations ──────────────────────────────────
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a Category
        
        Args:
            id: id of Category to delete
            
        Returns:
            True if Category was deleted, False if Category not found
        """
        return await self.repo.delete_by_id(id)
