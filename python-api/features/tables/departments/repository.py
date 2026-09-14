# ROSETIC:crud-guid



from typing import Any
from core.logging.repository_logger import log_repository_call
from core.db_exception_handler import handle_db_exceptions_async
from core.pagination import PaginationRequest, apply_filters, apply_pagination_filter
from features.tables.departments.models import DepartmentModel
from features.tables.departments.schemas import DepartmentFilter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

class DepartmentRepository:
    """Repository layer for all Department-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
    
    # ─── Create operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Department")
    async def create(self, department_record: DepartmentModel) -> DepartmentModel | None:
        """
        Create a new Department

        Args:
            data: New Department data
            
        Returns:
            Department data if created successfully, None if Department already exists
        """
        
        # Create new Department
        self.session.add(department_record)
        await self.session.commit()
        await self.session.refresh(department_record)

        return department_record

    
    # ─── Read operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Department")
    async def get_by_id(self, id: int) -> DepartmentModel | None:
        """
        Get departments by id
        
        Args:
            id: The id to search for
            
        Returns:
            Department if found, None otherwise
        """
        stmt = select(DepartmentModel).where(DepartmentModel.department_id == id)
        result = await self.session.execute(stmt)
        return result.unique().scalars().first()

    @handle_db_exceptions_async
    @log_repository_call("Department")
    async def get_all(self, pagination: PaginationRequest) -> tuple[list[DepartmentModel], int]:
        """
        Get all departments
        
        Returns:
            List of all departments
        """
        stmt = select(DepartmentModel)

        total = await self.session.scalar(select(func.count(DepartmentModel.department_id)))
        stmt = apply_pagination_filter(stmt, pagination, DepartmentModel)

        result = await self.session.execute(stmt)
        records = result.unique().scalars().all()
        return records, total
    
    @handle_db_exceptions_async
    @log_repository_call("Department")
    async def search(self, filters: DepartmentFilter, pagination: PaginationRequest) -> tuple[list[DepartmentModel], int]:
        stmt = select(DepartmentModel)
        stmt = apply_filters(stmt, filters, DepartmentModel)

        total = await self.session.scalar(select(func.count()).select_from(stmt.subquery()))
        stmt = apply_pagination_filter(stmt, pagination, DepartmentModel)

        results = await self.session.execute(stmt)
        records = results.unique().scalars().all()
        return records, total


    # ─── Update operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Department")
    async def update_by_id(self, id: int, updates: dict[str, Any]) -> DepartmentModel | None:
        """
        Update Department information
        
        Args:
            id: id of Department to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated Department if successful, None if Department not found
        """
        stmt = select(DepartmentModel).where(DepartmentModel.department_id == id)
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
    @log_repository_call("Department")
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a Department
        
        Args:
            id: id of Department to delete
            
        Returns:
            True if user was deleted, False if user not found
        """
        stmt = select(DepartmentModel).where(DepartmentModel.department_id == id)
        result = await self.session.execute(stmt)
        record = result.unique().scalars().first()
        if record:
            await self.session.delete(record)
            await self.session.commit()
            return True
        return False
