# ROSETIC:crud-guid



from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from core.pagination import PaginatedResponse, PaginationRequest
from features.tables.projects.models import ProjectModel
from features.tables.projects.schemas import ProjectResponse, ProjectCreate, ProjectUpdate, ProjectFilter
from features.tables.projects.repository import ProjectRepository

class ProjectService:
    """Service layer for all Project-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = ProjectRepository(session)

    
    # ─── Read operations ──────────────────────────────────id
    async def get_by_id(self, id: int) -> ProjectResponse | None:
        """
        Get projects by id
        
        Args:
            id: The id to search for
            
        Returns:
            ProjectResponse if found, None if not found
        """
        result = await self.repo.get_by_id(id)
        return ProjectResponse.model_validate(result) if result else None

    async def get_all(self, pagination: PaginationRequest) -> PaginatedResponse[ProjectResponse]:
        """
        Get all projects
        
        Returns:
            List of all projects
        """
        result, total = await self.repo.get_all(pagination)

        return PaginatedResponse[ProjectResponse](
            items=[ProjectResponse.model_validate(record) for record in result],
            **pagination.model_dump(),
            total=total
        )

    async def search(self, filters: ProjectFilter, pagination: PaginationRequest) -> PaginatedResponse[ProjectResponse]:
        results, total = await self.repo.search(filters, pagination)
        return PaginatedResponse[ProjectResponse](
            items=[ProjectResponse.model_validate(record) for record in results],
            **pagination.model_dump(),
            total=total
        )


    # ─── Create operations ──────────────────────────────────
    async def create(self, data: ProjectCreate) -> ProjectResponse:
        """
        Create a new Project

        Args:
            data: New Project data
            
        Returns:
            ProjectResponse if created successfully, None if Project already exists
        """

        # Check if unique fields already exist
        project_model = ProjectModel(**data.model_dump())
        
        # Create
        result = await self.repo.create(project_model)

        return ProjectResponse.model_validate(result)

    # ─── Update operations ──────────────────────────────────
    async def update_by_id(self, id: int, updates: ProjectUpdate) -> ProjectResponse | None:
        """
        Update Project information
        
        Args:
            id: id of Project to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated ProjectResponse if successful, None if Project not found
        """    
        result = await self.repo.update_by_id(id, updates.model_dump(exclude_unset=True))
        return ProjectResponse.model_validate(result) if result else None
    
    # ─── Delete operations ──────────────────────────────────
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a Project
        
        Args:
            id: id of Project to delete
            
        Returns:
            True if Project was deleted, False if Project not found
        """
        return await self.repo.delete_by_id(id)
