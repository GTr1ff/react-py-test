# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c



from typing import Any
from core.logging.repository_logger import log_repository_call
from core.db_exception_handler import handle_db_exceptions_async
from core.pagination import PaginationRequest, apply_filters, apply_pagination_filter
from features.tables.user.models import UserModel
from features.tables.user.schemas import UserFilter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

class UserRepository:
    """Repository layer for all User-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
    
    # ─── Create operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("User")
    async def create(self, user_record: UserModel) -> UserModel | None:
        """
        Create a new User

        Args:
            data: New User data
            
        Returns:
            User data if created successfully, None if User already exists
        """
        
        # Create new User
        self.session.add(user_record)
        await self.session.commit()
        await self.session.refresh(user_record)

        return user_record

    
    # ─── Read operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("User")
    async def get_by_id(self, id: int) -> UserModel | None:
        """
        Get user by id
        
        Args:
            id: The id to search for
            
        Returns:
            User if found, None otherwise
        """
        stmt = select(UserModel).where(UserModel.id == id)
        result = await self.session.execute(stmt)
        return result.unique().scalars().first()

    @handle_db_exceptions_async
    @log_repository_call("User")
    async def get_all(self, pagination: PaginationRequest) -> tuple[list[UserModel], int]:
        """
        Get all user
        
        Returns:
            List of all user
        """
        stmt = select(UserModel)

        total = await self.session.scalar(select(func.count(UserModel.id)))
        stmt = apply_pagination_filter(stmt, pagination, UserModel)

        result = await self.session.execute(stmt)
        records = result.unique().scalars().all()
        return records, total
    
    @handle_db_exceptions_async
    @log_repository_call("User")
    async def search(self, filters: UserFilter, pagination: PaginationRequest) -> tuple[list[UserModel], int]:
        stmt = select(UserModel)
        stmt = apply_filters(stmt, filters, UserModel)

        total = await self.session.scalar(select(func.count()).select_from(stmt.subquery()))
        stmt = apply_pagination_filter(stmt, pagination, UserModel)

        results = await self.session.execute(stmt)
        records = results.unique().scalars().all()
        return records, total


    # ─── Update operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("User")
    async def update_by_id(self, id: int, updates: dict[str, Any]) -> UserModel | None:
        """
        Update User information
        
        Args:
            id: id of User to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated User if successful, None if User not found
        """
        stmt = select(UserModel).where(UserModel.id == id)
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
    @log_repository_call("User")
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a User
        
        Args:
            id: id of User to delete
            
        Returns:
            True if user was deleted, False if user not found
        """
        stmt = select(UserModel).where(UserModel.id == id)
        result = await self.session.execute(stmt)
        record = result.unique().scalars().first()
        if record:
            await self.session.delete(record)
            await self.session.commit()
            return True
        return False
