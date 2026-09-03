# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c



from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from core.pagination import PaginatedResponse, PaginationRequest
from features.tables.consent.models import ConsentModel
from features.tables.consent.schemas import ConsentResponse, ConsentCreate, ConsentUpdate, ConsentFilter
from features.tables.consent.repository import ConsentRepository

class ConsentService:
    """Service layer for all Consent-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = ConsentRepository(session)

    
    # ─── Read operations ──────────────────────────────────id
    async def get_by_id(self, id: int) -> ConsentResponse | None:
        """
        Get consent by id
        
        Args:
            id: The id to search for
            
        Returns:
            ConsentResponse if found, None if not found
        """
        result = await self.repo.get_by_id(id)
        return ConsentResponse.model_validate(result) if result else None

    async def get_all(self, pagination: PaginationRequest) -> PaginatedResponse[ConsentResponse]:
        """
        Get all consent
        
        Returns:
            List of all consent
        """
        result, total = await self.repo.get_all(pagination)

        return PaginatedResponse[ConsentResponse](
            items=[ConsentResponse.model_validate(record) for record in result],
            **pagination.model_dump(),
            total=total
        )

    async def search(self, filters: ConsentFilter, pagination: PaginationRequest) -> PaginatedResponse[ConsentResponse]:
        results, total = await self.repo.search(filters, pagination)
        return PaginatedResponse[ConsentResponse](
            items=[ConsentResponse.model_validate(record) for record in results],
            **pagination.model_dump(),
            total=total
        )


    # ─── Create operations ──────────────────────────────────
    async def create(self, data: ConsentCreate) -> ConsentResponse:
        """
        Create a new Consent

        Args:
            data: New Consent data
            
        Returns:
            ConsentResponse if created successfully, None if Consent already exists
        """

        # Check if unique fields already exist
        consent_model = ConsentModel(**data.model_dump())
        
        # Create
        result = await self.repo.create(consent_model)

        return ConsentResponse.model_validate(result)

    # ─── Update operations ──────────────────────────────────
    async def update_by_id(self, id: int, updates: ConsentUpdate) -> ConsentResponse | None:
        """
        Update Consent information
        
        Args:
            id: id of Consent to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated ConsentResponse if successful, None if Consent not found
        """    
        result = await self.repo.update_by_id(id, updates.model_dump(exclude_unset=True))
        return ConsentResponse.model_validate(result) if result else None
    
    # ─── Delete operations ──────────────────────────────────
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a Consent
        
        Args:
            id: id of Consent to delete
            
        Returns:
            True if Consent was deleted, False if Consent not found
        """
        return await self.repo.delete_by_id(id)
