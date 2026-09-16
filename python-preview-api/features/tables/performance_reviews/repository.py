# ROSETIC:crud-guid



from typing import Any
from core.logging.repository_logger import log_repository_call
from core.db_exception_handler import handle_db_exceptions_async
from core.pagination import PaginationRequest, apply_filters, apply_pagination_filter
from features.tables.performance_reviews.models import PerformanceReviewModel
from features.tables.performance_reviews.schemas import PerformanceReviewFilter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

class PerformanceReviewRepository:
    """Repository layer for all PerformanceReview-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
    
    # ─── Create operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("PerformanceReview")
    async def create(self, performancereview_record: PerformanceReviewModel) -> PerformanceReviewModel | None:
        """
        Create a new PerformanceReview

        Args:
            data: New PerformanceReview data
            
        Returns:
            PerformanceReview data if created successfully, None if PerformanceReview already exists
        """
        
        # Create new PerformanceReview
        self.session.add(performancereview_record)
        await self.session.commit()
        await self.session.refresh(performancereview_record)

        return performancereview_record

    
    # ─── Read operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("PerformanceReview")
    async def get_by_id(self, id: int) -> PerformanceReviewModel | None:
        """
        Get performance_reviews by id
        
        Args:
            id: The id to search for
            
        Returns:
            PerformanceReview if found, None otherwise
        """
        stmt = select(PerformanceReviewModel).where(PerformanceReviewModel.review_id == id)
        result = await self.session.execute(stmt)
        return result.unique().scalars().first()

    @handle_db_exceptions_async
    @log_repository_call("PerformanceReview")
    async def get_all(self, pagination: PaginationRequest) -> tuple[list[PerformanceReviewModel], int]:
        """
        Get all performance_reviews
        
        Returns:
            List of all performance_reviews
        """
        stmt = select(PerformanceReviewModel)

        total = await self.session.scalar(select(func.count(PerformanceReviewModel.review_id)))
        stmt = apply_pagination_filter(stmt, pagination, PerformanceReviewModel)

        result = await self.session.execute(stmt)
        records = result.unique().scalars().all()
        return records, total
    
    @handle_db_exceptions_async
    @log_repository_call("PerformanceReview")
    async def search(self, filters: PerformanceReviewFilter, pagination: PaginationRequest) -> tuple[list[PerformanceReviewModel], int]:
        stmt = select(PerformanceReviewModel)
        stmt = apply_filters(stmt, filters, PerformanceReviewModel)

        total = await self.session.scalar(select(func.count()).select_from(stmt.subquery()))
        stmt = apply_pagination_filter(stmt, pagination, PerformanceReviewModel)

        results = await self.session.execute(stmt)
        records = results.unique().scalars().all()
        return records, total


    # ─── Update operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("PerformanceReview")
    async def update_by_id(self, id: int, updates: dict[str, Any]) -> PerformanceReviewModel | None:
        """
        Update PerformanceReview information
        
        Args:
            id: id of PerformanceReview to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated PerformanceReview if successful, None if PerformanceReview not found
        """
        stmt = select(PerformanceReviewModel).where(PerformanceReviewModel.review_id == id)
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
    @log_repository_call("PerformanceReview")
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a PerformanceReview
        
        Args:
            id: id of PerformanceReview to delete
            
        Returns:
            True if user was deleted, False if user not found
        """
        stmt = select(PerformanceReviewModel).where(PerformanceReviewModel.review_id == id)
        result = await self.session.execute(stmt)
        record = result.unique().scalars().first()
        if record:
            await self.session.delete(record)
            await self.session.commit()
            return True
        return False
