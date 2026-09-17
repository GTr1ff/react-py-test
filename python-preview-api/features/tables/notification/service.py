# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c



from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from core.pagination import PaginatedResponse, PaginationRequest
from features.tables.notification.models import NotificationModel
from features.tables.notification.schemas import NotificationResponse, NotificationCreate, NotificationUpdate, NotificationFilter
from features.tables.notification.repository import NotificationRepository

class NotificationService:
    """Service layer for all Notification-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = NotificationRepository(session)

    
    # ─── Read operations ──────────────────────────────────id
    async def get_by_id(self, id: int) -> NotificationResponse | None:
        """
        Get notification by id
        
        Args:
            id: The id to search for
            
        Returns:
            NotificationResponse if found, None if not found
        """
        result = await self.repo.get_by_id(id)
        return NotificationResponse.model_validate(result) if result else None

    async def get_all(self, pagination: PaginationRequest) -> PaginatedResponse[NotificationResponse]:
        """
        Get all notification
        
        Returns:
            List of all notification
        """
        result, total = await self.repo.get_all(pagination)

        return PaginatedResponse[NotificationResponse](
            items=[NotificationResponse.model_validate(record) for record in result],
            **pagination.model_dump(),
            total=total
        )

    async def search(self, filters: NotificationFilter, pagination: PaginationRequest) -> PaginatedResponse[NotificationResponse]:
        results, total = await self.repo.search(filters, pagination)
        return PaginatedResponse[NotificationResponse](
            items=[NotificationResponse.model_validate(record) for record in results],
            **pagination.model_dump(),
            total=total
        )


    # ─── Create operations ──────────────────────────────────
    async def create(self, data: NotificationCreate) -> NotificationResponse:
        """
        Create a new Notification

        Args:
            data: New Notification data
            
        Returns:
            NotificationResponse if created successfully, None if Notification already exists
        """

        # Check if unique fields already exist
        notification_model = NotificationModel(**data.model_dump())
        
        # Create
        result = await self.repo.create(notification_model)

        return NotificationResponse.model_validate(result)

    # ─── Update operations ──────────────────────────────────
    async def update_by_id(self, id: int, updates: NotificationUpdate) -> NotificationResponse | None:
        """
        Update Notification information
        
        Args:
            id: id of Notification to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated NotificationResponse if successful, None if Notification not found
        """    
        result = await self.repo.update_by_id(id, updates.model_dump(exclude_unset=True))
        return NotificationResponse.model_validate(result) if result else None
    
    # ─── Delete operations ──────────────────────────────────
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a Notification
        
        Args:
            id: id of Notification to delete
            
        Returns:
            True if Notification was deleted, False if Notification not found
        """
        return await self.repo.delete_by_id(id)
