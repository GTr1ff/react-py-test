# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c



from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from core.pagination import PaginatedResponse, PaginationRequest
from features.tables.shopping_list_item.models import ShoppingListItemModel
from features.tables.shopping_list_item.schemas import ShoppingListItemResponse, ShoppingListItemCreate, ShoppingListItemUpdate, ShoppingListItemFilter
from features.tables.shopping_list_item.repository import ShoppingListItemRepository

class ShoppingListItemService:
    """Service layer for all ShoppingListItem-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = ShoppingListItemRepository(session)

    
    # ─── Read operations ──────────────────────────────────id
    async def get_by_id(self, id: int) -> ShoppingListItemResponse | None:
        """
        Get shopping_list_item by id
        
        Args:
            id: The id to search for
            
        Returns:
            ShoppingListItemResponse if found, None if not found
        """
        result = await self.repo.get_by_id(id)
        return ShoppingListItemResponse.model_validate(result) if result else None

    async def get_all(self, pagination: PaginationRequest) -> PaginatedResponse[ShoppingListItemResponse]:
        """
        Get all shopping_list_item
        
        Returns:
            List of all shopping_list_item
        """
        result, total = await self.repo.get_all(pagination)

        return PaginatedResponse[ShoppingListItemResponse](
            items=[ShoppingListItemResponse.model_validate(record) for record in result],
            **pagination.model_dump(),
            total=total
        )

    async def search(self, filters: ShoppingListItemFilter, pagination: PaginationRequest) -> PaginatedResponse[ShoppingListItemResponse]:
        results, total = await self.repo.search(filters, pagination)
        return PaginatedResponse[ShoppingListItemResponse](
            items=[ShoppingListItemResponse.model_validate(record) for record in results],
            **pagination.model_dump(),
            total=total
        )


    # ─── Create operations ──────────────────────────────────
    async def create(self, data: ShoppingListItemCreate) -> ShoppingListItemResponse:
        """
        Create a new ShoppingListItem

        Args:
            data: New ShoppingListItem data
            
        Returns:
            ShoppingListItemResponse if created successfully, None if ShoppingListItem already exists
        """

        # Check if unique fields already exist
        shoppinglistitem_model = ShoppingListItemModel(**data.model_dump())
        
        # Create
        result = await self.repo.create(shoppinglistitem_model)

        return ShoppingListItemResponse.model_validate(result)

    # ─── Update operations ──────────────────────────────────
    async def update_by_id(self, id: int, updates: ShoppingListItemUpdate) -> ShoppingListItemResponse | None:
        """
        Update ShoppingListItem information
        
        Args:
            id: id of ShoppingListItem to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated ShoppingListItemResponse if successful, None if ShoppingListItem not found
        """    
        result = await self.repo.update_by_id(id, updates.model_dump(exclude_unset=True))
        return ShoppingListItemResponse.model_validate(result) if result else None
    
    # ─── Delete operations ──────────────────────────────────
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a ShoppingListItem
        
        Args:
            id: id of ShoppingListItem to delete
            
        Returns:
            True if ShoppingListItem was deleted, False if ShoppingListItem not found
        """
        return await self.repo.delete_by_id(id)
