# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c



from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, Depends, Query, status
from core.pagination import PaginatedResponse, PaginationRequest
from features.tables.event_log.service import EventLogService
from features.tables.event_log.schemas import EventLogResponse, EventLogCreate, EventLogUpdate, EventLogFilter

from core.database import get_db

router = APIRouter(prefix="/event-log", tags=["event-log"])

SessionDep = Annotated[AsyncSession, Depends(get_db)]
PaginationDep = Annotated[PaginationRequest, Query()]

NOT_FOUND = "EventLog not found"
NO_FIELDS_TO_UPDATE = "No fields to update"

# ─── Create operations ──────────────────────────────────
@router.post("", response_model=EventLogResponse, status_code=status.HTTP_201_CREATED)
async def create(payload: EventLogCreate, session: SessionDep):
    """Create a new event_log"""
    result = await EventLogService(session=session).create(payload)

    return result

# ─── Read operations ──────────────────────────────────
@router.get("/{id}", response_model=EventLogResponse, responses={404: {"description": NOT_FOUND}})
async def get_by_id(id: int, session: SessionDep):
    """Get EventLog by id
    
    Args:
        id: The id to search for
    """
    record = await EventLogService(session=session).get_by_id(id)

    if not record:
        raise HTTPException(status_code=404, detail=NOT_FOUND)

    return record

@router.get("", response_model=PaginatedResponse[EventLogResponse])
async def get_all(pagination: PaginationDep, session: SessionDep):
    """Get all event_log"""
    records = await EventLogService(session=session).get_all(pagination)
    return records

@router.post("/search", response_model=PaginatedResponse[EventLogResponse])
async def search(filters: EventLogFilter, pagination: PaginationDep, session: SessionDep):
    """Search EventLog by filters"""
    records = await EventLogService(session=session).search(filters, pagination)
    return records

# ─── Update operations ──────────────────────────────────
@router.put("/{id}", 
        response_model=EventLogResponse, 
        responses={
            400: {"description": NO_FIELDS_TO_UPDATE},
            404: {"description": NOT_FOUND},
        },
    )
async def update_by_id(id: int, payload: EventLogUpdate, session: SessionDep):
    """Update EventLog information
    
    Args:
        id: The id to update
    """
    if not payload.model_fields_set:
        raise HTTPException(status_code=400, detail=NO_FIELDS_TO_UPDATE)
    
    updated_record = await EventLogService(session=session).update_by_id(id, payload)
    if not updated_record:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    return updated_record

# ─── Delete operations ──────────────────────────────────
@router.delete("/{id}", responses={404: {"description": NOT_FOUND}})
async def delete_by_id(id: int, session: SessionDep):
    """Delete a EventLog
    
    Args:
        id: The id to delete
    """
    success = await EventLogService(session=session).delete_by_id(id)
    if not success:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    return {"message": "EventLog deleted successfully"}
