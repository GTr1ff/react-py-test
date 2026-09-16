# ROSETIC:crud-guid



from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from core.pagination import PaginatedResponse, PaginationRequest
from features.tables.salaries.models import SalaryModel
from features.tables.salaries.schemas import SalaryResponse, SalaryCreate, SalaryUpdate, SalaryFilter
from features.tables.salaries.repository import SalaryRepository

class SalaryService:
    """Service layer for all Salary-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = SalaryRepository(session)

    
    # ─── Read operations ──────────────────────────────────id
    async def get_by_id(self, id: int) -> SalaryResponse | None:
        """
        Get salaries by id
        
        Args:
            id: The id to search for
            
        Returns:
            SalaryResponse if found, None if not found
        """
        result = await self.repo.get_by_id(id)
        return SalaryResponse.model_validate(result) if result else None

    async def get_all(self, pagination: PaginationRequest) -> PaginatedResponse[SalaryResponse]:
        """
        Get all salaries
        
        Returns:
            List of all salaries
        """
        result, total = await self.repo.get_all(pagination)

        return PaginatedResponse[SalaryResponse](
            items=[SalaryResponse.model_validate(record) for record in result],
            **pagination.model_dump(),
            total=total
        )

    async def search(self, filters: SalaryFilter, pagination: PaginationRequest) -> PaginatedResponse[SalaryResponse]:
        results, total = await self.repo.search(filters, pagination)
        return PaginatedResponse[SalaryResponse](
            items=[SalaryResponse.model_validate(record) for record in results],
            **pagination.model_dump(),
            total=total
        )


    # ─── Create operations ──────────────────────────────────
    async def create(self, data: SalaryCreate) -> SalaryResponse:
        """
        Create a new Salary

        Args:
            data: New Salary data
            
        Returns:
            SalaryResponse if created successfully, None if Salary already exists
        """

        # Check if unique fields already exist
        salary_model = SalaryModel(**data.model_dump())
        
        # Create
        result = await self.repo.create(salary_model)

        return SalaryResponse.model_validate(result)

    # ─── Update operations ──────────────────────────────────
    async def update_by_id(self, id: int, updates: SalaryUpdate) -> SalaryResponse | None:
        """
        Update Salary information
        
        Args:
            id: id of Salary to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated SalaryResponse if successful, None if Salary not found
        """    
        result = await self.repo.update_by_id(id, updates.model_dump(exclude_unset=True))
        return SalaryResponse.model_validate(result) if result else None
    
    # ─── Delete operations ──────────────────────────────────
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a Salary
        
        Args:
            id: id of Salary to delete
            
        Returns:
            True if Salary was deleted, False if Salary not found
        """
        return await self.repo.delete_by_id(id)
