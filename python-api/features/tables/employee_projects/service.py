# ROSETIC:crud-guid



from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from core.pagination import PaginatedResponse, PaginationRequest
from features.tables.employee_projects.models import EmployeeProjectModel
from features.tables.employee_projects.schemas import EmployeeProjectResponse, EmployeeProjectCreate, EmployeeProjectUpdate, EmployeeProjectFilter
from features.tables.employee_projects.repository import EmployeeProjectRepository

class EmployeeProjectService:
    """Service layer for all EmployeeProject-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = EmployeeProjectRepository(session)

    
    # ─── Read operations ──────────────────────────────────id
    async def get_by_id(self, id: int) -> EmployeeProjectResponse | None:
        """
        Get employee_projects by id
        
        Args:
            id: The id to search for
            
        Returns:
            EmployeeProjectResponse if found, None if not found
        """
        result = await self.repo.get_by_id(id)
        return EmployeeProjectResponse.model_validate(result) if result else None

    async def get_all(self, pagination: PaginationRequest) -> PaginatedResponse[EmployeeProjectResponse]:
        """
        Get all employee_projects
        
        Returns:
            List of all employee_projects
        """
        result, total = await self.repo.get_all(pagination)

        return PaginatedResponse[EmployeeProjectResponse](
            items=[EmployeeProjectResponse.model_validate(record) for record in result],
            **pagination.model_dump(),
            total=total
        )

    async def search(self, filters: EmployeeProjectFilter, pagination: PaginationRequest) -> PaginatedResponse[EmployeeProjectResponse]:
        results, total = await self.repo.search(filters, pagination)
        return PaginatedResponse[EmployeeProjectResponse](
            items=[EmployeeProjectResponse.model_validate(record) for record in results],
            **pagination.model_dump(),
            total=total
        )


    # ─── Create operations ──────────────────────────────────
    async def create(self, data: EmployeeProjectCreate) -> EmployeeProjectResponse:
        """
        Create a new EmployeeProject

        Args:
            data: New EmployeeProject data
            
        Returns:
            EmployeeProjectResponse if created successfully, None if EmployeeProject already exists
        """

        # Check if unique fields already exist
        employeeproject_model = EmployeeProjectModel(**data.model_dump())
        
        # Create
        result = await self.repo.create(employeeproject_model)

        return EmployeeProjectResponse.model_validate(result)

    # ─── Update operations ──────────────────────────────────
    async def update_by_id(self, id: int, updates: EmployeeProjectUpdate) -> EmployeeProjectResponse | None:
        """
        Update EmployeeProject information
        
        Args:
            id: id of EmployeeProject to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated EmployeeProjectResponse if successful, None if EmployeeProject not found
        """    
        result = await self.repo.update_by_id(id, updates.model_dump(exclude_unset=True))
        return EmployeeProjectResponse.model_validate(result) if result else None
    
    # ─── Delete operations ──────────────────────────────────
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a EmployeeProject
        
        Args:
            id: id of EmployeeProject to delete
            
        Returns:
            True if EmployeeProject was deleted, False if EmployeeProject not found
        """
        return await self.repo.delete_by_id(id)
