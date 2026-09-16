# ROSETIC:crud-guid



from typing import Any
from core.logging.repository_logger import log_repository_call
from core.db_exception_handler import handle_db_exceptions_async
from core.pagination import PaginationRequest, apply_filters, apply_pagination_filter
from features.tables.locations.models import LocationModel
from features.tables.locations.schemas import LocationFilter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

class LocationRepository:
    """Repository layer for all Location-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
    
    # ─── Create operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Location")
    async def create(self, location_record: LocationModel) -> LocationModel | None:
        """
        Create a new Location

        Args:
            data: New Location data
            
        Returns:
            Location data if created successfully, None if Location already exists
        """
        
        # Create new Location
        self.session.add(location_record)
        await self.session.commit()
        await self.session.refresh(location_record)

        return location_record

    
    # ─── Read operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Location")
    async def get_by_id(self, id: int) -> LocationModel | None:
        """
        Get locations by id
        
        Args:
            id: The id to search for
            
        Returns:
            Location if found, None otherwise
        """
        stmt = select(LocationModel).where(LocationModel.location_id == id)
        result = await self.session.execute(stmt)
        return result.unique().scalars().first()

    @handle_db_exceptions_async
    @log_repository_call("Location")
    async def get_all(self, pagination: PaginationRequest) -> tuple[list[LocationModel], int]:
        """
        Get all locations
        
        Returns:
            List of all locations
        """
        stmt = select(LocationModel)

        total = await self.session.scalar(select(func.count(LocationModel.location_id)))
        stmt = apply_pagination_filter(stmt, pagination, LocationModel)

        result = await self.session.execute(stmt)
        records = result.unique().scalars().all()
        return records, total
    
    @handle_db_exceptions_async
    @log_repository_call("Location")
    async def search(self, filters: LocationFilter, pagination: PaginationRequest) -> tuple[list[LocationModel], int]:
        stmt = select(LocationModel)
        stmt = apply_filters(stmt, filters, LocationModel)

        total = await self.session.scalar(select(func.count()).select_from(stmt.subquery()))
        stmt = apply_pagination_filter(stmt, pagination, LocationModel)

        results = await self.session.execute(stmt)
        records = results.unique().scalars().all()
        return records, total


    # ─── Update operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Location")
    async def update_by_id(self, id: int, updates: dict[str, Any]) -> LocationModel | None:
        """
        Update Location information
        
        Args:
            id: id of Location to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated Location if successful, None if Location not found
        """
        stmt = select(LocationModel).where(LocationModel.location_id == id)
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
    @log_repository_call("Location")
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a Location
        
        Args:
            id: id of Location to delete
            
        Returns:
            True if user was deleted, False if user not found
        """
        stmt = select(LocationModel).where(LocationModel.location_id == id)
        result = await self.session.execute(stmt)
        record = result.unique().scalars().first()
        if record:
            await self.session.delete(record)
            await self.session.commit()
            return True
        return False
