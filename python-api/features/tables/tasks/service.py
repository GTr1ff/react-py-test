# ROSETIC:crud-guid



from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from core.pagination import PaginatedResponse, PaginationRequest
from features.tables.tasks.models import TaskModel
from features.tables.tasks.schemas import TaskResponse, TaskCreate, TaskUpdate, TaskFilter
from features.tables.tasks.repository import TaskRepository

class TaskService:
    """Service layer for all Task-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = TaskRepository(session)

    
    # ─── Read operations ──────────────────────────────────id
    async def get_by_id(self, id: int) -> TaskResponse | None:
        """
        Get tasks by id
        
        Args:
            id: The id to search for
            
        Returns:
            TaskResponse if found, None if not found
        """
        result = await self.repo.get_by_id(id)
        return TaskResponse.model_validate(result) if result else None

    async def get_all(self, pagination: PaginationRequest) -> PaginatedResponse[TaskResponse]:
        """
        Get all tasks
        
        Returns:
            List of all tasks
        """
        result, total = await self.repo.get_all(pagination)

        return PaginatedResponse[TaskResponse](
            items=[TaskResponse.model_validate(record) for record in result],
            **pagination.model_dump(),
            total=total
        )

    async def search(self, filters: TaskFilter, pagination: PaginationRequest) -> PaginatedResponse[TaskResponse]:
        results, total = await self.repo.search(filters, pagination)
        return PaginatedResponse[TaskResponse](
            items=[TaskResponse.model_validate(record) for record in results],
            **pagination.model_dump(),
            total=total
        )


    # ─── Create operations ──────────────────────────────────
    async def create(self, data: TaskCreate) -> TaskResponse:
        """
        Create a new Task

        Args:
            data: New Task data
            
        Returns:
            TaskResponse if created successfully, None if Task already exists
        """

        # Check if unique fields already exist
        task_model = TaskModel(**data.model_dump())
        
        # Create
        result = await self.repo.create(task_model)

        return TaskResponse.model_validate(result)

    # ─── Update operations ──────────────────────────────────
    async def update_by_id(self, id: int, updates: TaskUpdate) -> TaskResponse | None:
        """
        Update Task information
        
        Args:
            id: id of Task to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated TaskResponse if successful, None if Task not found
        """    
        result = await self.repo.update_by_id(id, updates.model_dump(exclude_unset=True))
        return TaskResponse.model_validate(result) if result else None
    
    # ─── Delete operations ──────────────────────────────────
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a Task
        
        Args:
            id: id of Task to delete
            
        Returns:
            True if Task was deleted, False if Task not found
        """
        return await self.repo.delete_by_id(id)
