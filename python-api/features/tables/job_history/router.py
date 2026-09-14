# ROSETIC:crud-guid



from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, Depends, Query, status
from core.pagination import PaginatedResponse, PaginationRequest
from features.tables.job_history.service import JobHistoryService
from features.tables.job_history.schemas import JobHistoryResponse, JobHistoryCreate, JobHistoryUpdate, JobHistoryFilter

from core.database import get_db

router = APIRouter(prefix="/job-history", tags=["job-history"])

SessionDep = Annotated[AsyncSession, Depends(get_db)]
PaginationDep = Annotated[PaginationRequest, Query()]

NOT_FOUND = "JobHistory not found"
NO_FIELDS_TO_UPDATE = "No fields to update"

# ─── Create operations ──────────────────────────────────
@router.post("", response_model=JobHistoryResponse, status_code=status.HTTP_201_CREATED)
async def create(payload: JobHistoryCreate, session: SessionDep):
    """Create a new job_history"""
    result = await JobHistoryService(session=session).create(payload)

    return result

# ─── Read operations ──────────────────────────────────
@router.get("/{id}", response_model=JobHistoryResponse, responses={404: {"description": NOT_FOUND}})
async def get_by_id(id: int, session: SessionDep):
    """Get JobHistory by id
    
    Args:
        id: The id to search for
    """
    record = await JobHistoryService(session=session).get_by_id(id)

    if not record:
        raise HTTPException(status_code=404, detail=NOT_FOUND)

    return record

@router.get("", response_model=PaginatedResponse[JobHistoryResponse])
async def get_all(pagination: PaginationDep, session: SessionDep):
    """Get all job_history"""
    records = await JobHistoryService(session=session).get_all(pagination)
    return records

@router.post("/search", response_model=PaginatedResponse[JobHistoryResponse])
async def search(filters: JobHistoryFilter, pagination: PaginationDep, session: SessionDep):
    """Search JobHistory by filters"""
    records = await JobHistoryService(session=session).search(filters, pagination)
    return records

# ─── Update operations ──────────────────────────────────
@router.put("/{id}", 
        response_model=JobHistoryResponse, 
        responses={
            400: {"description": NO_FIELDS_TO_UPDATE},
            404: {"description": NOT_FOUND},
        },
    )
async def update_by_id(id: int, payload: JobHistoryUpdate, session: SessionDep):
    """Update JobHistory information
    
    Args:
        id: The id to update
    """
    if not payload.model_fields_set:
        raise HTTPException(status_code=400, detail=NO_FIELDS_TO_UPDATE)
    
    updated_record = await JobHistoryService(session=session).update_by_id(id, payload)
    if not updated_record:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    return updated_record

# ─── Delete operations ──────────────────────────────────
@router.delete("/{id}", responses={404: {"description": NOT_FOUND}})
async def delete_by_id(id: int, session: SessionDep):
    """Delete a JobHistory
    
    Args:
        id: The id to delete
    """
    success = await JobHistoryService(session=session).delete_by_id(id)
    if not success:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    return {"message": "JobHistory deleted successfully"}
