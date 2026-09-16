# ROSETIC:crud-guid



from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from features.tables.employees.models import EmployeeModel

import sqlalchemy

import datetime
from dataclasses import Field
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base

class SalaryModel(Base):

    __tablename__ = "salaries"
    __default_sort__ = "salary_id"

    salary_id: Mapped[int] = mapped_column(
        sqlalchemy.Integer,
        primary_key=True, 
        autoincrement=True
    )

    currency: Mapped[str] = mapped_column(
        sqlalchemy.String(3),
        nullable=False
    )
    effective_date: Mapped[datetime.date] = mapped_column(
        sqlalchemy.Date,
        nullable=False
    )
    employee_id: Mapped[int] = mapped_column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("employees.employee_id")
    )
    employee_id_employee: Mapped[EmployeeModel] = relationship(
        back_populates="salaries_by_employee_id", 
        lazy="noload",
        remote_side="EmployeeModel.employee_id",
        foreign_keys=[employee_id]
    )
    
    salary: Mapped[Decimal] = mapped_column(
        sqlalchemy.Numeric(10, 2),
        nullable=False
    )

