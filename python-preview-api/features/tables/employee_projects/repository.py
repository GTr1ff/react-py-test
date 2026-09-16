# ROSETIC:crud-guid



from typing import Any
from core.logging.repository_logger import log_repository_call
from core.db_exception_handler import handle_db_exceptions_async
from core.pagination import PaginationRequest, apply_filters, apply_pagination_filter
from features.tables.employee_projects.models import EmployeeProjectModel
from features.tables.employee_projects.schemas import EmployeeProjectFilter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

class EmployeeProjectRepository:
    """Repository layer for all EmployeeProject-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
    
    # ─── Create operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("EmployeeProject")
    async def create(self, employeeproject_record: EmployeeProjectModel) -> EmployeeProjectModel | None:
        """
        Create a new EmployeeProject

        Args:
            data: New EmployeeProject data
            
        Returns:
            EmployeeProject data if created successfully, None if EmployeeProject already exists
        """
        
        # Create new EmployeeProject
        self.session.add(employeeproject_record)
        await self.session.commit()
        await self.session.refresh(employeeproject_record)

        return employeeproject_record

    
    # ─── Read operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("EmployeeProject")
    async def get_by_id(self, id: int) -> EmployeeProjectModel | None:
        """
        Get employee_projects by id
        
        Args:
            id: The id to search for
            
        Returns:
            EmployeeProject if found, None otherwise
        """
        stmt = select(EmployeeProjectModel).where(EmployeeProjectModel.employee_project_id == id)
        result = await self.session.execute(stmt)
        return result.unique().scalars().first()

    @handle_db_exceptions_async
    @log_repository_call("EmployeeProject")
    async def get_all(self, pagination: PaginationRequest) -> tuple[list[EmployeeProjectModel], int]:
        """
        Get all employee_projects
        
        Returns:
            List of all employee_projects
        """
        stmt = select(EmployeeProjectModel)

        total = await self.session.scalar(select(func.count(EmployeeProjectModel.employee_project_id)))
        stmt = apply_pagination_filter(stmt, pagination, EmployeeProjectModel)

        result = await self.session.execute(stmt)
        records = result.unique().scalars().all()
        return records, total
    
    @handle_db_exceptions_async
    @log_repository_call("EmployeeProject")
    async def search(self, filters: EmployeeProjectFilter, pagination: PaginationRequest) -> tuple[list[EmployeeProjectModel], int]:
        stmt = select(EmployeeProjectModel)
        stmt = apply_filters(stmt, filters, EmployeeProjectModel)

        total = await self.session.scalar(select(func.count()).select_from(stmt.subquery()))
        stmt = apply_pagination_filter(stmt, pagination, EmployeeProjectModel)

        results = await self.session.execute(stmt)
        records = results.unique().scalars().all()
        return records, total


    # ─── Update operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("EmployeeProject")
    async def update_by_id(self, id: int, updates: dict[str, Any]) -> EmployeeProjectModel | None:
        """
        Update EmployeeProject information
        
        Args:
            id: id of EmployeeProject to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated EmployeeProject if successful, None if EmployeeProject not found
        """
        stmt = select(EmployeeProjectModel).where(EmployeeProjectModel.employee_project_id == id)
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
    @log_repository_call("EmployeeProject")
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a EmployeeProject
        
        Args:
            id: id of EmployeeProject to delete
            
        Returns:
            True if user was deleted, False if user not found
        """
        stmt = select(EmployeeProjectModel).where(EmployeeProjectModel.employee_project_id == id)
        result = await self.session.execute(stmt)
        record = result.unique().scalars().first()
        if record:
            await self.session.delete(record)
            await self.session.commit()
            return True
        return False
