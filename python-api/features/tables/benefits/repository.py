# ROSETIC:crud-guid



from typing import Any
from core.logging.repository_logger import log_repository_call
from core.db_exception_handler import handle_db_exceptions_async
from core.pagination import PaginationRequest, apply_filters, apply_pagination_filter
from features.tables.benefits.models import BenefitModel
from features.tables.benefits.schemas import BenefitFilter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

class BenefitRepository:
    """Repository layer for all Benefit-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
    
    # ─── Create operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Benefit")
    async def create(self, benefit_record: BenefitModel) -> BenefitModel | None:
        """
        Create a new Benefit

        Args:
            data: New Benefit data
            
        Returns:
            Benefit data if created successfully, None if Benefit already exists
        """
        
        # Create new Benefit
        self.session.add(benefit_record)
        await self.session.commit()
        await self.session.refresh(benefit_record)

        return benefit_record

    
    # ─── Read operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Benefit")
    async def get_by_id(self, id: int) -> BenefitModel | None:
        """
        Get benefits by id
        
        Args:
            id: The id to search for
            
        Returns:
            Benefit if found, None otherwise
        """
        stmt = select(BenefitModel).where(BenefitModel.benefit_id == id)
        result = await self.session.execute(stmt)
        return result.unique().scalars().first()

    @handle_db_exceptions_async
    @log_repository_call("Benefit")
    async def get_all(self, pagination: PaginationRequest) -> tuple[list[BenefitModel], int]:
        """
        Get all benefits
        
        Returns:
            List of all benefits
        """
        stmt = select(BenefitModel)

        total = await self.session.scalar(select(func.count(BenefitModel.benefit_id)))
        stmt = apply_pagination_filter(stmt, pagination, BenefitModel)

        result = await self.session.execute(stmt)
        records = result.unique().scalars().all()
        return records, total
    
    @handle_db_exceptions_async
    @log_repository_call("Benefit")
    async def search(self, filters: BenefitFilter, pagination: PaginationRequest) -> tuple[list[BenefitModel], int]:
        stmt = select(BenefitModel)
        stmt = apply_filters(stmt, filters, BenefitModel)

        total = await self.session.scalar(select(func.count()).select_from(stmt.subquery()))
        stmt = apply_pagination_filter(stmt, pagination, BenefitModel)

        results = await self.session.execute(stmt)
        records = results.unique().scalars().all()
        return records, total


    # ─── Update operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Benefit")
    async def update_by_id(self, id: int, updates: dict[str, Any]) -> BenefitModel | None:
        """
        Update Benefit information
        
        Args:
            id: id of Benefit to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated Benefit if successful, None if Benefit not found
        """
        stmt = select(BenefitModel).where(BenefitModel.benefit_id == id)
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
    @log_repository_call("Benefit")
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a Benefit
        
        Args:
            id: id of Benefit to delete
            
        Returns:
            True if user was deleted, False if user not found
        """
        stmt = select(BenefitModel).where(BenefitModel.benefit_id == id)
        result = await self.session.execute(stmt)
        record = result.unique().scalars().first()
        if record:
            await self.session.delete(record)
            await self.session.commit()
            return True
        return False
