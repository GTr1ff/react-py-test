# ROSETIC:crud-guid



from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from core.pagination import PaginatedResponse, PaginationRequest
from features.tables.employees.models import EmployeeModel
from features.tables.employees.schemas import EmployeeResponse, EmployeeCreate, EmployeeUpdate, EmployeeFilter
from features.tables.employees.repository import EmployeeRepository

class EmployeeService:
    """Service layer for all Employee-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = EmployeeRepository(session)

    
    # ─── Read operations ──────────────────────────────────id
    async def get_by_id(self, id: int) -> EmployeeResponse | None:
        """
        Get employees by id
        
        Args:
            id: The id to search for
            
        Returns:
            EmployeeResponse if found, None if not found
        """
        result = await self.repo.get_by_id(id)
        return EmployeeResponse.model_validate(result) if result else None

    async def get_all(self, pagination: PaginationRequest) -> PaginatedResponse[EmployeeResponse]:
        """
        Get all employees
        
        Returns:
            List of all employees
        """
        result, total = await self.repo.get_all(pagination)

        return PaginatedResponse[EmployeeResponse](
            items=[EmployeeResponse.model_validate(record) for record in result],
            **pagination.model_dump(),
            total=total
        )

    async def search(self, filters: EmployeeFilter, pagination: PaginationRequest) -> PaginatedResponse[EmployeeResponse]:
        results, total = await self.repo.search(filters, pagination)
        return PaginatedResponse[EmployeeResponse](
            items=[EmployeeResponse.model_validate(record) for record in results],
            **pagination.model_dump(),
            total=total
        )


    # ─── Create operations ──────────────────────────────────
    async def create(self, data: EmployeeCreate) -> EmployeeResponse:
        """
        Create a new Employee

        Args:
            data: New Employee data
            
        Returns:
            EmployeeResponse if created successfully, None if Employee already exists
        """

        # Check if unique fields already exist
        employee_model = EmployeeModel(**data.model_dump())
        
        # Create
        result = await self.repo.create(employee_model)

        return EmployeeResponse.model_validate(result)

    # ─── Update operations ──────────────────────────────────
    async def update_by_id(self, id: int, updates: EmployeeUpdate) -> EmployeeResponse | None:
        """
        Update Employee information
        
        Args:
            id: id of Employee to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated EmployeeResponse if successful, None if Employee not found
        """    
        result = await self.repo.update_by_id(id, updates.model_dump(exclude_unset=True))
        return EmployeeResponse.model_validate(result) if result else None
    
    # ─── Delete operations ──────────────────────────────────
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a Employee
        
        Args:
            id: id of Employee to delete
            
        Returns:
            True if Employee was deleted, False if Employee not found
        """
        return await self.repo.delete_by_id(id)
