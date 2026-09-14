# ROSETIC:crud-guid



from typing import Any
from core.logging.repository_logger import log_repository_call
from core.db_exception_handler import handle_db_exceptions_async
from core.pagination import PaginationRequest, apply_filters, apply_pagination_filter
from features.tables.tasks.models import TaskModel
from features.tables.tasks.schemas import TaskFilter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

class TaskRepository:
    """Repository layer for all Task-related operations (CRUD)"""

    def __init__(self, session: AsyncSession):
        self.session = session
    
    # ─── Create operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Task")
    async def create(self, task_record: TaskModel) -> TaskModel | None:
        """
        Create a new Task

        Args:
            data: New Task data
            
        Returns:
            Task data if created successfully, None if Task already exists
        """
        
        # Create new Task
        self.session.add(task_record)
        await self.session.commit()
        await self.session.refresh(task_record)

        return task_record

    
    # ─── Read operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Task")
    async def get_by_id(self, id: int) -> TaskModel | None:
        """
        Get tasks by id
        
        Args:
            id: The id to search for
            
        Returns:
            Task if found, None otherwise
        """
        stmt = select(TaskModel).where(TaskModel.task_id == id)
        result = await self.session.execute(stmt)
        return result.unique().scalars().first()

    @handle_db_exceptions_async
    @log_repository_call("Task")
    async def get_all(self, pagination: PaginationRequest) -> tuple[list[TaskModel], int]:
        """
        Get all tasks
        
        Returns:
            List of all tasks
        """
        stmt = select(TaskModel)

        total = await self.session.scalar(select(func.count(TaskModel.task_id)))
        stmt = apply_pagination_filter(stmt, pagination, TaskModel)

        result = await self.session.execute(stmt)
        records = result.unique().scalars().all()
        return records, total
    
    @handle_db_exceptions_async
    @log_repository_call("Task")
    async def search(self, filters: TaskFilter, pagination: PaginationRequest) -> tuple[list[TaskModel], int]:
        stmt = select(TaskModel)
        stmt = apply_filters(stmt, filters, TaskModel)

        total = await self.session.scalar(select(func.count()).select_from(stmt.subquery()))
        stmt = apply_pagination_filter(stmt, pagination, TaskModel)

        results = await self.session.execute(stmt)
        records = results.unique().scalars().all()
        return records, total


    # ─── Update operations ──────────────────────────────────
    @handle_db_exceptions_async
    @log_repository_call("Task")
    async def update_by_id(self, id: int, updates: dict[str, Any]) -> TaskModel | None:
        """
        Update Task information
        
        Args:
            id: id of Task to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated Task if successful, None if Task not found
        """
        stmt = select(TaskModel).where(TaskModel.task_id == id)
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
    @log_repository_call("Task")
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a Task
        
        Args:
            id: id of Task to delete
            
        Returns:
            True if user was deleted, False if user not found
        """
        stmt = select(TaskModel).where(TaskModel.task_id == id)
        result = await self.session.execute(stmt)
        record = result.unique().scalars().first()
        if record:
            await self.session.delete(record)
            await self.session.commit()
            return True
        return False
