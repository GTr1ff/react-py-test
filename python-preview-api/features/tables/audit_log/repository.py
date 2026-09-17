# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c



from typing import Any
from core.logging.repository_logger import log_repository_call
from core.db_exception_handler import handle_db_exceptions_async
from core.pagination import PaginationRequest, apply_filters, apply_pagination_filter
from features.tables.audit_log.models import AuditLogModel
from features.tables.audit_log.schemas import AuditLogFilter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

class AuditLogRepository:
    """Repository layer for all AuditLog-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
    
    # ─── Create operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("AuditLog")
    async def create(self, auditlog_record: AuditLogModel) -> AuditLogModel | None:
        """
        Create a new AuditLog

        Args:
            data: New AuditLog data
            
        Returns:
            AuditLog data if created successfully, None if AuditLog already exists
        """
        
        # Create new AuditLog
        self.session.add(auditlog_record)
        await self.session.commit()
        await self.session.refresh(auditlog_record)

        return auditlog_record

    
    # ─── Read operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("AuditLog")
    async def get_by_id(self, id: int) -> AuditLogModel | None:
        """
        Get audit_log by id
        
        Args:
            id: The id to search for
            
        Returns:
            AuditLog if found, None otherwise
        """
        stmt = select(AuditLogModel).where(AuditLogModel.id == id)
        result = await self.session.execute(stmt)
        return result.unique().scalars().first()

    @handle_db_exceptions_async
    @log_repository_call("AuditLog")
    async def get_all(self, pagination: PaginationRequest) -> tuple[list[AuditLogModel], int]:
        """
        Get all audit_log
        
        Returns:
            List of all audit_log
        """
        stmt = select(AuditLogModel)

        total = await self.session.scalar(select(func.count(AuditLogModel.id)))
        stmt = apply_pagination_filter(stmt, pagination, AuditLogModel)

        result = await self.session.execute(stmt)
        records = result.unique().scalars().all()
        return records, total
    
    @handle_db_exceptions_async
    @log_repository_call("AuditLog")
    async def search(self, filters: AuditLogFilter, pagination: PaginationRequest) -> tuple[list[AuditLogModel], int]:
        stmt = select(AuditLogModel)
        stmt = apply_filters(stmt, filters, AuditLogModel)

        total = await self.session.scalar(select(func.count()).select_from(stmt.subquery()))
        stmt = apply_pagination_filter(stmt, pagination, AuditLogModel)

        results = await self.session.execute(stmt)
        records = results.unique().scalars().all()
        return records, total


    # ─── Update operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("AuditLog")
    async def update_by_id(self, id: int, updates: dict[str, Any]) -> AuditLogModel | None:
        """
        Update AuditLog information
        
        Args:
            id: id of AuditLog to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated AuditLog if successful, None if AuditLog not found
        """
        stmt = select(AuditLogModel).where(AuditLogModel.id == id)
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
    @log_repository_call("AuditLog")
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a AuditLog
        
        Args:
            id: id of AuditLog to delete
            
        Returns:
            True if user was deleted, False if user not found
        """
        stmt = select(AuditLogModel).where(AuditLogModel.id == id)
        result = await self.session.execute(stmt)
        record = result.unique().scalars().first()
        if record:
            await self.session.delete(record)
            await self.session.commit()
            return True
        return False
