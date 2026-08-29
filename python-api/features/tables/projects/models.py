# ROSETIC:crud-guid



from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from features.tables.tasks.models import TaskModel
    from features.tables.employee_projects.models import EmployeeProjectModel

import sqlalchemy

import datetime
from dataclasses import Field
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base

class ProjectModel(Base):

    __tablename__ = "projects"
    __default_sort__ = "project_id"

    project_id: Mapped[int] = mapped_column(
        sqlalchemy.Integer,
        primary_key=True, 
        autoincrement=True
    )

    budget: Mapped[Decimal | None] = mapped_column(
        sqlalchemy.Numeric(12, 2),
        nullable=True
    )
    created_at: Mapped[datetime.datetime | None] = mapped_column(
        sqlalchemy.DateTime(timezone=True),
        nullable=True,
        server_default=sqlalchemy.func.now()
    )
    end_date: Mapped[datetime.date | None] = mapped_column(
        sqlalchemy.Date,
        nullable=True
    )
    project_name: Mapped[str] = mapped_column(
        sqlalchemy.String(200),
        nullable=False
    )
    start_date: Mapped[datetime.date | None] = mapped_column(
        sqlalchemy.Date,
        nullable=True
    )
    status: Mapped[str] = mapped_column(
        sqlalchemy.String(50),
        nullable=False
    )
    tags: Mapped[list | None] = mapped_column(
        sqlalchemy.JSON,
        nullable=True
    )

    # Child relationships

    tasks_by_project_id: Mapped[list[TaskModel]] = relationship(
        back_populates="project_id_project",
        lazy="noload",
        foreign_keys="TaskModel.project_id"
    )
    employee_projects_by_project_id: Mapped[list[EmployeeProjectModel]] = relationship(
        back_populates="project_id_project",
        lazy="noload",
        foreign_keys="EmployeeProjectModel.project_id"
    )
