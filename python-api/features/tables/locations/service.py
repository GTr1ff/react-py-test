# ROSETIC:crud-guid



from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from core.pagination import PaginatedResponse, PaginationRequest
from features.tables.locations.models import LocationModel
from features.tables.locations.schemas import LocationResponse, LocationCreate, LocationUpdate, LocationFilter
from features.tables.locations.repository import LocationRepository

class LocationService:
    """Service layer for all Location-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = LocationRepository(session)

    
    # ─── Read operations ──────────────────────────────────id
    async def get_by_id(self, id: int) -> LocationResponse | None:
        """
        Get locations by id
        
        Args:
            id: The id to search for
            
        Returns:
            LocationResponse if found, None if not found
        """
        result = await self.repo.get_by_id(id)
        return LocationResponse.model_validate(result) if result else None

    async def get_all(self, pagination: PaginationRequest) -> PaginatedResponse[LocationResponse]:
        """
        Get all locations
        
        Returns:
            List of all locations
        """
        result, total = await self.repo.get_all(pagination)

        return PaginatedResponse[LocationResponse](
            items=[LocationResponse.model_validate(record) for record in result],
            **pagination.model_dump(),
            total=total
        )

    async def search(self, filters: LocationFilter, pagination: PaginationRequest) -> PaginatedResponse[LocationResponse]:
        results, total = await self.repo.search(filters, pagination)
        return PaginatedResponse[LocationResponse](
            items=[LocationResponse.model_validate(record) for record in results],
            **pagination.model_dump(),
            total=total
        )


    # ─── Create operations ──────────────────────────────────
    async def create(self, data: LocationCreate) -> LocationResponse:
        """
        Create a new Location

        Args:
            data: New Location data
            
        Returns:
            LocationResponse if created successfully, None if Location already exists
        """

        # Check if unique fields already exist
        location_model = LocationModel(**data.model_dump())
        
        # Create
        result = await self.repo.create(location_model)

        return LocationResponse.model_validate(result)

    # ─── Update operations ──────────────────────────────────
    async def update_by_id(self, id: int, updates: LocationUpdate) -> LocationResponse | None:
        """
        Update Location information
        
        Args:
            id: id of Location to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated LocationResponse if successful, None if Location not found
        """    
        result = await self.repo.update_by_id(id, updates.model_dump(exclude_unset=True))
        return LocationResponse.model_validate(result) if result else None
    
    # ─── Delete operations ──────────────────────────────────
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a Location
        
        Args:
            id: id of Location to delete
            
        Returns:
            True if Location was deleted, False if Location not found
        """
        return await self.repo.delete_by_id(id)
