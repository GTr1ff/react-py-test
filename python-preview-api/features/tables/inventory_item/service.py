# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c



from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from core.pagination import PaginatedResponse, PaginationRequest
from features.tables.inventory_item.models import InventoryItemModel
from features.tables.inventory_item.schemas import InventoryItemResponse, InventoryItemCreate, InventoryItemUpdate, InventoryItemFilter
from features.tables.inventory_item.repository import InventoryItemRepository

class InventoryItemService:
    """Service layer for all InventoryItem-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = InventoryItemRepository(session)

    
    # ─── Read operations ──────────────────────────────────id
    async def get_by_id(self, id: int) -> InventoryItemResponse | None:
        """
        Get inventory_item by id
        
        Args:
            id: The id to search for
            
        Returns:
            InventoryItemResponse if found, None if not found
        """
        result = await self.repo.get_by_id(id)
        return InventoryItemResponse.model_validate(result) if result else None

    async def get_all(self, pagination: PaginationRequest) -> PaginatedResponse[InventoryItemResponse]:
        """
        Get all inventory_item
        
        Returns:
            List of all inventory_item
        """
        result, total = await self.repo.get_all(pagination)

        return PaginatedResponse[InventoryItemResponse](
            items=[InventoryItemResponse.model_validate(record) for record in result],
            **pagination.model_dump(),
            total=total
        )

    async def search(self, filters: InventoryItemFilter, pagination: PaginationRequest) -> PaginatedResponse[InventoryItemResponse]:
        results, total = await self.repo.search(filters, pagination)
        return PaginatedResponse[InventoryItemResponse](
            items=[InventoryItemResponse.model_validate(record) for record in results],
            **pagination.model_dump(),
            total=total
        )


    # ─── Create operations ──────────────────────────────────
    async def create(self, data: InventoryItemCreate) -> InventoryItemResponse:
        """
        Create a new InventoryItem

        Args:
            data: New InventoryItem data
            
        Returns:
            InventoryItemResponse if created successfully, None if InventoryItem already exists
        """

        # Check if unique fields already exist
        inventoryitem_model = InventoryItemModel(**data.model_dump())
        
        # Create
        result = await self.repo.create(inventoryitem_model)

        return InventoryItemResponse.model_validate(result)

    # ─── Update operations ──────────────────────────────────
    async def update_by_id(self, id: int, updates: InventoryItemUpdate) -> InventoryItemResponse | None:
        """
        Update InventoryItem information
        
        Args:
            id: id of InventoryItem to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated InventoryItemResponse if successful, None if InventoryItem not found
        """    
        result = await self.repo.update_by_id(id, updates.model_dump(exclude_unset=True))
        return InventoryItemResponse.model_validate(result) if result else None
    
    # ─── Delete operations ──────────────────────────────────
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a InventoryItem
        
        Args:
            id: id of InventoryItem to delete
            
        Returns:
            True if InventoryItem was deleted, False if InventoryItem not found
        """
        return await self.repo.delete_by_id(id)
