# ROSETIC:crud-guid



from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from core.pagination import PaginatedResponse, PaginationRequest
from features.tables.memos.models import MemoModel
from features.tables.memos.schemas import MemoResponse, MemoCreate, MemoUpdate, MemoFilter
from features.tables.memos.repository import MemoRepository

class MemoService:
    """Service layer for all Memo-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = MemoRepository(session)

    
    # ─── Read operations ──────────────────────────────────id
    async def get_by_id(self, id: int) -> MemoResponse | None:
        """
        Get memos by id
        
        Args:
            id: The id to search for
            
        Returns:
            MemoResponse if found, None if not found
        """
        result = await self.repo.get_by_id(id)
        return MemoResponse.model_validate(result) if result else None

    async def get_all(self, pagination: PaginationRequest) -> PaginatedResponse[MemoResponse]:
        """
        Get all memos
        
        Returns:
            List of all memos
        """
        result, total = await self.repo.get_all(pagination)

        return PaginatedResponse[MemoResponse](
            items=[MemoResponse.model_validate(record) for record in result],
            **pagination.model_dump(),
            total=total
        )

    async def search(self, filters: MemoFilter, pagination: PaginationRequest) -> PaginatedResponse[MemoResponse]:
        results, total = await self.repo.search(filters, pagination)
        return PaginatedResponse[MemoResponse](
            items=[MemoResponse.model_validate(record) for record in results],
            **pagination.model_dump(),
            total=total
        )


    # ─── Create operations ──────────────────────────────────
    async def create(self, data: MemoCreate) -> MemoResponse:
        """
        Create a new Memo

        Args:
            data: New Memo data
            
        Returns:
            MemoResponse if created successfully, None if Memo already exists
        """

        # Check if unique fields already exist
        memo_model = MemoModel(**data.model_dump())
        
        # Create
        result = await self.repo.create(memo_model)

        return MemoResponse.model_validate(result)

    # ─── Update operations ──────────────────────────────────
    async def update_by_id(self, id: int, updates: MemoUpdate) -> MemoResponse | None:
        """
        Update Memo information
        
        Args:
            id: id of Memo to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated MemoResponse if successful, None if Memo not found
        """    
        result = await self.repo.update_by_id(id, updates.model_dump(exclude_unset=True))
        return MemoResponse.model_validate(result) if result else None
    
    # ─── Delete operations ──────────────────────────────────
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a Memo
        
        Args:
            id: id of Memo to delete
            
        Returns:
            True if Memo was deleted, False if Memo not found
        """
        return await self.repo.delete_by_id(id)
