# ROSETIC:crud-guid



from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from core.pagination import PaginatedResponse, PaginationRequest
from features.tables.payroll.models import PayrollModel
from features.tables.payroll.schemas import PayrollResponse, PayrollCreate, PayrollUpdate, PayrollFilter
from features.tables.payroll.repository import PayrollRepository

class PayrollService:
    """Service layer for all Payroll-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = PayrollRepository(session)

    
    # ─── Read operations ──────────────────────────────────id
    async def get_by_id(self, id: int) -> PayrollResponse | None:
        """
        Get payroll by id
        
        Args:
            id: The id to search for
            
        Returns:
            PayrollResponse if found, None if not found
        """
        result = await self.repo.get_by_id(id)
        return PayrollResponse.model_validate(result) if result else None

    async def get_all(self, pagination: PaginationRequest) -> PaginatedResponse[PayrollResponse]:
        """
        Get all payroll
        
        Returns:
            List of all payroll
        """
        result, total = await self.repo.get_all(pagination)

        return PaginatedResponse[PayrollResponse](
            items=[PayrollResponse.model_validate(record) for record in result],
            **pagination.model_dump(),
            total=total
        )

    async def search(self, filters: PayrollFilter, pagination: PaginationRequest) -> PaginatedResponse[PayrollResponse]:
        results, total = await self.repo.search(filters, pagination)
        return PaginatedResponse[PayrollResponse](
            items=[PayrollResponse.model_validate(record) for record in results],
            **pagination.model_dump(),
            total=total
        )


    # ─── Create operations ──────────────────────────────────
    async def create(self, data: PayrollCreate) -> PayrollResponse:
        """
        Create a new Payroll

        Args:
            data: New Payroll data
            
        Returns:
            PayrollResponse if created successfully, None if Payroll already exists
        """

        # Check if unique fields already exist
        payroll_model = PayrollModel(**data.model_dump())
        
        # Create
        result = await self.repo.create(payroll_model)

        return PayrollResponse.model_validate(result)

    # ─── Update operations ──────────────────────────────────
    async def update_by_id(self, id: int, updates: PayrollUpdate) -> PayrollResponse | None:
        """
        Update Payroll information
        
        Args:
            id: id of Payroll to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated PayrollResponse if successful, None if Payroll not found
        """    
        result = await self.repo.update_by_id(id, updates.model_dump(exclude_unset=True))
        return PayrollResponse.model_validate(result) if result else None
    
    # ─── Delete operations ──────────────────────────────────
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a Payroll
        
        Args:
            id: id of Payroll to delete
            
        Returns:
            True if Payroll was deleted, False if Payroll not found
        """
        return await self.repo.delete_by_id(id)
