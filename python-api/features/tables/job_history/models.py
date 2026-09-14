# ROSETIC:crud-guid



from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from features.tables.employees.models import EmployeeModel
    from features.tables.roles.models import RoleModel

import sqlalchemy

import datetime
from dataclasses import Field
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base

class JobHistoryModel(Base):

    __tablename__ = "job_history"
    __default_sort__ = "job_history_id"

    job_history_id: Mapped[int] = mapped_column(
        sqlalchemy.Integer,
        primary_key=True, 
        autoincrement=True
    )

    employee_id: Mapped[int] = mapped_column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("employees.employee_id")
    )
    employee_id_employee: Mapped[EmployeeModel] = relationship(
        back_populates="job_history_by_employee_id", 
        lazy="noload",
        remote_side="EmployeeModel.employee_id",
        foreign_keys=[employee_id]
    )
    
    end_date: Mapped[datetime.date | None] = mapped_column(
        sqlalchemy.Date,
        nullable=True
    )
    role_id: Mapped[int] = mapped_column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("roles.role_id")
    )
    role_id_role: Mapped[RoleModel] = relationship(
        back_populates="job_history_by_role_id", 
        lazy="noload",
        remote_side="RoleModel.role_id",
        foreign_keys=[role_id]
    )
    
    start_date: Mapped[datetime.date] = mapped_column(
        sqlalchemy.Date,
        nullable=False
    )

