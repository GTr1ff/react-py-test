# ROSETIC:crud-guid



from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from features.tables.projects.models import ProjectModel
    from features.tables.employees.models import EmployeeModel

import sqlalchemy

import datetime
from dataclasses import Field
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base

class TaskModel(Base):

    __tablename__ = "tasks"
    __default_sort__ = "task_id"

    task_id: Mapped[int] = mapped_column(
        sqlalchemy.Integer,
        primary_key=True, 
        autoincrement=True
    )

    assigned_to: Mapped[int | None] = mapped_column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("employees.employee_id")
    )
    assigned_to_employee: Mapped[EmployeeModel| None] = relationship(
        back_populates="tasks_by_assigned_to", 
        lazy="noload",
        remote_side="EmployeeModel.employee_id",
        foreign_keys=[assigned_to]
    )
    
    attachment: Mapped[bytes | None] = mapped_column(
        sqlalchemy.LargeBinary,
        nullable=True
    )
    completed: Mapped[bool | None] = mapped_column(
        sqlalchemy.Boolean,
        nullable=True,
        server_default=sqlalchemy.text("false")
    )
    due_date: Mapped[datetime.date | None] = mapped_column(
        sqlalchemy.Date,
        nullable=True
    )
    notes: Mapped[str | None] = mapped_column(
        sqlalchemy.Text,
        nullable=True
    )
    project_id: Mapped[int] = mapped_column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("projects.project_id")
    )
    project_id_project: Mapped[ProjectModel] = relationship(
        back_populates="tasks_by_project_id", 
        lazy="noload",
        remote_side="ProjectModel.project_id",
        foreign_keys=[project_id]
    )
    

