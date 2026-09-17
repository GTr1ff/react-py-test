# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c



from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, Depends, Query, status
from core.pagination import PaginatedResponse, PaginationRequest
from features.tables.inventory_item.service import InventoryItemService
from features.tables.inventory_item.schemas import InventoryItemResponse, InventoryItemCreate, InventoryItemUpdate, InventoryItemFilter

from core.database import get_db

router = APIRouter(prefix="/inventory-item", tags=["inventory-item"])

SessionDep = Annotated[AsyncSession, Depends(get_db)]
PaginationDep = Annotated[PaginationRequest, Query()]

NOT_FOUND = "InventoryItem not found"
NO_FIELDS_TO_UPDATE = "No fields to update"

# ─── Create operations ──────────────────────────────────
@router.post("", response_model=InventoryItemResponse, status_code=status.HTTP_201_CREATED)
async def create(payload: InventoryItemCreate, session: SessionDep):
    """Create a new inventory_item"""
    result = await InventoryItemService(session=session).create(payload)

    return result

# ─── Read operations ──────────────────────────────────
@router.get("/{id}", response_model=InventoryItemResponse, responses={404: {"description": NOT_FOUND}})
async def get_by_id(id: int, session: SessionDep):
    """Get InventoryItem by id
    
    Args:
        id: The id to search for
    """
    record = await InventoryItemService(session=session).get_by_id(id)

    if not record:
        raise HTTPException(status_code=404, detail=NOT_FOUND)

    return record

@router.get("", response_model=PaginatedResponse[InventoryItemResponse])
async def get_all(pagination: PaginationDep, session: SessionDep):
    """Get all inventory_item"""
    records = await InventoryItemService(session=session).get_all(pagination)
    return records

@router.post("/search", response_model=PaginatedResponse[InventoryItemResponse])
async def search(filters: InventoryItemFilter, pagination: PaginationDep, session: SessionDep):
    """Search InventoryItem by filters"""
    records = await InventoryItemService(session=session).search(filters, pagination)
    return records

# ─── Update operations ──────────────────────────────────
@router.put("/{id}", 
        response_model=InventoryItemResponse, 
        responses={
            400: {"description": NO_FIELDS_TO_UPDATE},
            404: {"description": NOT_FOUND},
        },
    )
async def update_by_id(id: int, payload: InventoryItemUpdate, session: SessionDep):
    """Update InventoryItem information
    
    Args:
        id: The id to update
    """
    if not payload.model_fields_set:
        raise HTTPException(status_code=400, detail=NO_FIELDS_TO_UPDATE)
    
    updated_record = await InventoryItemService(session=session).update_by_id(id, payload)
    if not updated_record:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    return updated_record

# ─── Delete operations ──────────────────────────────────
@router.delete("/{id}", responses={404: {"description": NOT_FOUND}})
async def delete_by_id(id: int, session: SessionDep):
    """Delete a InventoryItem
    
    Args:
        id: The id to delete
    """
    success = await InventoryItemService(session=session).delete_by_id(id)
    if not success:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    return {"message": "InventoryItem deleted successfully"}
