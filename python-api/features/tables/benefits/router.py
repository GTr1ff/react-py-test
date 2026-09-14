# ROSETIC:crud-guid



from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, Depends, Query, status
from core.pagination import PaginatedResponse, PaginationRequest
from features.tables.benefits.service import BenefitService
from features.tables.benefits.schemas import BenefitResponse, BenefitCreate, BenefitUpdate, BenefitFilter

from core.database import get_db

router = APIRouter(prefix="/benefits", tags=["benefits"])

SessionDep = Annotated[AsyncSession, Depends(get_db)]
PaginationDep = Annotated[PaginationRequest, Query()]

NOT_FOUND = "Benefit not found"
NO_FIELDS_TO_UPDATE = "No fields to update"

# ─── Create operations ──────────────────────────────────
@router.post("", response_model=BenefitResponse, status_code=status.HTTP_201_CREATED)
async def create(payload: BenefitCreate, session: SessionDep):
    """Create a new benefits"""
    result = await BenefitService(session=session).create(payload)

    return result

# ─── Read operations ──────────────────────────────────
@router.get("/{id}", response_model=BenefitResponse, responses={404: {"description": NOT_FOUND}})
async def get_by_id(id: int, session: SessionDep):
    """Get Benefit by id
    
    Args:
        id: The id to search for
    """
    record = await BenefitService(session=session).get_by_id(id)

    if not record:
        raise HTTPException(status_code=404, detail=NOT_FOUND)

    return record

@router.get("", response_model=PaginatedResponse[BenefitResponse])
async def get_all(pagination: PaginationDep, session: SessionDep):
    """Get all benefits"""
    records = await BenefitService(session=session).get_all(pagination)
    return records

@router.post("/search", response_model=PaginatedResponse[BenefitResponse])
async def search(filters: BenefitFilter, pagination: PaginationDep, session: SessionDep):
    """Search Benefit by filters"""
    records = await BenefitService(session=session).search(filters, pagination)
    return records

# ─── Update operations ──────────────────────────────────
@router.put("/{id}", 
        response_model=BenefitResponse, 
        responses={
            400: {"description": NO_FIELDS_TO_UPDATE},
            404: {"description": NOT_FOUND},
        },
    )
async def update_by_id(id: int, payload: BenefitUpdate, session: SessionDep):
    """Update Benefit information
    
    Args:
        id: The id to update
    """
    if not payload.model_fields_set:
        raise HTTPException(status_code=400, detail=NO_FIELDS_TO_UPDATE)
    
    updated_record = await BenefitService(session=session).update_by_id(id, payload)
    if not updated_record:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    return updated_record

# ─── Delete operations ──────────────────────────────────
@router.delete("/{id}", responses={404: {"description": NOT_FOUND}})
async def delete_by_id(id: int, session: SessionDep):
    """Delete a Benefit
    
    Args:
        id: The id to delete
    """
    success = await BenefitService(session=session).delete_by_id(id)
    if not success:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    return {"message": "Benefit deleted successfully"}
