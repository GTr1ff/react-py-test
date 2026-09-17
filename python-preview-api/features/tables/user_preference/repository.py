# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c



from typing import Any
from core.logging.repository_logger import log_repository_call
from core.db_exception_handler import handle_db_exceptions_async
from core.pagination import PaginationRequest, apply_filters, apply_pagination_filter
from features.tables.user_preference.models import UserPreferenceModel
from features.tables.user_preference.schemas import UserPreferenceFilter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

class UserPreferenceRepository:
    """Repository layer for all UserPreference-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
    
    # ─── Create operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("UserPreference")
    async def create(self, userpreference_record: UserPreferenceModel) -> UserPreferenceModel | None:
        """
        Create a new UserPreference

        Args:
            data: New UserPreference data
            
        Returns:
            UserPreference data if created successfully, None if UserPreference already exists
        """
        
        # Create new UserPreference
        self.session.add(userpreference_record)
        await self.session.commit()
        await self.session.refresh(userpreference_record)

        return userpreference_record

    
    # ─── Read operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("UserPreference")
    async def get_by_id(self, id: int) -> UserPreferenceModel | None:
        """
        Get user_preference by id
        
        Args:
            id: The id to search for
            
        Returns:
            UserPreference if found, None otherwise
        """
        stmt = select(UserPreferenceModel).where(UserPreferenceModel.id == id)
        result = await self.session.execute(stmt)
        return result.unique().scalars().first()

    @handle_db_exceptions_async
    @log_repository_call("UserPreference")
    async def get_all(self, pagination: PaginationRequest) -> tuple[list[UserPreferenceModel], int]:
        """
        Get all user_preference
        
        Returns:
            List of all user_preference
        """
        stmt = select(UserPreferenceModel)

        total = await self.session.scalar(select(func.count(UserPreferenceModel.id)))
        stmt = apply_pagination_filter(stmt, pagination, UserPreferenceModel)

        result = await self.session.execute(stmt)
        records = result.unique().scalars().all()
        return records, total
    
    @handle_db_exceptions_async
    @log_repository_call("UserPreference")
    async def search(self, filters: UserPreferenceFilter, pagination: PaginationRequest) -> tuple[list[UserPreferenceModel], int]:
        stmt = select(UserPreferenceModel)
        stmt = apply_filters(stmt, filters, UserPreferenceModel)

        total = await self.session.scalar(select(func.count()).select_from(stmt.subquery()))
        stmt = apply_pagination_filter(stmt, pagination, UserPreferenceModel)

        results = await self.session.execute(stmt)
        records = results.unique().scalars().all()
        return records, total


    # ─── Update operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("UserPreference")
    async def update_by_id(self, id: int, updates: dict[str, Any]) -> UserPreferenceModel | None:
        """
        Update UserPreference information
        
        Args:
            id: id of UserPreference to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated UserPreference if successful, None if UserPreference not found
        """
        stmt = select(UserPreferenceModel).where(UserPreferenceModel.id == id)
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
    @log_repository_call("UserPreference")
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a UserPreference
        
        Args:
            id: id of UserPreference to delete
            
        Returns:
            True if user was deleted, False if user not found
        """
        stmt = select(UserPreferenceModel).where(UserPreferenceModel.id == id)
        result = await self.session.execute(stmt)
        record = result.unique().scalars().first()
        if record:
            await self.session.delete(record)
            await self.session.commit()
            return True
        return False
