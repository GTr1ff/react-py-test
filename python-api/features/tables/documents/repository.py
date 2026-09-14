# ROSETIC:crud-guid



from typing import Any
from core.logging.repository_logger import log_repository_call
from core.db_exception_handler import handle_db_exceptions_async
from core.pagination import PaginationRequest, apply_filters, apply_pagination_filter
from features.tables.documents.models import DocumentModel
from features.tables.documents.schemas import DocumentFilter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

class DocumentRepository:
    """Repository layer for all Document-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
    
    # ─── Create operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Document")
    async def create(self, document_record: DocumentModel) -> DocumentModel | None:
        """
        Create a new Document

        Args:
            data: New Document data
            
        Returns:
            Document data if created successfully, None if Document already exists
        """
        
        # Create new Document
        self.session.add(document_record)
        await self.session.commit()
        await self.session.refresh(document_record)

        return document_record

    
    # ─── Read operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Document")
    async def get_by_id(self, id: int) -> DocumentModel | None:
        """
        Get documents by id
        
        Args:
            id: The id to search for
            
        Returns:
            Document if found, None otherwise
        """
        stmt = select(DocumentModel).where(DocumentModel.document_id == id)
        result = await self.session.execute(stmt)
        return result.unique().scalars().first()

    @handle_db_exceptions_async
    @log_repository_call("Document")
    async def get_all(self, pagination: PaginationRequest) -> tuple[list[DocumentModel], int]:
        """
        Get all documents
        
        Returns:
            List of all documents
        """
        stmt = select(DocumentModel)

        total = await self.session.scalar(select(func.count(DocumentModel.document_id)))
        stmt = apply_pagination_filter(stmt, pagination, DocumentModel)

        result = await self.session.execute(stmt)
        records = result.unique().scalars().all()
        return records, total
    
    @handle_db_exceptions_async
    @log_repository_call("Document")
    async def search(self, filters: DocumentFilter, pagination: PaginationRequest) -> tuple[list[DocumentModel], int]:
        stmt = select(DocumentModel)
        stmt = apply_filters(stmt, filters, DocumentModel)

        total = await self.session.scalar(select(func.count()).select_from(stmt.subquery()))
        stmt = apply_pagination_filter(stmt, pagination, DocumentModel)

        results = await self.session.execute(stmt)
        records = results.unique().scalars().all()
        return records, total


    # ─── Update operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Document")
    async def update_by_id(self, id: int, updates: dict[str, Any]) -> DocumentModel | None:
        """
        Update Document information
        
        Args:
            id: id of Document to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated Document if successful, None if Document not found
        """
        stmt = select(DocumentModel).where(DocumentModel.document_id == id)
        result = await self.session.execute(stmt)
        record = result.unique().scalars().first()
        if record:
            for key, value in updates.items():
                setattr(record, key, value)
            await self.session.commit()
            await self.session.refresh(record)

        return record
    
    # ─── Delete operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Document")
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a Document
        
        Args:
            id: id of Document to delete
            
        Returns:
            True if user was deleted, False if user not found
        """
        stmt = select(DocumentModel).where(DocumentModel.document_id == id)
        result = await self.session.execute(stmt)
        record = result.unique().scalars().first()
        if record:
            await self.session.delete(record)
            await self.session.commit()
            return True
        return False
