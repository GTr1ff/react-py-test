# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c



from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, Depends, Query, status
from core.pagination import PaginatedResponse, PaginationRequest
from features.tables.notification.service import NotificationService
from features.tables.notification.schemas import NotificationResponse, NotificationCreate, NotificationUpdate, NotificationFilter

from core.database import get_db

router = APIRouter(prefix="/notification", tags=["notification"])

SessionDep = Annotated[AsyncSession, Depends(get_db)]
PaginationDep = Annotated[PaginationRequest, Query()]

NOT_FOUND = "Notification not found"
NO_FIELDS_TO_UPDATE = "No fields to update"

# ─── Create operations ──────────────────────────────────
@router.post("", response_model=NotificationResponse, status_code=status.HTTP_201_CREATED)
async def create(payload: NotificationCreate, session: SessionDep):
    """Create a new notification"""
    result = await NotificationService(session=session).create(payload)

    return result

# ─── Read operations ──────────────────────────────────
@router.get("/{id}", response_model=NotificationResponse, responses={404: {"description": NOT_FOUND}})
async def get_by_id(id: int, session: SessionDep):
    """Get Notification by id
    
    Args:
        id: The id to search for
    """
    record = await NotificationService(session=session).get_by_id(id)

    if not record:
        raise HTTPException(status_code=404, detail=NOT_FOUND)

    return record

@router.get("", response_model=PaginatedResponse[NotificationResponse])
async def get_all(pagination: PaginationDep, session: SessionDep):
    """Get all notification"""
    records = await NotificationService(session=session).get_all(pagination)
    return records

@router.post("/search", response_model=PaginatedResponse[NotificationResponse])
async def search(filters: NotificationFilter, pagination: PaginationDep, session: SessionDep):
    """Search Notification by filters"""
    records = await NotificationService(session=session).search(filters, pagination)
    return records

# ─── Update operations ──────────────────────────────────
@router.put("/{id}", 
        response_model=NotificationResponse, 
        responses={
            400: {"description": NO_FIELDS_TO_UPDATE},
            404: {"description": NOT_FOUND},
        },
    )
async def update_by_id(id: int, payload: NotificationUpdate, session: SessionDep):
    """Update Notification information
    
    Args:
        id: The id to update
    """
    if not payload.model_fields_set:
        raise HTTPException(status_code=400, detail=NO_FIELDS_TO_UPDATE)
    
    updated_record = await NotificationService(session=session).update_by_id(id, payload)
    if not updated_record:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    return updated_record

# ─── Delete operations ──────────────────────────────────
@router.delete("/{id}", responses={404: {"description": NOT_FOUND}})
async def delete_by_id(id: int, session: SessionDep):
    """Delete a Notification
    
    Args:
        id: The id to delete
    """
    success = await NotificationService(session=session).delete_by_id(id)
    if not success:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    return {"message": "Notification deleted successfully"}
