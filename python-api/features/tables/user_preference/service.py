# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c



from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from core.pagination import PaginatedResponse, PaginationRequest
from features.tables.user_preference.models import UserPreferenceModel
from features.tables.user_preference.schemas import UserPreferenceResponse, UserPreferenceCreate, UserPreferenceUpdate, UserPreferenceFilter
from features.tables.user_preference.repository import UserPreferenceRepository

class UserPreferenceService:
    """Service layer for all UserPreference-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = UserPreferenceRepository(session)

    
    # ─── Read operations ──────────────────────────────────id
    async def get_by_id(self, id: int) -> UserPreferenceResponse | None:
        """
        Get user_preference by id
        
        Args:
            id: The id to search for
            
        Returns:
            UserPreferenceResponse if found, None if not found
        """
        result = await self.repo.get_by_id(id)
        return UserPreferenceResponse.model_validate(result) if result else None

    async def get_all(self, pagination: PaginationRequest) -> PaginatedResponse[UserPreferenceResponse]:
        """
        Get all user_preference
        
        Returns:
            List of all user_preference
        """
        result, total = await self.repo.get_all(pagination)

        return PaginatedResponse[UserPreferenceResponse](
            items=[UserPreferenceResponse.model_validate(record) for record in result],
            **pagination.model_dump(),
            total=total
        )

    async def search(self, filters: UserPreferenceFilter, pagination: PaginationRequest) -> PaginatedResponse[UserPreferenceResponse]:
        results, total = await self.repo.search(filters, pagination)
        return PaginatedResponse[UserPreferenceResponse](
            items=[UserPreferenceResponse.model_validate(record) for record in results],
            **pagination.model_dump(),
            total=total
        )


    # ─── Create operations ──────────────────────────────────
    async def create(self, data: UserPreferenceCreate) -> UserPreferenceResponse:
        """
        Create a new UserPreference

        Args:
            data: New UserPreference data
            
        Returns:
            UserPreferenceResponse if created successfully, None if UserPreference already exists
        """

        # Check if unique fields already exist
        userpreference_model = UserPreferenceModel(**data.model_dump())
        
        # Create
        result = await self.repo.create(userpreference_model)

        return UserPreferenceResponse.model_validate(result)

    # ─── Update operations ──────────────────────────────────
    async def update_by_id(self, id: int, updates: UserPreferenceUpdate) -> UserPreferenceResponse | None:
        """
        Update UserPreference information
        
        Args:
            id: id of UserPreference to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated UserPreferenceResponse if successful, None if UserPreference not found
        """    
        result = await self.repo.update_by_id(id, updates.model_dump(exclude_unset=True))
        return UserPreferenceResponse.model_validate(result) if result else None
    
    # ─── Delete operations ──────────────────────────────────
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a UserPreference
        
        Args:
            id: id of UserPreference to delete
            
        Returns:
            True if UserPreference was deleted, False if UserPreference not found
        """
        return await self.repo.delete_by_id(id)
