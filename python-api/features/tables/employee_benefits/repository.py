# ROSETIC:crud-guid



from typing import Any
from core.logging.repository_logger import log_repository_call
from core.db_exception_handler import handle_db_exceptions_async
from core.pagination import PaginationRequest, apply_filters, apply_pagination_filter
from features.tables.employee_benefits.models import EmployeeBenefitModel
from features.tables.employee_benefits.schemas import EmployeeBenefitFilter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

class EmployeeBenefitRepository:
    """Repository layer for all EmployeeBenefit-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
    
    # ─── Create operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("EmployeeBenefit")
    async def create(self, employeebenefit_record: EmployeeBenefitModel) -> EmployeeBenefitModel | None:
        """
        Create a new EmployeeBenefit

        Args:
            data: New EmployeeBenefit data
            
        Returns:
            EmployeeBenefit data if created successfully, None if EmployeeBenefit already exists
        """
        
        # Create new EmployeeBenefit
        self.session.add(employeebenefit_record)
        await self.session.commit()
        await self.session.refresh(employeebenefit_record)

        return employeebenefit_record

    
    # ─── Read operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("EmployeeBenefit")
    async def get_by_id(self, id: int) -> EmployeeBenefitModel | None:
        """
        Get employee_benefits by id
        
        Args:
            id: The id to search for
            
        Returns:
            EmployeeBenefit if found, None otherwise
        """
        stmt = select(EmployeeBenefitModel).where(EmployeeBenefitModel.employee_benefit_id == id)
        result = await self.session.execute(stmt)
        return result.unique().scalars().first()

    @handle_db_exceptions_async
    @log_repository_call("EmployeeBenefit")
    async def get_all(self, pagination: PaginationRequest) -> tuple[list[EmployeeBenefitModel], int]:
        """
        Get all employee_benefits
        
        Returns:
            List of all employee_benefits
        """
        stmt = select(EmployeeBenefitModel)

        total = await self.session.scalar(select(func.count(EmployeeBenefitModel.employee_benefit_id)))
        stmt = apply_pagination_filter(stmt, pagination, EmployeeBenefitModel)

        result = await self.session.execute(stmt)
        records = result.unique().scalars().all()
        return records, total
    
    @handle_db_exceptions_async
    @log_repository_call("EmployeeBenefit")
    async def search(self, filters: EmployeeBenefitFilter, pagination: PaginationRequest) -> tuple[list[EmployeeBenefitModel], int]:
        stmt = select(EmployeeBenefitModel)
        stmt = apply_filters(stmt, filters, EmployeeBenefitModel)

        total = await self.session.scalar(select(func.count()).select_from(stmt.subquery()))
        stmt = apply_pagination_filter(stmt, pagination, EmployeeBenefitModel)

        results = await self.session.execute(stmt)
        records = results.unique().scalars().all()
        return records, total


    # ─── Update operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("EmployeeBenefit")
    async def update_by_id(self, id: int, updates: dict[str, Any]) -> EmployeeBenefitModel | None:
        """
        Update EmployeeBenefit information
        
        Args:
            id: id of EmployeeBenefit to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated EmployeeBenefit if successful, None if EmployeeBenefit not found
        """
        stmt = select(EmployeeBenefitModel).where(EmployeeBenefitModel.employee_benefit_id == id)
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
    @log_repository_call("EmployeeBenefit")
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a EmployeeBenefit
        
        Args:
            id: id of EmployeeBenefit to delete
            
        Returns:
            True if user was deleted, False if user not found
        """
        stmt = select(EmployeeBenefitModel).where(EmployeeBenefitModel.employee_benefit_id == id)
        result = await self.session.execute(stmt)
        record = result.unique().scalars().first()
        if record:
            await self.session.delete(record)
            await self.session.commit()
            return True
        return False
