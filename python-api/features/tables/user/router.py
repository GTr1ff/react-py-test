# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c



from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, Depends, Query, status
from core.pagination import PaginatedResponse, PaginationRequest
from features.tables.user.service import UserService
from features.tables.user.schemas import UserResponse, UserCreate, UserUpdate, UserFilter

from core.database import get_db

router = APIRouter(prefix="/user", tags=["user"])

SessionDep = Annotated[AsyncSession, Depends(get_db)]
PaginationDep = Annotated[PaginationRequest, Query()]

NOT_FOUND = "User not found"
NO_FIELDS_TO_UPDATE = "No fields to update"

# ─── Create operations ──────────────────────────────────
@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create(payload: UserCreate, session: SessionDep):
    """Create a new user"""
    result = await UserService(session=session).create(payload)

    return result

# ─── Read operations ──────────────────────────────────
@router.get("/{id}", response_model=UserResponse, responses={404: {"description": NOT_FOUND}})
async def get_by_id(id: int, session: SessionDep):
    """Get User by id
    
    Args:
        id: The id to search for
    """
    record = await UserService(session=session).get_by_id(id)

    if not record:
        raise HTTPException(status_code=404, detail=NOT_FOUND)

    return record

@router.get("", response_model=PaginatedResponse[UserResponse])
async def get_all(pagination: PaginationDep, session: SessionDep):
    """Get all user"""
    records = await UserService(session=session).get_all(pagination)
    return records

@router.post("/search", response_model=PaginatedResponse[UserResponse])
async def search(filters: UserFilter, pagination: PaginationDep, session: SessionDep):
    """Search User by filters"""
    records = await UserService(session=session).search(filters, pagination)
    return records

# ─── Update operations ──────────────────────────────────
@router.put("/{id}", 
        response_model=UserResponse, 
        responses={
            400: {"description": NO_FIELDS_TO_UPDATE},
            404: {"description": NOT_FOUND},
        },
    )
async def update_by_id(id: int, payload: UserUpdate, session: SessionDep):
    """Update User information
    
    Args:
        id: The id to update
    """
    if not payload.model_fields_set:
        raise HTTPException(status_code=400, detail=NO_FIELDS_TO_UPDATE)
    
    updated_record = await UserService(session=session).update_by_id(id, payload)
    if not updated_record:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    return updated_record

# ─── Delete operations ──────────────────────────────────
@router.delete("/{id}", responses={404: {"description": NOT_FOUND}})
async def delete_by_id(id: int, session: SessionDep):
    """Delete a User
    
    Args:
        id: The id to delete
    """
    success = await UserService(session=session).delete_by_id(id)
    if not success:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    return {"message": "User deleted successfully"}
