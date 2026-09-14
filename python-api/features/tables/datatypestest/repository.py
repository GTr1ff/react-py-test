# ROSETIC:crud-guid


import uuid
from typing import Any
from core.logging.repository_logger import log_repository_call
from core.db_exception_handler import handle_db_exceptions_async
from core.pagination import PaginationRequest, apply_filters, apply_pagination_filter
from features.tables.datatypestest.models import DatatypestestModel
from features.tables.datatypestest.schemas import DatatypestestFilter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

class DatatypestestRepository:
    """Repository layer for all Datatypestest-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
    
    # ─── Create operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Datatypestest")
    async def create(self, datatypestest_record: DatatypestestModel) -> DatatypestestModel | None:
        """
        Create a new Datatypestest

        Args:
            data: New Datatypestest data
            
        Returns:
            Datatypestest data if created successfully, None if Datatypestest already exists
        """
        
        # Create new Datatypestest
        self.session.add(datatypestest_record)
        await self.session.commit()
        await self.session.refresh(datatypestest_record)

        return datatypestest_record

    
    # ─── Read operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Datatypestest")
    async def get_by_keykey(self, keykey: int) -> DatatypestestModel | None:
        """
        Get datatypestest by keykey
        
        Args:
            keykey: The keykey to search for
            
        Returns:
            Datatypestest if found, None otherwise
        """
        stmt = select(DatatypestestModel).where(DatatypestestModel.keykey == keykey)
        result = await self.session.execute(stmt)
        return result.unique().scalars().first()

    @handle_db_exceptions_async
    @log_repository_call("Datatypestest")
    async def get_all(self, pagination: PaginationRequest) -> tuple[list[DatatypestestModel], int]:
        """
        Get all datatypestest
        
        Returns:
            List of all datatypestest
        """
        stmt = select(DatatypestestModel)

        total = await self.session.scalar(select(func.count(DatatypestestModel.keykey)))
        stmt = apply_pagination_filter(stmt, pagination, DatatypestestModel)

        result = await self.session.execute(stmt)
        records = result.unique().scalars().all()
        return records, total
    
    @handle_db_exceptions_async
    @log_repository_call("Datatypestest")
    async def search(self, filters: DatatypestestFilter, pagination: PaginationRequest) -> tuple[list[DatatypestestModel], int]:
        stmt = select(DatatypestestModel)
        stmt = apply_filters(stmt, filters, DatatypestestModel)

        total = await self.session.scalar(select(func.count()).select_from(stmt.subquery()))
        stmt = apply_pagination_filter(stmt, pagination, DatatypestestModel)

        results = await self.session.execute(stmt)
        records = results.unique().scalars().all()
        return records, total


    # ─── Update operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Datatypestest")
    async def update_by_keykey(self, keykey: int, updates: dict[str, Any]) -> DatatypestestModel | None:
        """
        Update Datatypestest information
        
        Args:
            keykey: keykey of Datatypestest to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated Datatypestest if successful, None if Datatypestest not found
        """
        stmt = select(DatatypestestModel).where(DatatypestestModel.keykey == keykey)
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
    @log_repository_call("Datatypestest")
    async def delete_by_keykey(self, keykey: int) -> bool:
        """
        Delete a Datatypestest
        
        Args:
            keykey: keykey of Datatypestest to delete
            
        Returns:
            True if user was deleted, False if user not found
        """
        stmt = select(DatatypestestModel).where(DatatypestestModel.keykey == keykey)
        result = await self.session.execute(stmt)
        record = result.unique().scalars().first()
        if record:
            await self.session.delete(record)
            await self.session.commit()
            return True
        return False
