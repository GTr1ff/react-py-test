# ROSETIC:crud-guid



from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, Depends, Query, status
from core.pagination import PaginatedResponse, PaginationRequest
from features.tables.tasks.service import TaskService
from features.tables.tasks.schemas import TaskResponse, TaskCreate, TaskUpdate, TaskFilter

from core.database import get_db

router = APIRouter(prefix="/tasks", tags=["tasks"])

SessionDep = Annotated[AsyncSession, Depends(get_db)]
PaginationDep = Annotated[PaginationRequest, Query()]

NOT_FOUND = "Task not found"
NO_FIELDS_TO_UPDATE = "No fields to update"

# ─── Create operations ──────────────────────────────────
@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create(payload: TaskCreate, session: SessionDep):
    """Create a new tasks"""
    result = await TaskService(session=session).create(payload)

    return result

# ─── Read operations ──────────────────────────────────
@router.get("/{id}", response_model=TaskResponse, responses={404: {"description": NOT_FOUND}})
async def get_by_id(id: int, session: SessionDep):
    """Get Task by id
    
    Args:
        id: The id to search for
    """
    record = await TaskService(session=session).get_by_id(id)

    if not record:
        raise HTTPException(status_code=404, detail=NOT_FOUND)

    return record

@router.get("", response_model=PaginatedResponse[TaskResponse])
async def get_all(pagination: PaginationDep, session: SessionDep):
    """Get all tasks"""
    records = await TaskService(session=session).get_all(pagination)
    return records

@router.post("/search", response_model=PaginatedResponse[TaskResponse])
async def search(filters: TaskFilter, pagination: PaginationDep, session: SessionDep):
    """Search Task by filters"""
    records = await TaskService(session=session).search(filters, pagination)
    return records

# ─── Update operations ──────────────────────────────────
@router.put("/{id}", 
        response_model=TaskResponse, 
        responses={
            400: {"description": NO_FIELDS_TO_UPDATE},
            404: {"description": NOT_FOUND},
        },
    )
async def update_by_id(id: int, payload: TaskUpdate, session: SessionDep):
    """Update Task information
    
    Args:
        id: The id to update
    """
    if not payload.model_fields_set:
        raise HTTPException(status_code=400, detail=NO_FIELDS_TO_UPDATE)
    
    updated_record = await TaskService(session=session).update_by_id(id, payload)
    if not updated_record:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    return updated_record

# ─── Delete operations ──────────────────────────────────
@router.delete("/{id}", responses={404: {"description": NOT_FOUND}})
async def delete_by_id(id: int, session: SessionDep):
    """Delete a Task
    
    Args:
        id: The id to delete
    """
    success = await TaskService(session=session).delete_by_id(id)
    if not success:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    return {"message": "Task deleted successfully"}
