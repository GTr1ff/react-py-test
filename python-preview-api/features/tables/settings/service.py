# ROSETIC:crud-guid



from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from core.pagination import PaginatedResponse, PaginationRequest
from features.tables.settings.models import SettingModel
from features.tables.settings.schemas import SettingResponse, SettingCreate, SettingUpdate, SettingFilter
from features.tables.settings.repository import SettingRepository

class SettingService:
    """Service layer for all Setting-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = SettingRepository(session)

    
    # ─── Read operations ──────────────────────────────────id
    async def get_by_id(self, id: int) -> SettingResponse | None:
        """
        Get settings by id
        
        Args:
            id: The id to search for
            
        Returns:
            SettingResponse if found, None if not found
        """
        result = await self.repo.get_by_id(id)
        return SettingResponse.model_validate(result) if result else None

    async def get_all(self, pagination: PaginationRequest) -> PaginatedResponse[SettingResponse]:
        """
        Get all settings
        
        Returns:
            List of all settings
        """
        result, total = await self.repo.get_all(pagination)

        return PaginatedResponse[SettingResponse](
            items=[SettingResponse.model_validate(record) for record in result],
            **pagination.model_dump(),
            total=total
        )

    async def search(self, filters: SettingFilter, pagination: PaginationRequest) -> PaginatedResponse[SettingResponse]:
        results, total = await self.repo.search(filters, pagination)
        return PaginatedResponse[SettingResponse](
            items=[SettingResponse.model_validate(record) for record in results],
            **pagination.model_dump(),
            total=total
        )


    # ─── Create operations ──────────────────────────────────
    async def create(self, data: SettingCreate) -> SettingResponse:
        """
        Create a new Setting

        Args:
            data: New Setting data
            
        Returns:
            SettingResponse if created successfully, None if Setting already exists
        """

        # Check if unique fields already exist
        setting_model = SettingModel(**data.model_dump())
        
        # Create
        result = await self.repo.create(setting_model)

        return SettingResponse.model_validate(result)

    # ─── Update operations ──────────────────────────────────
    async def update_by_id(self, id: int, updates: SettingUpdate) -> SettingResponse | None:
        """
        Update Setting information
        
        Args:
            id: id of Setting to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated SettingResponse if successful, None if Setting not found
        """    
        result = await self.repo.update_by_id(id, updates.model_dump(exclude_unset=True))
        return SettingResponse.model_validate(result) if result else None
    
    # ─── Delete operations ──────────────────────────────────
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a Setting
        
        Args:
            id: id of Setting to delete
            
        Returns:
            True if Setting was deleted, False if Setting not found
        """
        return await self.repo.delete_by_id(id)
