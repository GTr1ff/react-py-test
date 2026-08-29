# ROSETIC:crud-guid



from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from features.tables.employees.models import EmployeeModel
    from features.tables.employees.models import EmployeeModel

import sqlalchemy

import datetime
from dataclasses import Field
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base

class LeafModel(Base):

    __tablename__ = "leaves"
    __default_sort__ = "leave_id"

    leave_id: Mapped[int] = mapped_column(
        sqlalchemy.Integer,
        primary_key=True, 
        autoincrement=True
    )

    approval_status: Mapped[str | None] = mapped_column(
        sqlalchemy.String(20),
        nullable=True
    )
    approved_by: Mapped[int | None] = mapped_column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("employees.employee_id")
    )
    approved_by_employee: Mapped[EmployeeModel| None] = relationship(
        back_populates="leaves_by_approved_by", 
        lazy="noload",
        remote_side="EmployeeModel.employee_id",
        foreign_keys=[approved_by]
    )
    
    employee_id: Mapped[int] = mapped_column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("employees.employee_id")
    )
    employee_id_employee: Mapped[EmployeeModel] = relationship(
        back_populates="leaves_by_employee_id", 
        lazy="noload",
        remote_side="EmployeeModel.employee_id",
        foreign_keys=[employee_id]
    )
    
    end_date: Mapped[datetime.date] = mapped_column(
        sqlalchemy.Date,
        nullable=False
    )
    reason: Mapped[str | None] = mapped_column(
        sqlalchemy.Text,
        nullable=True
    )
    start_date: Mapped[datetime.date] = mapped_column(
        sqlalchemy.Date,
        nullable=False
    )

