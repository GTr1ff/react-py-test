# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c



from typing import Any
from core.logging.repository_logger import log_repository_call
from core.db_exception_handler import handle_db_exceptions_async
from core.pagination import PaginationRequest, apply_filters, apply_pagination_filter
from features.tables.consent.models import ConsentModel
from features.tables.consent.schemas import ConsentFilter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

class ConsentRepository:
    """Repository layer for all Consent-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
    
    # ─── Create operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Consent")
    async def create(self, consent_record: ConsentModel) -> ConsentModel | None:
        """
        Create a new Consent

        Args:
            data: New Consent data
            
        Returns:
            Consent data if created successfully, None if Consent already exists
        """
        
        # Create new Consent
        self.session.add(consent_record)
        await self.session.commit()
        await self.session.refresh(consent_record)

        return consent_record

    
    # ─── Read operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Consent")
    async def get_by_id(self, id: int) -> ConsentModel | None:
        """
        Get consent by id
        
        Args:
            id: The id to search for
            
        Returns:
            Consent if found, None otherwise
        """
        stmt = select(ConsentModel).where(ConsentModel.id == id)
        result = await self.session.execute(stmt)
        return result.unique().scalars().first()

    @handle_db_exceptions_async
    @log_repository_call("Consent")
    async def get_all(self, pagination: PaginationRequest) -> tuple[list[ConsentModel], int]:
        """
        Get all consent
        
        Returns:
            List of all consent
        """
        stmt = select(ConsentModel)

        total = await self.session.scalar(select(func.count(ConsentModel.id)))
        stmt = apply_pagination_filter(stmt, pagination, ConsentModel)

        result = await self.session.execute(stmt)
        records = result.unique().scalars().all()
        return records, total
    
    @handle_db_exceptions_async
    @log_repository_call("Consent")
    async def search(self, filters: ConsentFilter, pagination: PaginationRequest) -> tuple[list[ConsentModel], int]:
        stmt = select(ConsentModel)
        stmt = apply_filters(stmt, filters, ConsentModel)

        total = await self.session.scalar(select(func.count()).select_from(stmt.subquery()))
        stmt = apply_pagination_filter(stmt, pagination, ConsentModel)

        results = await self.session.execute(stmt)
        records = results.unique().scalars().all()
        return records, total


    # ─── Update operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Consent")
    async def update_by_id(self, id: int, updates: dict[str, Any]) -> ConsentModel | None:
        """
        Update Consent information
        
        Args:
            id: id of Consent to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated Consent if successful, None if Consent not found
        """
        stmt = select(ConsentModel).where(ConsentModel.id == id)
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
    @log_repository_call("Consent")
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a Consent
        
        Args:
            id: id of Consent to delete
            
        Returns:
            True if user was deleted, False if user not found
        """
        stmt = select(ConsentModel).where(ConsentModel.id == id)
        result = await self.session.execute(stmt)
        record = result.unique().scalars().first()
        if record:
            await self.session.delete(record)
            await self.session.commit()
            return True
        return False
