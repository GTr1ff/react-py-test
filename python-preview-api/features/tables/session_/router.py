# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c



from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, Depends, Query, status
from core.pagination import PaginatedResponse, PaginationRequest
from features.tables.session_.service import SessionService
from features.tables.session_.schemas import SessionResponse, SessionCreate, SessionUpdate, SessionFilter

from core.database import get_db

router = APIRouter(prefix="/session", tags=["session"])

SessionDep = Annotated[AsyncSession, Depends(get_db)]
PaginationDep = Annotated[PaginationRequest, Query()]

NOT_FOUND = "Session not found"
NO_FIELDS_TO_UPDATE = "No fields to update"

# ─── Create operations ──────────────────────────────────
@router.post("", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def create(payload: SessionCreate, session: SessionDep):
    """Create a new session"""
    result = await SessionService(session=session).create(payload)

    return result

# ─── Read operations ──────────────────────────────────
@router.get("/{id}", response_model=SessionResponse, responses={404: {"description": NOT_FOUND}})
async def get_by_id(id: int, session: SessionDep):
    """Get Session by id
    
    Args:
        id: The id to search for
    """
    record = await SessionService(session=session).get_by_id(id)

    if not record:
        raise HTTPException(status_code=404, detail=NOT_FOUND)

    return record

@router.get("", response_model=PaginatedResponse[SessionResponse])
async def get_all(pagination: PaginationDep, session: SessionDep):
    """Get all session"""
    records = await SessionService(session=session).get_all(pagination)
    return records

@router.post("/search", response_model=PaginatedResponse[SessionResponse])
async def search(filters: SessionFilter, pagination: PaginationDep, session: SessionDep):
    """Search Session by filters"""
    records = await SessionService(session=session).search(filters, pagination)
    return records

# ─── Update operations ──────────────────────────────────
@router.put("/{id}", 
        response_model=SessionResponse, 
        responses={
            400: {"description": NO_FIELDS_TO_UPDATE},
            404: {"description": NOT_FOUND},
        },
    )
async def update_by_id(id: int, payload: SessionUpdate, session: SessionDep):
    """Update Session information
    
    Args:
        id: The id to update
    """
    if not payload.model_fields_set:
        raise HTTPException(status_code=400, detail=NO_FIELDS_TO_UPDATE)
    
    updated_record = await SessionService(session=session).update_by_id(id, payload)
    if not updated_record:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    return updated_record

# ─── Delete operations ──────────────────────────────────
@router.delete("/{id}", responses={404: {"description": NOT_FOUND}})
async def delete_by_id(id: int, session: SessionDep):
    """Delete a Session
    
    Args:
        id: The id to delete
    """
    success = await SessionService(session=session).delete_by_id(id)
    if not success:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    return {"message": "Session deleted successfully"}
