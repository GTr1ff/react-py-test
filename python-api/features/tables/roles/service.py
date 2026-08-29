# ROSETIC:crud-guid



from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from core.pagination import PaginatedResponse, PaginationRequest
from features.tables.roles.models import RoleModel
from features.tables.roles.schemas import RoleResponse, RoleCreate, RoleUpdate, RoleFilter
from features.tables.roles.repository import RoleRepository

class RoleService:
    """Service layer for all Role-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = RoleRepository(session)

    
    # ─── Read operations ──────────────────────────────────id
    async def get_by_id(self, id: int) -> RoleResponse | None:
        """
        Get roles by id
        
        Args:
            id: The id to search for
            
        Returns:
            RoleResponse if found, None if not found
        """
        result = await self.repo.get_by_id(id)
        return RoleResponse.model_validate(result) if result else None

    async def get_all(self, pagination: PaginationRequest) -> PaginatedResponse[RoleResponse]:
        """
        Get all roles
        
        Returns:
            List of all roles
        """
        result, total = await self.repo.get_all(pagination)

        return PaginatedResponse[RoleResponse](
            items=[RoleResponse.model_validate(record) for record in result],
            **pagination.model_dump(),
            total=total
        )

    async def search(self, filters: RoleFilter, pagination: PaginationRequest) -> PaginatedResponse[RoleResponse]:
        results, total = await self.repo.search(filters, pagination)
        return PaginatedResponse[RoleResponse](
            items=[RoleResponse.model_validate(record) for record in results],
            **pagination.model_dump(),
            total=total
        )


    # ─── Create operations ──────────────────────────────────
    async def create(self, data: RoleCreate) -> RoleResponse:
        """
        Create a new Role

        Args:
            data: New Role data
            
        Returns:
            RoleResponse if created successfully, None if Role already exists
        """

        # Check if unique fields already exist
        role_model = RoleModel(**data.model_dump())
        
        # Create
        result = await self.repo.create(role_model)

        return RoleResponse.model_validate(result)

    # ─── Update operations ──────────────────────────────────
    async def update_by_id(self, id: int, updates: RoleUpdate) -> RoleResponse | None:
        """
        Update Role information
        
        Args:
            id: id of Role to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated RoleResponse if successful, None if Role not found
        """    
        result = await self.repo.update_by_id(id, updates.model_dump(exclude_unset=True))
        return RoleResponse.model_validate(result) if result else None
    
    # ─── Delete operations ──────────────────────────────────
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a Role
        
        Args:
            id: id of Role to delete
            
        Returns:
            True if Role was deleted, False if Role not found
        """
        return await self.repo.delete_by_id(id)
