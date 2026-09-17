# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c



from typing import Any
from core.logging.repository_logger import log_repository_call
from core.db_exception_handler import handle_db_exceptions_async
from core.pagination import PaginationRequest, apply_filters, apply_pagination_filter
from features.tables.notification.models import NotificationModel
from features.tables.notification.schemas import NotificationFilter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

class NotificationRepository:
    """Repository layer for all Notification-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
    
    # ─── Create operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Notification")
    async def create(self, notification_record: NotificationModel) -> NotificationModel | None:
        """
        Create a new Notification

        Args:
            data: New Notification data
            
        Returns:
            Notification data if created successfully, None if Notification already exists
        """
        
        # Create new Notification
        self.session.add(notification_record)
        await self.session.commit()
        await self.session.refresh(notification_record)

        return notification_record

    
    # ─── Read operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Notification")
    async def get_by_id(self, id: int) -> NotificationModel | None:
        """
        Get notification by id
        
        Args:
            id: The id to search for
            
        Returns:
            Notification if found, None otherwise
        """
        stmt = select(NotificationModel).where(NotificationModel.id == id)
        result = await self.session.execute(stmt)
        return result.unique().scalars().first()

    @handle_db_exceptions_async
    @log_repository_call("Notification")
    async def get_all(self, pagination: PaginationRequest) -> tuple[list[NotificationModel], int]:
        """
        Get all notification
        
        Returns:
            List of all notification
        """
        stmt = select(NotificationModel)

        total = await self.session.scalar(select(func.count(NotificationModel.id)))
        stmt = apply_pagination_filter(stmt, pagination, NotificationModel)

        result = await self.session.execute(stmt)
        records = result.unique().scalars().all()
        return records, total
    
    @handle_db_exceptions_async
    @log_repository_call("Notification")
    async def search(self, filters: NotificationFilter, pagination: PaginationRequest) -> tuple[list[NotificationModel], int]:
        stmt = select(NotificationModel)
        stmt = apply_filters(stmt, filters, NotificationModel)

        total = await self.session.scalar(select(func.count()).select_from(stmt.subquery()))
        stmt = apply_pagination_filter(stmt, pagination, NotificationModel)

        results = await self.session.execute(stmt)
        records = results.unique().scalars().all()
        return records, total


    # ─── Update operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Notification")
    async def update_by_id(self, id: int, updates: dict[str, Any]) -> NotificationModel | None:
        """
        Update Notification information
        
        Args:
            id: id of Notification to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated Notification if successful, None if Notification not found
        """
        stmt = select(NotificationModel).where(NotificationModel.id == id)
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
    @log_repository_call("Notification")
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a Notification
        
        Args:
            id: id of Notification to delete
            
        Returns:
            True if user was deleted, False if user not found
        """
        stmt = select(NotificationModel).where(NotificationModel.id == id)
        result = await self.session.execute(stmt)
        record = result.unique().scalars().first()
        if record:
            await self.session.delete(record)
            await self.session.commit()
            return True
        return False
