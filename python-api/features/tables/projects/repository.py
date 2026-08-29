# ROSETIC:crud-guid



from typing import Any
from core.logging.repository_logger import log_repository_call
from core.db_exception_handler import handle_db_exceptions_async
from core.pagination import PaginationRequest, apply_filters, apply_pagination_filter
from features.tables.projects.models import ProjectModel
from features.tables.projects.schemas import ProjectFilter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

class ProjectRepository:
    """Repository layer for all Project-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
    
    # ─── Create operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Project")
    async def create(self, project_record: ProjectModel) -> ProjectModel | None:
        """
        Create a new Project

        Args:
            data: New Project data
            
        Returns:
            Project data if created successfully, None if Project already exists
        """
        
        # Create new Project
        self.session.add(project_record)
        await self.session.commit()
        await self.session.refresh(project_record)

        return project_record

    
    # ─── Read operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Project")
    async def get_by_id(self, id: int) -> ProjectModel | None:
        """
        Get projects by id
        
        Args:
            id: The id to search for
            
        Returns:
            Project if found, None otherwise
        """
        stmt = select(ProjectModel).where(ProjectModel.project_id == id)
        result = await self.session.execute(stmt)
        return result.unique().scalars().first()

    @handle_db_exceptions_async
    @log_repository_call("Project")
    async def get_all(self, pagination: PaginationRequest) -> tuple[list[ProjectModel], int]:
        """
        Get all projects
        
        Returns:
            List of all projects
        """
        stmt = select(ProjectModel)

        total = await self.session.scalar(select(func.count(ProjectModel.project_id)))
        stmt = apply_pagination_filter(stmt, pagination, ProjectModel)

        result = await self.session.execute(stmt)
        records = result.unique().scalars().all()
        return records, total
    
    @handle_db_exceptions_async
    @log_repository_call("Project")
    async def search(self, filters: ProjectFilter, pagination: PaginationRequest) -> tuple[list[ProjectModel], int]:
        stmt = select(ProjectModel)
        stmt = apply_filters(stmt, filters, ProjectModel)

        total = await self.session.scalar(select(func.count()).select_from(stmt.subquery()))
        stmt = apply_pagination_filter(stmt, pagination, ProjectModel)

        results = await self.session.execute(stmt)
        records = results.unique().scalars().all()
        return records, total


    # ─── Update operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Project")
    async def update_by_id(self, id: int, updates: dict[str, Any]) -> ProjectModel | None:
        """
        Update Project information
        
        Args:
            id: id of Project to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated Project if successful, None if Project not found
        """
        stmt = select(ProjectModel).where(ProjectModel.project_id == id)
        result = await self.session.execute(stmt)
        record = result.unique().scalars().first()
        if record:
            for key, value in updates.items():
                setattr(record, key, value)
            await self.session.commit()
            await self.session.refresh(record)

        return record
    
    # ─── Delete operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Project")
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a Project
        
        Args:
            id: id of Project to delete
            
        Returns:
            True if user was deleted, False if user not found
        """
        stmt = select(ProjectModel).where(ProjectModel.project_id == id)
        result = await self.session.execute(stmt)
        record = result.unique().scalars().first()
        if record:
            await self.session.delete(record)
            await self.session.commit()
            return True
        return False
