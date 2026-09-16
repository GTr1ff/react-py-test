# ROSETIC:crud-guid


import uuid
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from core.pagination import PaginatedResponse, PaginationRequest
from features.tables.datatypestest.models import DatatypestestModel
from features.tables.datatypestest.schemas import DatatypestestResponse, DatatypestestCreate, DatatypestestUpdate, DatatypestestFilter
from features.tables.datatypestest.repository import DatatypestestRepository

class DatatypestestService:
    """Service layer for all Datatypestest-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = DatatypestestRepository(session)

    
    # ─── Read operations ──────────────────────────────────keykey
    async def get_by_keykey(self, keykey: int) -> DatatypestestResponse | None:
        """
        Get datatypestest by keykey
        
        Args:
            keykey: The keykey to search for
            
        Returns:
            DatatypestestResponse if found, None if not found
        """
        result = await self.repo.get_by_keykey(keykey)
        return DatatypestestResponse.model_validate(result) if result else None

    async def get_all(self, pagination: PaginationRequest) -> PaginatedResponse[DatatypestestResponse]:
        """
        Get all datatypestest
        
        Returns:
            List of all datatypestest
        """
        result, total = await self.repo.get_all(pagination)

        return PaginatedResponse[DatatypestestResponse](
            items=[DatatypestestResponse.model_validate(record) for record in result],
            **pagination.model_dump(),
            total=total
        )

    async def search(self, filters: DatatypestestFilter, pagination: PaginationRequest) -> PaginatedResponse[DatatypestestResponse]:
        results, total = await self.repo.search(filters, pagination)
        return PaginatedResponse[DatatypestestResponse](
            items=[DatatypestestResponse.model_validate(record) for record in results],
            **pagination.model_dump(),
            total=total
        )


    # ─── Create operations ──────────────────────────────────
    async def create(self, data: DatatypestestCreate) -> DatatypestestResponse:
        """
        Create a new Datatypestest

        Args:
            data: New Datatypestest data
            
        Returns:
            DatatypestestResponse if created successfully, None if Datatypestest already exists
        """

        # Check if unique fields already exist
        datatypestest_model = DatatypestestModel(**data.model_dump())
        
        # Create
        result = await self.repo.create(datatypestest_model)

        return DatatypestestResponse.model_validate(result)

    # ─── Update operations ──────────────────────────────────
    async def update_by_keykey(self, keykey: int, updates: DatatypestestUpdate) -> DatatypestestResponse | None:
        """
        Update Datatypestest information
        
        Args:
            keykey: keykey of Datatypestest to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated DatatypestestResponse if successful, None if Datatypestest not found
        """    
        result = await self.repo.update_by_keykey(keykey, updates.model_dump(exclude_unset=True))
        return DatatypestestResponse.model_validate(result) if result else None
    
    # ─── Delete operations ──────────────────────────────────
    async def delete_by_keykey(self, keykey: int) -> bool:
        """
        Delete a Datatypestest
        
        Args:
            keykey: keykey of Datatypestest to delete
            
        Returns:
            True if Datatypestest was deleted, False if Datatypestest not found
        """
        return await self.repo.delete_by_keykey(keykey)
