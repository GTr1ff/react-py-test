# ROSETIC:crud-guid



from typing import Any
from core.logging.repository_logger import log_repository_call
from core.db_exception_handler import handle_db_exceptions_async
from core.pagination import PaginationRequest, apply_filters, apply_pagination_filter
from features.tables.payroll.models import PayrollModel
from features.tables.payroll.schemas import PayrollFilter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

class PayrollRepository:
    """Repository layer for all Payroll-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
    
    # ─── Create operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Payroll")
    async def create(self, payroll_record: PayrollModel) -> PayrollModel | None:
        """
        Create a new Payroll

        Args:
            data: New Payroll data
            
        Returns:
            Payroll data if created successfully, None if Payroll already exists
        """
        
        # Create new Payroll
        self.session.add(payroll_record)
        await self.session.commit()
        await self.session.refresh(payroll_record)

        return payroll_record

    
    # ─── Read operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Payroll")
    async def get_by_id(self, id: int) -> PayrollModel | None:
        """
        Get payroll by id
        
        Args:
            id: The id to search for
            
        Returns:
            Payroll if found, None otherwise
        """
        stmt = select(PayrollModel).where(PayrollModel.payroll_id == id)
        result = await self.session.execute(stmt)
        return result.unique().scalars().first()

    @handle_db_exceptions_async
    @log_repository_call("Payroll")
    async def get_all(self, pagination: PaginationRequest) -> tuple[list[PayrollModel], int]:
        """
        Get all payroll
        
        Returns:
            List of all payroll
        """
        stmt = select(PayrollModel)

        total = await self.session.scalar(select(func.count(PayrollModel.payroll_id)))
        stmt = apply_pagination_filter(stmt, pagination, PayrollModel)

        result = await self.session.execute(stmt)
        records = result.unique().scalars().all()
        return records, total
    
    @handle_db_exceptions_async
    @log_repository_call("Payroll")
    async def search(self, filters: PayrollFilter, pagination: PaginationRequest) -> tuple[list[PayrollModel], int]:
        stmt = select(PayrollModel)
        stmt = apply_filters(stmt, filters, PayrollModel)

        total = await self.session.scalar(select(func.count()).select_from(stmt.subquery()))
        stmt = apply_pagination_filter(stmt, pagination, PayrollModel)

        results = await self.session.execute(stmt)
        records = results.unique().scalars().all()
        return records, total


    # ─── Update operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Payroll")
    async def update_by_id(self, id: int, updates: dict[str, Any]) -> PayrollModel | None:
        """
        Update Payroll information
        
        Args:
            id: id of Payroll to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated Payroll if successful, None if Payroll not found
        """
        stmt = select(PayrollModel).where(PayrollModel.payroll_id == id)
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
    @log_repository_call("Payroll")
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a Payroll
        
        Args:
            id: id of Payroll to delete
            
        Returns:
            True if user was deleted, False if user not found
        """
        stmt = select(PayrollModel).where(PayrollModel.payroll_id == id)
        result = await self.session.execute(stmt)
        record = result.unique().scalars().first()
        if record:
            await self.session.delete(record)
            await self.session.commit()
            return True
        return False
