# ROSETIC:crud-guid



from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, Depends, Query, status
from core.pagination import PaginatedResponse, PaginationRequest
from features.tables.documents.service import DocumentService
from features.tables.documents.schemas import DocumentResponse, DocumentCreate, DocumentUpdate, DocumentFilter

from core.database import get_db

router = APIRouter(prefix="/documents", tags=["documents"])

SessionDep = Annotated[AsyncSession, Depends(get_db)]
PaginationDep = Annotated[PaginationRequest, Query()]

NOT_FOUND = "Document not found"
NO_FIELDS_TO_UPDATE = "No fields to update"

# ─── Create operations ──────────────────────────────────
@router.post("", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def create(payload: DocumentCreate, session: SessionDep):
    """Create a new documents"""
    result = await DocumentService(session=session).create(payload)

    return result

# ─── Read operations ──────────────────────────────────
@router.get("/{id}", response_model=DocumentResponse, responses={404: {"description": NOT_FOUND}})
async def get_by_id(id: int, session: SessionDep):
    """Get Document by id
    
    Args:
        id: The id to search for
    """
    record = await DocumentService(session=session).get_by_id(id)

    if not record:
        raise HTTPException(status_code=404, detail=NOT_FOUND)

    return record

@router.get("", response_model=PaginatedResponse[DocumentResponse])
async def get_all(pagination: PaginationDep, session: SessionDep):
    """Get all documents"""
    records = await DocumentService(session=session).get_all(pagination)
    return records

@router.post("/search", response_model=PaginatedResponse[DocumentResponse])
async def search(filters: DocumentFilter, pagination: PaginationDep, session: SessionDep):
    """Search Document by filters"""
    records = await DocumentService(session=session).search(filters, pagination)
    return records

# ─── Update operations ──────────────────────────────────
@router.put("/{id}", 
        response_model=DocumentResponse, 
        responses={
            400: {"description": NO_FIELDS_TO_UPDATE},
            404: {"description": NOT_FOUND},
        },
    )
async def update_by_id(id: int, payload: DocumentUpdate, session: SessionDep):
    """Update Document information
    
    Args:
        id: The id to update
    """
    if not payload.model_fields_set:
        raise HTTPException(status_code=400, detail=NO_FIELDS_TO_UPDATE)
    
    updated_record = await DocumentService(session=session).update_by_id(id, payload)
    if not updated_record:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    return updated_record

# ─── Delete operations ──────────────────────────────────
@router.delete("/{id}", responses={404: {"description": NOT_FOUND}})
async def delete_by_id(id: int, session: SessionDep):
    """Delete a Document
    
    Args:
        id: The id to delete
    """
    success = await DocumentService(session=session).delete_by_id(id)
    if not success:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    return {"message": "Document deleted successfully"}
