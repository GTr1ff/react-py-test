# ROSETIC:crud-guid



from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from features.tables.employees.models import EmployeeModel
    from features.tables.projects.models import ProjectModel

import sqlalchemy

import datetime
from dataclasses import Field
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base

class EmployeeProjectModel(Base):

    __tablename__ = "employee_projects"
    __default_sort__ = "employee_project_id"

    employee_project_id: Mapped[int] = mapped_column(
        sqlalchemy.Integer,
        primary_key=True, 
        autoincrement=True
    )

    assigned_date: Mapped[datetime.date | None] = mapped_column(
        sqlalchemy.Date,
        nullable=True,
        server_default=sqlalchemy.func.current_date()
    )
    employee_id: Mapped[int] = mapped_column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("employees.employee_id")
    )
    employee_id_employee: Mapped[EmployeeModel] = relationship(
        back_populates="employee_projects_by_employee_id", 
        lazy="noload",
        remote_side="EmployeeModel.employee_id",
        foreign_keys=[employee_id]
    )
    
    project_id: Mapped[int] = mapped_column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("projects.project_id")
    )
    project_id_project: Mapped[ProjectModel] = relationship(
        back_populates="employee_projects_by_project_id", 
        lazy="noload",
        remote_side="ProjectModel.project_id",
        foreign_keys=[project_id]
    )
    
    role_name: Mapped[str | None] = mapped_column(
        sqlalchemy.String(50),
        nullable=True
    )

