# ROSETIC:crud-guid



from typing import Any
from core.logging.repository_logger import log_repository_call
from core.db_exception_handler import handle_db_exceptions_async
from core.pagination import PaginationRequest, apply_filters, apply_pagination_filter
from features.tables.roles.models import RoleModel
from features.tables.roles.schemas import RoleFilter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

class RoleRepository:
    """Repository layer for all Role-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
    
    # ─── Create operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Role")
    async def create(self, role_record: RoleModel) -> RoleModel | None:
        """
        Create a new Role

        Args:
            data: New Role data
            
        Returns:
            Role data if created successfully, None if Role already exists
        """
        
        # Create new Role
        self.session.add(role_record)
        await self.session.commit()
        await self.session.refresh(role_record)

        return role_record

    
    # ─── Read operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Role")
    async def get_by_id(self, id: int) -> RoleModel | None:
        """
        Get roles by id
        
        Args:
            id: The id to search for
            
        Returns:
            Role if found, None otherwise
        """
        stmt = select(RoleModel).where(RoleModel.role_id == id)
        result = await self.session.execute(stmt)
        return result.unique().scalars().first()

    @handle_db_exceptions_async
    @log_repository_call("Role")
    async def get_all(self, pagination: PaginationRequest) -> tuple[list[RoleModel], int]:
        """
        Get all roles
        
        Returns:
            List of all roles
        """
        stmt = select(RoleModel)

        total = await self.session.scalar(select(func.count(RoleModel.role_id)))
        stmt = apply_pagination_filter(stmt, pagination, RoleModel)

        result = await self.session.execute(stmt)
        records = result.unique().scalars().all()
        return records, total
    
    @handle_db_exceptions_async
    @log_repository_call("Role")
    async def search(self, filters: RoleFilter, pagination: PaginationRequest) -> tuple[list[RoleModel], int]:
        stmt = select(RoleModel)
        stmt = apply_filters(stmt, filters, RoleModel)

        total = await self.session.scalar(select(func.count()).select_from(stmt.subquery()))
        stmt = apply_pagination_filter(stmt, pagination, RoleModel)

        results = await self.session.execute(stmt)
        records = results.unique().scalars().all()
        return records, total


    # ─── Update operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Role")
    async def update_by_id(self, id: int, updates: dict[str, Any]) -> RoleModel | None:
        """
        Update Role information
        
        Args:
            id: id of Role to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated Role if successful, None if Role not found
        """
        stmt = select(RoleModel).where(RoleModel.role_id == id)
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
    @log_repository_call("Role")
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a Role
        
        Args:
            id: id of Role to delete
            
        Returns:
            True if user was deleted, False if user not found
        """
        stmt = select(RoleModel).where(RoleModel.role_id == id)
        result = await self.session.execute(stmt)
        record = result.unique().scalars().first()
        if record:
            await self.session.delete(record)
            await self.session.commit()
            return True
        return False
