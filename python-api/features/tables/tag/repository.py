# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c



from typing import Any
from core.logging.repository_logger import log_repository_call
from core.db_exception_handler import handle_db_exceptions_async
from core.pagination import PaginationRequest, apply_filters, apply_pagination_filter
from features.tables.tag.models import TagModel
from features.tables.tag.schemas import TagFilter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

class TagRepository:
    """Repository layer for all Tag-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
    
    # ─── Create operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Tag")
    async def create(self, tag_record: TagModel) -> TagModel | None:
        """
        Create a new Tag

        Args:
            data: New Tag data
            
        Returns:
            Tag data if created successfully, None if Tag already exists
        """
        
        # Create new Tag
        self.session.add(tag_record)
        await self.session.commit()
        await self.session.refresh(tag_record)

        return tag_record

    
    # ─── Read operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Tag")
    async def get_by_id(self, id: int) -> TagModel | None:
        """
        Get tag by id
        
        Args:
            id: The id to search for
            
        Returns:
            Tag if found, None otherwise
        """
        stmt = select(TagModel).where(TagModel.id == id)
        result = await self.session.execute(stmt)
        return result.unique().scalars().first()

    @handle_db_exceptions_async
    @log_repository_call("Tag")
    async def get_all(self, pagination: PaginationRequest) -> tuple[list[TagModel], int]:
        """
        Get all tag
        
        Returns:
            List of all tag
        """
        stmt = select(TagModel)

        total = await self.session.scalar(select(func.count(TagModel.id)))
        stmt = apply_pagination_filter(stmt, pagination, TagModel)

        result = await self.session.execute(stmt)
        records = result.unique().scalars().all()
        return records, total
    
    @handle_db_exceptions_async
    @log_repository_call("Tag")
    async def search(self, filters: TagFilter, pagination: PaginationRequest) -> tuple[list[TagModel], int]:
        stmt = select(TagModel)
        stmt = apply_filters(stmt, filters, TagModel)

        total = await self.session.scalar(select(func.count()).select_from(stmt.subquery()))
        stmt = apply_pagination_filter(stmt, pagination, TagModel)

        results = await self.session.execute(stmt)
        records = results.unique().scalars().all()
        return records, total


    # ─── Update operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Tag")
    async def update_by_id(self, id: int, updates: dict[str, Any]) -> TagModel | None:
        """
        Update Tag information
        
        Args:
            id: id of Tag to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated Tag if successful, None if Tag not found
        """
        stmt = select(TagModel).where(TagModel.id == id)
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
    @log_repository_call("Tag")
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a Tag
        
        Args:
            id: id of Tag to delete
            
        Returns:
            True if user was deleted, False if user not found
        """
        stmt = select(TagModel).where(TagModel.id == id)
        result = await self.session.execute(stmt)
        record = result.unique().scalars().first()
        if record:
            await self.session.delete(record)
            await self.session.commit()
            return True
        return False
