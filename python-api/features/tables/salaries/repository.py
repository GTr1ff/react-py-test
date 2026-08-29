# ROSETIC:crud-guid



from typing import Any
from core.logging.repository_logger import log_repository_call
from core.db_exception_handler import handle_db_exceptions_async
from core.pagination import PaginationRequest, apply_filters, apply_pagination_filter
from features.tables.salaries.models import SalaryModel
from features.tables.salaries.schemas import SalaryFilter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

class SalaryRepository:
    """Repository layer for all Salary-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
    
    # ─── Create operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Salary")
    async def create(self, salary_record: SalaryModel) -> SalaryModel | None:
        """
        Create a new Salary

        Args:
            data: New Salary data
            
        Returns:
            Salary data if created successfully, None if Salary already exists
        """
        
        # Create new Salary
        self.session.add(salary_record)
        await self.session.commit()
        await self.session.refresh(salary_record)

        return salary_record

    
    # ─── Read operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Salary")
    async def get_by_id(self, id: int) -> SalaryModel | None:
        """
        Get salaries by id
        
        Args:
            id: The id to search for
            
        Returns:
            Salary if found, None otherwise
        """
        stmt = select(SalaryModel).where(SalaryModel.salary_id == id)
        result = await self.session.execute(stmt)
        return result.unique().scalars().first()

    @handle_db_exceptions_async
    @log_repository_call("Salary")
    async def get_all(self, pagination: PaginationRequest) -> tuple[list[SalaryModel], int]:
        """
        Get all salaries
        
        Returns:
            List of all salaries
        """
        stmt = select(SalaryModel)

        total = await self.session.scalar(select(func.count(SalaryModel.salary_id)))
        stmt = apply_pagination_filter(stmt, pagination, SalaryModel)

        result = await self.session.execute(stmt)
        records = result.unique().scalars().all()
        return records, total
    
    @handle_db_exceptions_async
    @log_repository_call("Salary")
    async def search(self, filters: SalaryFilter, pagination: PaginationRequest) -> tuple[list[SalaryModel], int]:
        stmt = select(SalaryModel)
        stmt = apply_filters(stmt, filters, SalaryModel)

        total = await self.session.scalar(select(func.count()).select_from(stmt.subquery()))
        stmt = apply_pagination_filter(stmt, pagination, SalaryModel)

        results = await self.session.execute(stmt)
        records = results.unique().scalars().all()
        return records, total


    # ─── Update operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Salary")
    async def update_by_id(self, id: int, updates: dict[str, Any]) -> SalaryModel | None:
        """
        Update Salary information
        
        Args:
            id: id of Salary to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated Salary if successful, None if Salary not found
        """
        stmt = select(SalaryModel).where(SalaryModel.salary_id == id)
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
    @log_repository_call("Salary")
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a Salary
        
        Args:
            id: id of Salary to delete
            
        Returns:
            True if user was deleted, False if user not found
        """
        stmt = select(SalaryModel).where(SalaryModel.salary_id == id)
        result = await self.session.execute(stmt)
        record = result.unique().scalars().first()
        if record:
            await self.session.delete(record)
            await self.session.commit()
            return True
        return False
