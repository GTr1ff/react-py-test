# ROSETIC:crud-guid



from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from core.pagination import PaginatedResponse, PaginationRequest
from features.tables.employee_benefits.models import EmployeeBenefitModel
from features.tables.employee_benefits.schemas import EmployeeBenefitResponse, EmployeeBenefitCreate, EmployeeBenefitUpdate, EmployeeBenefitFilter
from features.tables.employee_benefits.repository import EmployeeBenefitRepository

class EmployeeBenefitService:
    """Service layer for all EmployeeBenefit-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = EmployeeBenefitRepository(session)

    
    # ─── Read operations ──────────────────────────────────id
    async def get_by_id(self, id: int) -> EmployeeBenefitResponse | None:
        """
        Get employee_benefits by id
        
        Args:
            id: The id to search for
            
        Returns:
            EmployeeBenefitResponse if found, None if not found
        """
        result = await self.repo.get_by_id(id)
        return EmployeeBenefitResponse.model_validate(result) if result else None

    async def get_all(self, pagination: PaginationRequest) -> PaginatedResponse[EmployeeBenefitResponse]:
        """
        Get all employee_benefits
        
        Returns:
            List of all employee_benefits
        """
        result, total = await self.repo.get_all(pagination)

        return PaginatedResponse[EmployeeBenefitResponse](
            items=[EmployeeBenefitResponse.model_validate(record) for record in result],
            **pagination.model_dump(),
            total=total
        )

    async def search(self, filters: EmployeeBenefitFilter, pagination: PaginationRequest) -> PaginatedResponse[EmployeeBenefitResponse]:
        results, total = await self.repo.search(filters, pagination)
        return PaginatedResponse[EmployeeBenefitResponse](
            items=[EmployeeBenefitResponse.model_validate(record) for record in results],
            **pagination.model_dump(),
            total=total
        )


    # ─── Create operations ──────────────────────────────────
    async def create(self, data: EmployeeBenefitCreate) -> EmployeeBenefitResponse:
        """
        Create a new EmployeeBenefit

        Args:
            data: New EmployeeBenefit data
            
        Returns:
            EmployeeBenefitResponse if created successfully, None if EmployeeBenefit already exists
        """

        # Check if unique fields already exist
        employeebenefit_model = EmployeeBenefitModel(**data.model_dump())
        
        # Create
        result = await self.repo.create(employeebenefit_model)

        return EmployeeBenefitResponse.model_validate(result)

    # ─── Update operations ──────────────────────────────────
    async def update_by_id(self, id: int, updates: EmployeeBenefitUpdate) -> EmployeeBenefitResponse | None:
        """
        Update EmployeeBenefit information
        
        Args:
            id: id of EmployeeBenefit to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated EmployeeBenefitResponse if successful, None if EmployeeBenefit not found
        """    
        result = await self.repo.update_by_id(id, updates.model_dump(exclude_unset=True))
        return EmployeeBenefitResponse.model_validate(result) if result else None
    
    # ─── Delete operations ──────────────────────────────────
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a EmployeeBenefit
        
        Args:
            id: id of EmployeeBenefit to delete
            
        Returns:
            True if EmployeeBenefit was deleted, False if EmployeeBenefit not found
        """
        return await self.repo.delete_by_id(id)
