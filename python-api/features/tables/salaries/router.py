# ROSETIC:crud-guid



from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, Depends, Query, status
from core.pagination import PaginatedResponse, PaginationRequest
from features.tables.salaries.service import SalaryService
from features.tables.salaries.schemas import SalaryResponse, SalaryCreate, SalaryUpdate, SalaryFilter

from core.database import get_db

router = APIRouter(prefix="/salaries", tags=["salaries"])

SessionDep = Annotated[AsyncSession, Depends(get_db)]
PaginationDep = Annotated[PaginationRequest, Query()]

NOT_FOUND = "Salary not found"
NO_FIELDS_TO_UPDATE = "No fields to update"

# ─── Create operations ──────────────────────────────────
@router.post("", response_model=SalaryResponse, status_code=status.HTTP_201_CREATED)
async def create(payload: SalaryCreate, session: SessionDep):
    """Create a new salaries"""
    result = await SalaryService(session=session).create(payload)

    return result

# ─── Read operations ──────────────────────────────────
@router.get("/{id}", response_model=SalaryResponse, responses={404: {"description": NOT_FOUND}})
async def get_by_id(id: int, session: SessionDep):
    """Get Salary by id
    
    Args:
        id: The id to search for
    """
    record = await SalaryService(session=session).get_by_id(id)

    if not record:
        raise HTTPException(status_code=404, detail=NOT_FOUND)

    return record

@router.get("", response_model=PaginatedResponse[SalaryResponse])
async def get_all(pagination: PaginationDep, session: SessionDep):
    """Get all salaries"""
    records = await SalaryService(session=session).get_all(pagination)
    return records

@router.post("/search", response_model=PaginatedResponse[SalaryResponse])
async def search(filters: SalaryFilter, pagination: PaginationDep, session: SessionDep):
    """Search Salary by filters"""
    records = await SalaryService(session=session).search(filters, pagination)
    return records

# ─── Update operations ──────────────────────────────────
@router.put("/{id}", 
        response_model=SalaryResponse, 
        responses={
            400: {"description": NO_FIELDS_TO_UPDATE},
            404: {"description": NOT_FOUND},
        },
    )
async def update_by_id(id: int, payload: SalaryUpdate, session: SessionDep):
    """Update Salary information
    
    Args:
        id: The id to update
    """
    if not payload.model_fields_set:
        raise HTTPException(status_code=400, detail=NO_FIELDS_TO_UPDATE)
    
    updated_record = await SalaryService(session=session).update_by_id(id, payload)
    if not updated_record:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    return updated_record

# ─── Delete operations ──────────────────────────────────
@router.delete("/{id}", responses={404: {"description": NOT_FOUND}})
async def delete_by_id(id: int, session: SessionDep):
    """Delete a Salary
    
    Args:
        id: The id to delete
    """
    success = await SalaryService(session=session).delete_by_id(id)
    if not success:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    return {"message": "Salary deleted successfully"}
