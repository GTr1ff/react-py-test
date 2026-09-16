# ROSETIC:crud-guid



from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from core.pagination import PaginatedResponse, PaginationRequest
from features.tables.documents.models import DocumentModel
from features.tables.documents.schemas import DocumentResponse, DocumentCreate, DocumentUpdate, DocumentFilter
from features.tables.documents.repository import DocumentRepository

class DocumentService:
    """Service layer for all Document-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = DocumentRepository(session)

    
    # ─── Read operations ──────────────────────────────────id
    async def get_by_id(self, id: int) -> DocumentResponse | None:
        """
        Get documents by id
        
        Args:
            id: The id to search for
            
        Returns:
            DocumentResponse if found, None if not found
        """
        result = await self.repo.get_by_id(id)
        return DocumentResponse.model_validate(result) if result else None

    async def get_all(self, pagination: PaginationRequest) -> PaginatedResponse[DocumentResponse]:
        """
        Get all documents
        
        Returns:
            List of all documents
        """
        result, total = await self.repo.get_all(pagination)

        return PaginatedResponse[DocumentResponse](
            items=[DocumentResponse.model_validate(record) for record in result],
            **pagination.model_dump(),
            total=total
        )

    async def search(self, filters: DocumentFilter, pagination: PaginationRequest) -> PaginatedResponse[DocumentResponse]:
        results, total = await self.repo.search(filters, pagination)
        return PaginatedResponse[DocumentResponse](
            items=[DocumentResponse.model_validate(record) for record in results],
            **pagination.model_dump(),
            total=total
        )


    # ─── Create operations ──────────────────────────────────
    async def create(self, data: DocumentCreate) -> DocumentResponse:
        """
        Create a new Document

        Args:
            data: New Document data
            
        Returns:
            DocumentResponse if created successfully, None if Document already exists
        """

        # Check if unique fields already exist
        document_model = DocumentModel(**data.model_dump())
        
        # Create
        result = await self.repo.create(document_model)

        return DocumentResponse.model_validate(result)

    # ─── Update operations ──────────────────────────────────
    async def update_by_id(self, id: int, updates: DocumentUpdate) -> DocumentResponse | None:
        """
        Update Document information
        
        Args:
            id: id of Document to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated DocumentResponse if successful, None if Document not found
        """    
        result = await self.repo.update_by_id(id, updates.model_dump(exclude_unset=True))
        return DocumentResponse.model_validate(result) if result else None
    
    # ─── Delete operations ──────────────────────────────────
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a Document
        
        Args:
            id: id of Document to delete
            
        Returns:
            True if Document was deleted, False if Document not found
        """
        return await self.repo.delete_by_id(id)
