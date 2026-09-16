# ROSETIC:crud-guid



from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, Depends, Query, status
from core.pagination import PaginatedResponse, PaginationRequest
from features.tables.employees.service import EmployeeService
from features.tables.employees.schemas import EmployeeResponse, EmployeeCreate, EmployeeUpdate, EmployeeFilter

from core.database import get_db

router = APIRouter(prefix="/employees", tags=["employees"])

SessionDep = Annotated[AsyncSession, Depends(get_db)]
PaginationDep = Annotated[PaginationRequest, Query()]

NOT_FOUND = "Employee not found"
NO_FIELDS_TO_UPDATE = "No fields to update"

# ─── Create operations ──────────────────────────────────
@router.post("", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
async def create(payload: EmployeeCreate, session: SessionDep):
    """Create a new employees"""
    result = await EmployeeService(session=session).create(payload)

    return result

# ─── Read operations ──────────────────────────────────
@router.get("/{id}", response_model=EmployeeResponse, responses={404: {"description": NOT_FOUND}})
async def get_by_id(id: int, session: SessionDep):
    """Get Employee by id
    
    Args:
        id: The id to search for
    """
    record = await EmployeeService(session=session).get_by_id(id)

    if not record:
        raise HTTPException(status_code=404, detail=NOT_FOUND)

    return record

@router.get("", response_model=PaginatedResponse[EmployeeResponse])
async def get_all(pagination: PaginationDep, session: SessionDep):
    """Get all employees"""
    records = await EmployeeService(session=session).get_all(pagination)
    return records

@router.post("/search", response_model=PaginatedResponse[EmployeeResponse])
async def search(filters: EmployeeFilter, pagination: PaginationDep, session: SessionDep):
    """Search Employee by filters"""
    records = await EmployeeService(session=session).search(filters, pagination)
    return records

# ─── Update operations ──────────────────────────────────
@router.put("/{id}", 
        response_model=EmployeeResponse, 
        responses={
            400: {"description": NO_FIELDS_TO_UPDATE},
            404: {"description": NOT_FOUND},
        },
    )
async def update_by_id(id: int, payload: EmployeeUpdate, session: SessionDep):
    """Update Employee information
    
    Args:
        id: The id to update
    """
    if not payload.model_fields_set:
        raise HTTPException(status_code=400, detail=NO_FIELDS_TO_UPDATE)
    
    updated_record = await EmployeeService(session=session).update_by_id(id, payload)
    if not updated_record:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    return updated_record

# ─── Delete operations ──────────────────────────────────
@router.delete("/{id}", responses={404: {"description": NOT_FOUND}})
async def delete_by_id(id: int, session: SessionDep):
    """Delete a Employee
    
    Args:
        id: The id to delete
    """
    success = await EmployeeService(session=session).delete_by_id(id)
    if not success:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    return {"message": "Employee deleted successfully"}
