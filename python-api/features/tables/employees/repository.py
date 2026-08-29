# ROSETIC:crud-guid



from typing import Any
from core.logging.repository_logger import log_repository_call
from core.db_exception_handler import handle_db_exceptions_async
from core.pagination import PaginationRequest, apply_filters, apply_pagination_filter
from features.tables.employees.models import EmployeeModel
from features.tables.employees.schemas import EmployeeFilter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

class EmployeeRepository:
    """Repository layer for all Employee-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
    
    # ─── Create operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Employee")
    async def create(self, employee_record: EmployeeModel) -> EmployeeModel | None:
        """
        Create a new Employee

        Args:
            data: New Employee data
            
        Returns:
            Employee data if created successfully, None if Employee already exists
        """
        
        # Create new Employee
        self.session.add(employee_record)
        await self.session.commit()
        await self.session.refresh(employee_record)

        return employee_record

    
    # ─── Read operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Employee")
    async def get_by_id(self, id: int) -> EmployeeModel | None:
        """
        Get employees by id
        
        Args:
            id: The id to search for
            
        Returns:
            Employee if found, None otherwise
        """
        stmt = select(EmployeeModel).where(EmployeeModel.employee_id == id)
        result = await self.session.execute(stmt)
        return result.unique().scalars().first()

    @handle_db_exceptions_async
    @log_repository_call("Employee")
    async def get_all(self, pagination: PaginationRequest) -> tuple[list[EmployeeModel], int]:
        """
        Get all employees
        
        Returns:
            List of all employees
        """
        stmt = select(EmployeeModel)

        total = await self.session.scalar(select(func.count(EmployeeModel.employee_id)))
        stmt = apply_pagination_filter(stmt, pagination, EmployeeModel)

        result = await self.session.execute(stmt)
        records = result.unique().scalars().all()
        return records, total
    
    @handle_db_exceptions_async
    @log_repository_call("Employee")
    async def search(self, filters: EmployeeFilter, pagination: PaginationRequest) -> tuple[list[EmployeeModel], int]:
        stmt = select(EmployeeModel)
        stmt = apply_filters(stmt, filters, EmployeeModel)

        total = await self.session.scalar(select(func.count()).select_from(stmt.subquery()))
        stmt = apply_pagination_filter(stmt, pagination, EmployeeModel)

        results = await self.session.execute(stmt)
        records = results.unique().scalars().all()
        return records, total


    # ─── Update operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Employee")
    async def update_by_id(self, id: int, updates: dict[str, Any]) -> EmployeeModel | None:
        """
        Update Employee information
        
        Args:
            id: id of Employee to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated Employee if successful, None if Employee not found
        """
        stmt = select(EmployeeModel).where(EmployeeModel.employee_id == id)
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
    @log_repository_call("Employee")
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a Employee
        
        Args:
            id: id of Employee to delete
            
        Returns:
            True if user was deleted, False if user not found
        """
        stmt = select(EmployeeModel).where(EmployeeModel.employee_id == id)
        result = await self.session.execute(stmt)
        record = result.unique().scalars().first()
        if record:
            await self.session.delete(record)
            await self.session.commit()
            return True
        return False
