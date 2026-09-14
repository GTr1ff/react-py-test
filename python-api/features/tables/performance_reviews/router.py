# ROSETIC:crud-guid



from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, Depends, Query, status
from core.pagination import PaginatedResponse, PaginationRequest
from features.tables.performance_reviews.service import PerformanceReviewService
from features.tables.performance_reviews.schemas import PerformanceReviewResponse, PerformanceReviewCreate, PerformanceReviewUpdate, PerformanceReviewFilter

from core.database import get_db

router = APIRouter(prefix="/performance-reviews", tags=["performance-reviews"])

SessionDep = Annotated[AsyncSession, Depends(get_db)]
PaginationDep = Annotated[PaginationRequest, Query()]

NOT_FOUND = "PerformanceReview not found"
NO_FIELDS_TO_UPDATE = "No fields to update"

# ─── Create operations ──────────────────────────────────
@router.post("", response_model=PerformanceReviewResponse, status_code=status.HTTP_201_CREATED)
async def create(payload: PerformanceReviewCreate, session: SessionDep):
    """Create a new performance_reviews"""
    result = await PerformanceReviewService(session=session).create(payload)

    return result

# ─── Read operations ──────────────────────────────────
@router.get("/{id}", response_model=PerformanceReviewResponse, responses={404: {"description": NOT_FOUND}})
async def get_by_id(id: int, session: SessionDep):
    """Get PerformanceReview by id
    
    Args:
        id: The id to search for
    """
    record = await PerformanceReviewService(session=session).get_by_id(id)

    if not record:
        raise HTTPException(status_code=404, detail=NOT_FOUND)

    return record

@router.get("", response_model=PaginatedResponse[PerformanceReviewResponse])
async def get_all(pagination: PaginationDep, session: SessionDep):
    """Get all performance_reviews"""
    records = await PerformanceReviewService(session=session).get_all(pagination)
    return records

@router.post("/search", response_model=PaginatedResponse[PerformanceReviewResponse])
async def search(filters: PerformanceReviewFilter, pagination: PaginationDep, session: SessionDep):
    """Search PerformanceReview by filters"""
    records = await PerformanceReviewService(session=session).search(filters, pagination)
    return records

# ─── Update operations ──────────────────────────────────
@router.put("/{id}", 
        response_model=PerformanceReviewResponse, 
        responses={
            400: {"description": NO_FIELDS_TO_UPDATE},
            404: {"description": NOT_FOUND},
        },
    )
async def update_by_id(id: int, payload: PerformanceReviewUpdate, session: SessionDep):
    """Update PerformanceReview information
    
    Args:
        id: The id to update
    """
    if not payload.model_fields_set:
        raise HTTPException(status_code=400, detail=NO_FIELDS_TO_UPDATE)
    
    updated_record = await PerformanceReviewService(session=session).update_by_id(id, payload)
    if not updated_record:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    return updated_record

# ─── Delete operations ──────────────────────────────────
@router.delete("/{id}", responses={404: {"description": NOT_FOUND}})
async def delete_by_id(id: int, session: SessionDep):
    """Delete a PerformanceReview
    
    Args:
        id: The id to delete
    """
    success = await PerformanceReviewService(session=session).delete_by_id(id)
    if not success:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    return {"message": "PerformanceReview deleted successfully"}
