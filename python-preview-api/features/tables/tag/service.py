# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c



from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from core.pagination import PaginatedResponse, PaginationRequest
from features.tables.tag.models import TagModel
from features.tables.tag.schemas import TagResponse, TagCreate, TagUpdate, TagFilter
from features.tables.tag.repository import TagRepository

class TagService:
    """Service layer for all Tag-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = TagRepository(session)

    
    # ─── Read operations ──────────────────────────────────id
    async def get_by_id(self, id: int) -> TagResponse | None:
        """
        Get tag by id
        
        Args:
            id: The id to search for
            
        Returns:
            TagResponse if found, None if not found
        """
        result = await self.repo.get_by_id(id)
        return TagResponse.model_validate(result) if result else None

    async def get_all(self, pagination: PaginationRequest) -> PaginatedResponse[TagResponse]:
        """
        Get all tag
        
        Returns:
            List of all tag
        """
        result, total = await self.repo.get_all(pagination)

        return PaginatedResponse[TagResponse](
            items=[TagResponse.model_validate(record) for record in result],
            **pagination.model_dump(),
            total=total
        )

    async def search(self, filters: TagFilter, pagination: PaginationRequest) -> PaginatedResponse[TagResponse]:
        results, total = await self.repo.search(filters, pagination)
        return PaginatedResponse[TagResponse](
            items=[TagResponse.model_validate(record) for record in results],
            **pagination.model_dump(),
            total=total
        )


    # ─── Create operations ──────────────────────────────────
    async def create(self, data: TagCreate) -> TagResponse:
        """
        Create a new Tag

        Args:
            data: New Tag data
            
        Returns:
            TagResponse if created successfully, None if Tag already exists
        """

        # Check if unique fields already exist
        tag_model = TagModel(**data.model_dump())
        
        # Create
        result = await self.repo.create(tag_model)

        return TagResponse.model_validate(result)

    # ─── Update operations ──────────────────────────────────
    async def update_by_id(self, id: int, updates: TagUpdate) -> TagResponse | None:
        """
        Update Tag information
        
        Args:
            id: id of Tag to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated TagResponse if successful, None if Tag not found
        """    
        result = await self.repo.update_by_id(id, updates.model_dump(exclude_unset=True))
        return TagResponse.model_validate(result) if result else None
    
    # ─── Delete operations ──────────────────────────────────
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a Tag
        
        Args:
            id: id of Tag to delete
            
        Returns:
            True if Tag was deleted, False if Tag not found
        """
        return await self.repo.delete_by_id(id)
