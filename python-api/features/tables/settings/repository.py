# ROSETIC:crud-guid



from typing import Any
from core.logging.repository_logger import log_repository_call
from core.db_exception_handler import handle_db_exceptions_async
from core.pagination import PaginationRequest, apply_filters, apply_pagination_filter
from features.tables.settings.models import SettingModel
from features.tables.settings.schemas import SettingFilter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

class SettingRepository:
    """Repository layer for all Setting-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
    
    # ─── Create operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Setting")
    async def create(self, setting_record: SettingModel) -> SettingModel | None:
        """
        Create a new Setting

        Args:
            data: New Setting data
            
        Returns:
            Setting data if created successfully, None if Setting already exists
        """
        
        # Create new Setting
        self.session.add(setting_record)
        await self.session.commit()
        await self.session.refresh(setting_record)

        return setting_record

    
    # ─── Read operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Setting")
    async def get_by_id(self, id: int) -> SettingModel | None:
        """
        Get settings by id
        
        Args:
            id: The id to search for
            
        Returns:
            Setting if found, None otherwise
        """
        stmt = select(SettingModel).where(SettingModel.setting_id == id)
        result = await self.session.execute(stmt)
        return result.unique().scalars().first()

    @handle_db_exceptions_async
    @log_repository_call("Setting")
    async def get_all(self, pagination: PaginationRequest) -> tuple[list[SettingModel], int]:
        """
        Get all settings
        
        Returns:
            List of all settings
        """
        stmt = select(SettingModel)

        total = await self.session.scalar(select(func.count(SettingModel.setting_id)))
        stmt = apply_pagination_filter(stmt, pagination, SettingModel)

        result = await self.session.execute(stmt)
        records = result.unique().scalars().all()
        return records, total
    
    @handle_db_exceptions_async
    @log_repository_call("Setting")
    async def search(self, filters: SettingFilter, pagination: PaginationRequest) -> tuple[list[SettingModel], int]:
        stmt = select(SettingModel)
        stmt = apply_filters(stmt, filters, SettingModel)

        total = await self.session.scalar(select(func.count()).select_from(stmt.subquery()))
        stmt = apply_pagination_filter(stmt, pagination, SettingModel)

        results = await self.session.execute(stmt)
        records = results.unique().scalars().all()
        return records, total


    # ─── Update operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Setting")
    async def update_by_id(self, id: int, updates: dict[str, Any]) -> SettingModel | None:
        """
        Update Setting information
        
        Args:
            id: id of Setting to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated Setting if successful, None if Setting not found
        """
        stmt = select(SettingModel).where(SettingModel.setting_id == id)
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
    @log_repository_call("Setting")
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a Setting
        
        Args:
            id: id of Setting to delete
            
        Returns:
            True if user was deleted, False if user not found
        """
        stmt = select(SettingModel).where(SettingModel.setting_id == id)
        result = await self.session.execute(stmt)
        record = result.unique().scalars().first()
        if record:
            await self.session.delete(record)
            await self.session.commit()
            return True
        return False
