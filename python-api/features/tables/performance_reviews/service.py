# ROSETIC:crud-guid



from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from core.pagination import PaginatedResponse, PaginationRequest
from features.tables.performance_reviews.models import PerformanceReviewModel
from features.tables.performance_reviews.schemas import PerformanceReviewResponse, PerformanceReviewCreate, PerformanceReviewUpdate, PerformanceReviewFilter
from features.tables.performance_reviews.repository import PerformanceReviewRepository

class PerformanceReviewService:
    """Service layer for all PerformanceReview-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = PerformanceReviewRepository(session)

    
    # ─── Read operations ──────────────────────────────────id
    async def get_by_id(self, id: int) -> PerformanceReviewResponse | None:
        """
        Get performance_reviews by id
        
        Args:
            id: The id to search for
            
        Returns:
            PerformanceReviewResponse if found, None if not found
        """
        result = await self.repo.get_by_id(id)
        return PerformanceReviewResponse.model_validate(result) if result else None

    async def get_all(self, pagination: PaginationRequest) -> PaginatedResponse[PerformanceReviewResponse]:
        """
        Get all performance_reviews
        
        Returns:
            List of all performance_reviews
        """
        result, total = await self.repo.get_all(pagination)

        return PaginatedResponse[PerformanceReviewResponse](
            items=[PerformanceReviewResponse.model_validate(record) for record in result],
            **pagination.model_dump(),
            total=total
        )

    async def search(self, filters: PerformanceReviewFilter, pagination: PaginationRequest) -> PaginatedResponse[PerformanceReviewResponse]:
        results, total = await self.repo.search(filters, pagination)
        return PaginatedResponse[PerformanceReviewResponse](
            items=[PerformanceReviewResponse.model_validate(record) for record in results],
            **pagination.model_dump(),
            total=total
        )


    # ─── Create operations ──────────────────────────────────
    async def create(self, data: PerformanceReviewCreate) -> PerformanceReviewResponse:
        """
        Create a new PerformanceReview

        Args:
            data: New PerformanceReview data
            
        Returns:
            PerformanceReviewResponse if created successfully, None if PerformanceReview already exists
        """

        # Check if unique fields already exist
        performancereview_model = PerformanceReviewModel(**data.model_dump())
        
        # Create
        result = await self.repo.create(performancereview_model)

        return PerformanceReviewResponse.model_validate(result)

    # ─── Update operations ──────────────────────────────────
    async def update_by_id(self, id: int, updates: PerformanceReviewUpdate) -> PerformanceReviewResponse | None:
        """
        Update PerformanceReview information
        
        Args:
            id: id of PerformanceReview to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated PerformanceReviewResponse if successful, None if PerformanceReview not found
        """    
        result = await self.repo.update_by_id(id, updates.model_dump(exclude_unset=True))
        return PerformanceReviewResponse.model_validate(result) if result else None
    
    # ─── Delete operations ──────────────────────────────────
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a PerformanceReview
        
        Args:
            id: id of PerformanceReview to delete
            
        Returns:
            True if PerformanceReview was deleted, False if PerformanceReview not found
        """
        return await self.repo.delete_by_id(id)
