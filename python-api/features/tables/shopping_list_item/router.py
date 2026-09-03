# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c



from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, Depends, Query, status
from core.pagination import PaginatedResponse, PaginationRequest
from features.tables.shopping_list_item.service import ShoppingListItemService
from features.tables.shopping_list_item.schemas import ShoppingListItemResponse, ShoppingListItemCreate, ShoppingListItemUpdate, ShoppingListItemFilter

from core.database import get_db

router = APIRouter(prefix="/shopping-list-item", tags=["shopping-list-item"])

SessionDep = Annotated[AsyncSession, Depends(get_db)]
PaginationDep = Annotated[PaginationRequest, Query()]

NOT_FOUND = "ShoppingListItem not found"
NO_FIELDS_TO_UPDATE = "No fields to update"

# ─── Create operations ──────────────────────────────────
@router.post("", response_model=ShoppingListItemResponse, status_code=status.HTTP_201_CREATED)
async def create(payload: ShoppingListItemCreate, session: SessionDep):
    """Create a new shopping_list_item"""
    result = await ShoppingListItemService(session=session).create(payload)

    return result

# ─── Read operations ──────────────────────────────────
@router.get("/{id}", response_model=ShoppingListItemResponse, responses={404: {"description": NOT_FOUND}})
async def get_by_id(id: int, session: SessionDep):
    """Get ShoppingListItem by id
    
    Args:
        id: The id to search for
    """
    record = await ShoppingListItemService(session=session).get_by_id(id)

    if not record:
        raise HTTPException(status_code=404, detail=NOT_FOUND)

    return record

@router.get("", response_model=PaginatedResponse[ShoppingListItemResponse])
async def get_all(pagination: PaginationDep, session: SessionDep):
    """Get all shopping_list_item"""
    records = await ShoppingListItemService(session=session).get_all(pagination)
    return records

@router.post("/search", response_model=PaginatedResponse[ShoppingListItemResponse])
async def search(filters: ShoppingListItemFilter, pagination: PaginationDep, session: SessionDep):
    """Search ShoppingListItem by filters"""
    records = await ShoppingListItemService(session=session).search(filters, pagination)
    return records

# ─── Update operations ──────────────────────────────────
@router.put("/{id}", 
        response_model=ShoppingListItemResponse, 
        responses={
            400: {"description": NO_FIELDS_TO_UPDATE},
            404: {"description": NOT_FOUND},
        },
    )
async def update_by_id(id: int, payload: ShoppingListItemUpdate, session: SessionDep):
    """Update ShoppingListItem information
    
    Args:
        id: The id to update
    """
    if not payload.model_fields_set:
        raise HTTPException(status_code=400, detail=NO_FIELDS_TO_UPDATE)
    
    updated_record = await ShoppingListItemService(session=session).update_by_id(id, payload)
    if not updated_record:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    return updated_record

# ─── Delete operations ──────────────────────────────────
@router.delete("/{id}", responses={404: {"description": NOT_FOUND}})
async def delete_by_id(id: int, session: SessionDep):
    """Delete a ShoppingListItem
    
    Args:
        id: The id to delete
    """
    success = await ShoppingListItemService(session=session).delete_by_id(id)
    if not success:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    return {"message": "ShoppingListItem deleted successfully"}
