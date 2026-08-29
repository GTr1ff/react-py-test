# ROSETIC:crud-guid



from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, Depends, Query, status
from core.pagination import PaginatedResponse, PaginationRequest
from features.tables.employee_projects.service import EmployeeProjectService
from features.tables.employee_projects.schemas import EmployeeProjectResponse, EmployeeProjectCreate, EmployeeProjectUpdate, EmployeeProjectFilter

from core.database import get_db

router = APIRouter(prefix="/employee-projects", tags=["employee-projects"])

SessionDep = Annotated[AsyncSession, Depends(get_db)]
PaginationDep = Annotated[PaginationRequest, Query()]

NOT_FOUND = "EmployeeProject not found"
NO_FIELDS_TO_UPDATE = "No fields to update"

# ─── Create operations ──────────────────────────────────
@router.post("", response_model=EmployeeProjectResponse, status_code=status.HTTP_201_CREATED)
async def create(payload: EmployeeProjectCreate, session: SessionDep):
    """Create a new employee_projects"""
    result = await EmployeeProjectService(session=session).create(payload)

    return result

# ─── Read operations ──────────────────────────────────
@router.get("/{id}", response_model=EmployeeProjectResponse, responses={404: {"description": NOT_FOUND}})
async def get_by_id(id: int, session: SessionDep):
    """Get EmployeeProject by id
    
    Args:
        id: The id to search for
    """
    record = await EmployeeProjectService(session=session).get_by_id(id)

    if not record:
        raise HTTPException(status_code=404, detail=NOT_FOUND)

    return record

@router.get("", response_model=PaginatedResponse[EmployeeProjectResponse])
async def get_all(pagination: PaginationDep, session: SessionDep):
    """Get all employee_projects"""
    records = await EmployeeProjectService(session=session).get_all(pagination)
    return records

@router.post("/search", response_model=PaginatedResponse[EmployeeProjectResponse])
async def search(filters: EmployeeProjectFilter, pagination: PaginationDep, session: SessionDep):
    """Search EmployeeProject by filters"""
    records = await EmployeeProjectService(session=session).search(filters, pagination)
    return records

# ─── Update operations ──────────────────────────────────
@router.put("/{id}", 
        response_model=EmployeeProjectResponse, 
        responses={
            400: {"description": NO_FIELDS_TO_UPDATE},
            404: {"description": NOT_FOUND},
        },
    )
async def update_by_id(id: int, payload: EmployeeProjectUpdate, session: SessionDep):
    """Update EmployeeProject information
    
    Args:
        id: The id to update
    """
    if not payload.model_fields_set:
        raise HTTPException(status_code=400, detail=NO_FIELDS_TO_UPDATE)
    
    updated_record = await EmployeeProjectService(session=session).update_by_id(id, payload)
    if not updated_record:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    return updated_record

# ─── Delete operations ──────────────────────────────────
@router.delete("/{id}", responses={404: {"description": NOT_FOUND}})
async def delete_by_id(id: int, session: SessionDep):
    """Delete a EmployeeProject
    
    Args:
        id: The id to delete
    """
    success = await EmployeeProjectService(session=session).delete_by_id(id)
    if not success:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    return {"message": "EmployeeProject deleted successfully"}
