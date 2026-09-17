# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c



from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from core.pagination import PaginatedResponse, PaginationRequest
from features.tables.session_.models import SessionModel
from features.tables.session_.schemas import SessionResponse, SessionCreate, SessionUpdate, SessionFilter
from features.tables.session_.repository import SessionRepository

class SessionService:
    """Service layer for all Session-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = SessionRepository(session)

    
    # ─── Read operations ──────────────────────────────────id
    async def get_by_id(self, id: int) -> SessionResponse | None:
        """
        Get session by id
        
        Args:
            id: The id to search for
            
        Returns:
            SessionResponse if found, None if not found
        """
        result = await self.repo.get_by_id(id)
        return SessionResponse.model_validate(result) if result else None

    async def get_all(self, pagination: PaginationRequest) -> PaginatedResponse[SessionResponse]:
        """
        Get all session
        
        Returns:
            List of all session
        """
        result, total = await self.repo.get_all(pagination)

        return PaginatedResponse[SessionResponse](
            items=[SessionResponse.model_validate(record) for record in result],
            **pagination.model_dump(),
            total=total
        )

    async def search(self, filters: SessionFilter, pagination: PaginationRequest) -> PaginatedResponse[SessionResponse]:
        results, total = await self.repo.search(filters, pagination)
        return PaginatedResponse[SessionResponse](
            items=[SessionResponse.model_validate(record) for record in results],
            **pagination.model_dump(),
            total=total
        )


    # ─── Create operations ──────────────────────────────────
    async def create(self, data: SessionCreate) -> SessionResponse:
        """
        Create a new Session

        Args:
            data: New Session data
            
        Returns:
            SessionResponse if created successfully, None if Session already exists
        """

        # Check if unique fields already exist
        session_model = SessionModel(**data.model_dump())
        
        # Create
        result = await self.repo.create(session_model)

        return SessionResponse.model_validate(result)

    # ─── Update operations ──────────────────────────────────
    async def update_by_id(self, id: int, updates: SessionUpdate) -> SessionResponse | None:
        """
        Update Session information
        
        Args:
            id: id of Session to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated SessionResponse if successful, None if Session not found
        """    
        result = await self.repo.update_by_id(id, updates.model_dump(exclude_unset=True))
        return SessionResponse.model_validate(result) if result else None
    
    # ─── Delete operations ──────────────────────────────────
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a Session
        
        Args:
            id: id of Session to delete
            
        Returns:
            True if Session was deleted, False if Session not found
        """
        return await self.repo.delete_by_id(id)
