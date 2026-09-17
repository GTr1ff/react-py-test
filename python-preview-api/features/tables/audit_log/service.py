# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c



from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from core.pagination import PaginatedResponse, PaginationRequest
from features.tables.audit_log.models import AuditLogModel
from features.tables.audit_log.schemas import AuditLogResponse, AuditLogCreate, AuditLogUpdate, AuditLogFilter
from features.tables.audit_log.repository import AuditLogRepository

class AuditLogService:
    """Service layer for all AuditLog-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = AuditLogRepository(session)

    
    # ─── Read operations ──────────────────────────────────id
    async def get_by_id(self, id: int) -> AuditLogResponse | None:
        """
        Get audit_log by id
        
        Args:
            id: The id to search for
            
        Returns:
            AuditLogResponse if found, None if not found
        """
        result = await self.repo.get_by_id(id)
        return AuditLogResponse.model_validate(result) if result else None

    async def get_all(self, pagination: PaginationRequest) -> PaginatedResponse[AuditLogResponse]:
        """
        Get all audit_log
        
        Returns:
            List of all audit_log
        """
        result, total = await self.repo.get_all(pagination)

        return PaginatedResponse[AuditLogResponse](
            items=[AuditLogResponse.model_validate(record) for record in result],
            **pagination.model_dump(),
            total=total
        )

    async def search(self, filters: AuditLogFilter, pagination: PaginationRequest) -> PaginatedResponse[AuditLogResponse]:
        results, total = await self.repo.search(filters, pagination)
        return PaginatedResponse[AuditLogResponse](
            items=[AuditLogResponse.model_validate(record) for record in results],
            **pagination.model_dump(),
            total=total
        )


    # ─── Create operations ──────────────────────────────────
    async def create(self, data: AuditLogCreate) -> AuditLogResponse:
        """
        Create a new AuditLog

        Args:
            data: New AuditLog data
            
        Returns:
            AuditLogResponse if created successfully, None if AuditLog already exists
        """

        # Check if unique fields already exist
        auditlog_model = AuditLogModel(**data.model_dump())
        
        # Create
        result = await self.repo.create(auditlog_model)

        return AuditLogResponse.model_validate(result)

    # ─── Update operations ──────────────────────────────────
    async def update_by_id(self, id: int, updates: AuditLogUpdate) -> AuditLogResponse | None:
        """
        Update AuditLog information
        
        Args:
            id: id of AuditLog to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated AuditLogResponse if successful, None if AuditLog not found
        """    
        result = await self.repo.update_by_id(id, updates.model_dump(exclude_unset=True))
        return AuditLogResponse.model_validate(result) if result else None
    
    # ─── Delete operations ──────────────────────────────────
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a AuditLog
        
        Args:
            id: id of AuditLog to delete
            
        Returns:
            True if AuditLog was deleted, False if AuditLog not found
        """
        return await self.repo.delete_by_id(id)
