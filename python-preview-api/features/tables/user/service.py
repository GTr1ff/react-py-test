# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c



from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from core.pagination import PaginatedResponse, PaginationRequest
from features.tables.user.models import UserModel
from features.tables.user.schemas import UserResponse, UserCreate, UserUpdate, UserFilter
from features.tables.user.repository import UserRepository

class UserService:
    """Service layer for all User-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = UserRepository(session)

    
    # ─── Read operations ──────────────────────────────────id
    async def get_by_id(self, id: int) -> UserResponse | None:
        """
        Get user by id
        
        Args:
            id: The id to search for
            
        Returns:
            UserResponse if found, None if not found
        """
        result = await self.repo.get_by_id(id)
        return UserResponse.model_validate(result) if result else None

    async def get_all(self, pagination: PaginationRequest) -> PaginatedResponse[UserResponse]:
        """
        Get all user
        
        Returns:
            List of all user
        """
        result, total = await self.repo.get_all(pagination)

        return PaginatedResponse[UserResponse](
            items=[UserResponse.model_validate(record) for record in result],
            **pagination.model_dump(),
            total=total
        )

    async def search(self, filters: UserFilter, pagination: PaginationRequest) -> PaginatedResponse[UserResponse]:
        results, total = await self.repo.search(filters, pagination)
        return PaginatedResponse[UserResponse](
            items=[UserResponse.model_validate(record) for record in results],
            **pagination.model_dump(),
            total=total
        )


    # ─── Create operations ──────────────────────────────────
    async def create(self, data: UserCreate) -> UserResponse:
        """
        Create a new User

        Args:
            data: New User data
            
        Returns:
            UserResponse if created successfully, None if User already exists
        """

        # Check if unique fields already exist
        user_model = UserModel(**data.model_dump())
        
        # Create
        result = await self.repo.create(user_model)

        return UserResponse.model_validate(result)

    # ─── Update operations ──────────────────────────────────
    async def update_by_id(self, id: int, updates: UserUpdate) -> UserResponse | None:
        """
        Update User information
        
        Args:
            id: id of User to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated UserResponse if successful, None if User not found
        """    
        result = await self.repo.update_by_id(id, updates.model_dump(exclude_unset=True))
        return UserResponse.model_validate(result) if result else None
    
    # ─── Delete operations ──────────────────────────────────
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a User
        
        Args:
            id: id of User to delete
            
        Returns:
            True if User was deleted, False if User not found
        """
        return await self.repo.delete_by_id(id)
