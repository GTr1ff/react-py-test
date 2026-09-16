# ROSETIC:crud-guid



from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, Depends, Query, status
from core.pagination import PaginatedResponse, PaginationRequest
from features.tables.memos.service import MemoService
from features.tables.memos.schemas import MemoResponse, MemoCreate, MemoUpdate, MemoFilter

from core.database import get_db

router = APIRouter(prefix="/memos", tags=["memos"])

SessionDep = Annotated[AsyncSession, Depends(get_db)]
PaginationDep = Annotated[PaginationRequest, Query()]

NOT_FOUND = "Memo not found"
NO_FIELDS_TO_UPDATE = "No fields to update"

# ─── Create operations ──────────────────────────────────
@router.post("", response_model=MemoResponse, status_code=status.HTTP_201_CREATED)
async def create(payload: MemoCreate, session: SessionDep):
    """Create a new memos"""
    result = await MemoService(session=session).create(payload)

    return result

# ─── Read operations ──────────────────────────────────
@router.get("/{id}", response_model=MemoResponse, responses={404: {"description": NOT_FOUND}})
async def get_by_id(id: int, session: SessionDep):
    """Get Memo by id
    
    Args:
        id: The id to search for
    """
    record = await MemoService(session=session).get_by_id(id)

    if not record:
        raise HTTPException(status_code=404, detail=NOT_FOUND)

    return record

@router.get("", response_model=PaginatedResponse[MemoResponse])
async def get_all(pagination: PaginationDep, session: SessionDep):
    """Get all memos"""
    records = await MemoService(session=session).get_all(pagination)
    return records

@router.post("/search", response_model=PaginatedResponse[MemoResponse])
async def search(filters: MemoFilter, pagination: PaginationDep, session: SessionDep):
    """Search Memo by filters"""
    records = await MemoService(session=session).search(filters, pagination)
    return records

# ─── Update operations ──────────────────────────────────
@router.put("/{id}", 
        response_model=MemoResponse, 
        responses={
            400: {"description": NO_FIELDS_TO_UPDATE},
            404: {"description": NOT_FOUND},
        },
    )
async def update_by_id(id: int, payload: MemoUpdate, session: SessionDep):
    """Update Memo information
    
    Args:
        id: The id to update
    """
    if not payload.model_fields_set:
        raise HTTPException(status_code=400, detail=NO_FIELDS_TO_UPDATE)
    
    updated_record = await MemoService(session=session).update_by_id(id, payload)
    if not updated_record:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    return updated_record

# ─── Delete operations ──────────────────────────────────
@router.delete("/{id}", responses={404: {"description": NOT_FOUND}})
async def delete_by_id(id: int, session: SessionDep):
    """Delete a Memo
    
    Args:
        id: The id to delete
    """
    success = await MemoService(session=session).delete_by_id(id)
    if not success:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    return {"message": "Memo deleted successfully"}
