# ROSETIC:crud-guid



from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from core.pagination import PaginatedResponse, PaginationRequest
from features.tables.departments.models import DepartmentModel
from features.tables.departments.schemas import DepartmentResponse, DepartmentCreate, DepartmentUpdate, DepartmentFilter
from features.tables.departments.repository import DepartmentRepository

class DepartmentService:
    """Service layer for all Department-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = DepartmentRepository(session)

    
    # ─── Read operations ──────────────────────────────────id
    async def get_by_id(self, id: int) -> DepartmentResponse | None:
        """
        Get departments by id
        
        Args:
            id: The id to search for
            
        Returns:
            DepartmentResponse if found, None if not found
        """
        result = await self.repo.get_by_id(id)
        return DepartmentResponse.model_validate(result) if result else None

    async def get_all(self, pagination: PaginationRequest) -> PaginatedResponse[DepartmentResponse]:
        """
        Get all departments
        
        Returns:
            List of all departments
        """
        result, total = await self.repo.get_all(pagination)

        return PaginatedResponse[DepartmentResponse](
            items=[DepartmentResponse.model_validate(record) for record in result],
            **pagination.model_dump(),
            total=total
        )

    async def search(self, filters: DepartmentFilter, pagination: PaginationRequest) -> PaginatedResponse[DepartmentResponse]:
        results, total = await self.repo.search(filters, pagination)
        return PaginatedResponse[DepartmentResponse](
            items=[DepartmentResponse.model_validate(record) for record in results],
            **pagination.model_dump(),
            total=total
        )


    # ─── Create operations ──────────────────────────────────
    async def create(self, data: DepartmentCreate) -> DepartmentResponse:
        """
        Create a new Department

        Args:
            data: New Department data
            
        Returns:
            DepartmentResponse if created successfully, None if Department already exists
        """

        # Check if unique fields already exist
        department_model = DepartmentModel(**data.model_dump())
        
        # Create
        result = await self.repo.create(department_model)

        return DepartmentResponse.model_validate(result)

    # ─── Update operations ──────────────────────────────────
    async def update_by_id(self, id: int, updates: DepartmentUpdate) -> DepartmentResponse | None:
        """
        Update Department information
        
        Args:
            id: id of Department to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated DepartmentResponse if successful, None if Department not found
        """    
        result = await self.repo.update_by_id(id, updates.model_dump(exclude_unset=True))
        return DepartmentResponse.model_validate(result) if result else None
    
    # ─── Delete operations ──────────────────────────────────
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a Department
        
        Args:
            id: id of Department to delete
            
        Returns:
            True if Department was deleted, False if Department not found
        """
        return await self.repo.delete_by_id(id)
