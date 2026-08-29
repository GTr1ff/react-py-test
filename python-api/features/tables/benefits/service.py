# ROSETIC:crud-guid



from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from core.pagination import PaginatedResponse, PaginationRequest
from features.tables.benefits.models import BenefitModel
from features.tables.benefits.schemas import BenefitResponse, BenefitCreate, BenefitUpdate, BenefitFilter
from features.tables.benefits.repository import BenefitRepository

class BenefitService:
    """Service layer for all Benefit-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = BenefitRepository(session)

    
    # ─── Read operations ──────────────────────────────────id
    async def get_by_id(self, id: int) -> BenefitResponse | None:
        """
        Get benefits by id
        
        Args:
            id: The id to search for
            
        Returns:
            BenefitResponse if found, None if not found
        """
        result = await self.repo.get_by_id(id)
        return BenefitResponse.model_validate(result) if result else None

    async def get_all(self, pagination: PaginationRequest) -> PaginatedResponse[BenefitResponse]:
        """
        Get all benefits
        
        Returns:
            List of all benefits
        """
        result, total = await self.repo.get_all(pagination)

        return PaginatedResponse[BenefitResponse](
            items=[BenefitResponse.model_validate(record) for record in result],
            **pagination.model_dump(),
            total=total
        )

    async def search(self, filters: BenefitFilter, pagination: PaginationRequest) -> PaginatedResponse[BenefitResponse]:
        results, total = await self.repo.search(filters, pagination)
        return PaginatedResponse[BenefitResponse](
            items=[BenefitResponse.model_validate(record) for record in results],
            **pagination.model_dump(),
            total=total
        )


    # ─── Create operations ──────────────────────────────────
    async def create(self, data: BenefitCreate) -> BenefitResponse:
        """
        Create a new Benefit

        Args:
            data: New Benefit data
            
        Returns:
            BenefitResponse if created successfully, None if Benefit already exists
        """

        # Check if unique fields already exist
        benefit_model = BenefitModel(**data.model_dump())
        
        # Create
        result = await self.repo.create(benefit_model)

        return BenefitResponse.model_validate(result)

    # ─── Update operations ──────────────────────────────────
    async def update_by_id(self, id: int, updates: BenefitUpdate) -> BenefitResponse | None:
        """
        Update Benefit information
        
        Args:
            id: id of Benefit to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated BenefitResponse if successful, None if Benefit not found
        """    
        result = await self.repo.update_by_id(id, updates.model_dump(exclude_unset=True))
        return BenefitResponse.model_validate(result) if result else None
    
    # ─── Delete operations ──────────────────────────────────
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a Benefit
        
        Args:
            id: id of Benefit to delete
            
        Returns:
            True if Benefit was deleted, False if Benefit not found
        """
        return await self.repo.delete_by_id(id)
