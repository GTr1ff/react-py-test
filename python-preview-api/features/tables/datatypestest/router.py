# ROSETIC:crud-guid


import uuid
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, Depends, Query, status
from core.pagination import PaginatedResponse, PaginationRequest
from features.tables.datatypestest.service import DatatypestestService
from features.tables.datatypestest.schemas import DatatypestestResponse, DatatypestestCreate, DatatypestestUpdate, DatatypestestFilter

from core.database import get_db

router = APIRouter(prefix="/datatypestest", tags=["datatypestest"])

SessionDep = Annotated[AsyncSession, Depends(get_db)]
PaginationDep = Annotated[PaginationRequest, Query()]

NOT_FOUND = "Datatypestest not found"
NO_FIELDS_TO_UPDATE = "No fields to update"

# ─── Create operations ──────────────────────────────────
@router.post("", response_model=DatatypestestResponse, status_code=status.HTTP_201_CREATED)
async def create(payload: DatatypestestCreate, session: SessionDep):
    """Create a new datatypestest"""
    result = await DatatypestestService(session=session).create(payload)

    return result

# ─── Read operations ──────────────────────────────────
@router.get("/{keykey}", response_model=DatatypestestResponse, responses={404: {"description": NOT_FOUND}})
async def get_by_keykey(keykey: int, session: SessionDep):
    """Get Datatypestest by keykey
    
    Args:
        keykey: The keykey to search for
    """
    record = await DatatypestestService(session=session).get_by_keykey(keykey)

    if not record:
        raise HTTPException(status_code=404, detail=NOT_FOUND)

    return record

@router.get("", response_model=PaginatedResponse[DatatypestestResponse])
async def get_all(pagination: PaginationDep, session: SessionDep):
    """Get all datatypestest"""
    records = await DatatypestestService(session=session).get_all(pagination)
    return records

@router.post("/search", response_model=PaginatedResponse[DatatypestestResponse])
async def search(filters: DatatypestestFilter, pagination: PaginationDep, session: SessionDep):
    """Search Datatypestest by filters"""
    records = await DatatypestestService(session=session).search(filters, pagination)
    return records

# ─── Update operations ──────────────────────────────────
@router.put("/{keykey}", 
        response_model=DatatypestestResponse, 
        responses={
            400: {"description": NO_FIELDS_TO_UPDATE},
            404: {"description": NOT_FOUND},
        },
    )
async def update_by_keykey(keykey: int, payload: DatatypestestUpdate, session: SessionDep):
    """Update Datatypestest information
    
    Args:
        keykey: The keykey to update
    """
    if not payload.model_fields_set:
        raise HTTPException(status_code=400, detail=NO_FIELDS_TO_UPDATE)
    
    updated_record = await DatatypestestService(session=session).update_by_keykey(keykey, payload)
    if not updated_record:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    return updated_record

# ─── Delete operations ──────────────────────────────────
@router.delete("/{keykey}", responses={404: {"description": NOT_FOUND}})
async def delete_by_keykey(keykey: int, session: SessionDep):
    """Delete a Datatypestest
    
    Args:
        keykey: The keykey to delete
    """
    success = await DatatypestestService(session=session).delete_by_keykey(keykey)
    if not success:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    return {"message": "Datatypestest deleted successfully"}
