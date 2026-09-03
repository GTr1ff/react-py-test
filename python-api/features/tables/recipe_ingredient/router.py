# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c



from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, Depends, Query, status
from core.pagination import PaginatedResponse, PaginationRequest
from features.tables.recipe_ingredient.service import RecipeIngredientService
from features.tables.recipe_ingredient.schemas import RecipeIngredientResponse, RecipeIngredientCreate, RecipeIngredientUpdate, RecipeIngredientFilter

from core.database import get_db

router = APIRouter(prefix="/recipe-ingredient", tags=["recipe-ingredient"])

SessionDep = Annotated[AsyncSession, Depends(get_db)]
PaginationDep = Annotated[PaginationRequest, Query()]

NOT_FOUND = "RecipeIngredient not found"
NO_FIELDS_TO_UPDATE = "No fields to update"

# ─── Create operations ──────────────────────────────────
@router.post("", response_model=RecipeIngredientResponse, status_code=status.HTTP_201_CREATED)
async def create(payload: RecipeIngredientCreate, session: SessionDep):
    """Create a new recipe_ingredient"""
    result = await RecipeIngredientService(session=session).create(payload)

    return result

# ─── Read operations ──────────────────────────────────
@router.get("/{id}", response_model=RecipeIngredientResponse, responses={404: {"description": NOT_FOUND}})
async def get_by_id(id: int, session: SessionDep):
    """Get RecipeIngredient by id
    
    Args:
        id: The id to search for
    """
    record = await RecipeIngredientService(session=session).get_by_id(id)

    if not record:
        raise HTTPException(status_code=404, detail=NOT_FOUND)

    return record

@router.get("", response_model=PaginatedResponse[RecipeIngredientResponse])
async def get_all(pagination: PaginationDep, session: SessionDep):
    """Get all recipe_ingredient"""
    records = await RecipeIngredientService(session=session).get_all(pagination)
    return records

@router.post("/search", response_model=PaginatedResponse[RecipeIngredientResponse])
async def search(filters: RecipeIngredientFilter, pagination: PaginationDep, session: SessionDep):
    """Search RecipeIngredient by filters"""
    records = await RecipeIngredientService(session=session).search(filters, pagination)
    return records

# ─── Update operations ──────────────────────────────────
@router.put("/{id}", 
        response_model=RecipeIngredientResponse, 
        responses={
            400: {"description": NO_FIELDS_TO_UPDATE},
            404: {"description": NOT_FOUND},
        },
    )
async def update_by_id(id: int, payload: RecipeIngredientUpdate, session: SessionDep):
    """Update RecipeIngredient information
    
    Args:
        id: The id to update
    """
    if not payload.model_fields_set:
        raise HTTPException(status_code=400, detail=NO_FIELDS_TO_UPDATE)
    
    updated_record = await RecipeIngredientService(session=session).update_by_id(id, payload)
    if not updated_record:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    return updated_record

# ─── Delete operations ──────────────────────────────────
@router.delete("/{id}", responses={404: {"description": NOT_FOUND}})
async def delete_by_id(id: int, session: SessionDep):
    """Delete a RecipeIngredient
    
    Args:
        id: The id to delete
    """
    success = await RecipeIngredientService(session=session).delete_by_id(id)
    if not success:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    return {"message": "RecipeIngredient deleted successfully"}
