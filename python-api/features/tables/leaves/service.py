# ROSETIC:crud-guid



from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from core.pagination import PaginatedResponse, PaginationRequest
from features.tables.leaves.models import LeafModel
from features.tables.leaves.schemas import LeafResponse, LeafCreate, LeafUpdate, LeafFilter
from features.tables.leaves.repository import LeafRepository

class LeafService:
    """Service layer for all Leaf-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = LeafRepository(session)

    
    # ─── Read operations ──────────────────────────────────id
    async def get_by_id(self, id: int) -> LeafResponse | None:
        """
        Get leaves by id
        
        Args:
            id: The id to search for
            
        Returns:
            LeafResponse if found, None if not found
        """
        result = await self.repo.get_by_id(id)
        return LeafResponse.model_validate(result) if result else None

    async def get_all(self, pagination: PaginationRequest) -> PaginatedResponse[LeafResponse]:
        """
        Get all leaves
        
        Returns:
            List of all leaves
        """
        result, total = await self.repo.get_all(pagination)

        return PaginatedResponse[LeafResponse](
            items=[LeafResponse.model_validate(record) for record in result],
            **pagination.model_dump(),
            total=total
        )

    async def search(self, filters: LeafFilter, pagination: PaginationRequest) -> PaginatedResponse[LeafResponse]:
        results, total = await self.repo.search(filters, pagination)
        return PaginatedResponse[LeafResponse](
            items=[LeafResponse.model_validate(record) for record in results],
            **pagination.model_dump(),
            total=total
        )


    # ─── Create operations ──────────────────────────────────
    async def create(self, data: LeafCreate) -> LeafResponse:
        """
        Create a new Leaf

        Args:
            data: New Leaf data
            
        Returns:
            LeafResponse if created successfully, None if Leaf already exists
        """

        # Check if unique fields already exist
        leaf_model = LeafModel(**data.model_dump())
        
        # Create
        result = await self.repo.create(leaf_model)

        return LeafResponse.model_validate(result)

    # ─── Update operations ──────────────────────────────────
    async def update_by_id(self, id: int, updates: LeafUpdate) -> LeafResponse | None:
        """
        Update Leaf information
        
        Args:
            id: id of Leaf to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated LeafResponse if successful, None if Leaf not found
        """    
        result = await self.repo.update_by_id(id, updates.model_dump(exclude_unset=True))
        return LeafResponse.model_validate(result) if result else None
    
    # ─── Delete operations ──────────────────────────────────
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a Leaf
        
        Args:
            id: id of Leaf to delete
            
        Returns:
            True if Leaf was deleted, False if Leaf not found
        """
        return await self.repo.delete_by_id(id)
