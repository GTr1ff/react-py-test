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

class PayrollModel(Base):

    __tablename__ = "payroll"
    __default_sort__ = "payroll_id"

    payroll_id: Mapped[int] = mapped_column(
        sqlalchemy.Integer,
        primary_key=True, 
        autoincrement=True
    )

    employee_id: Mapped[int] = mapped_column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("employees.employee_id")
    )
    employee_id_employee: Mapped[EmployeeModel] = relationship(
        back_populates="payroll_by_employee_id", 
        lazy="noload",
        remote_side="EmployeeModel.employee_id",
        foreign_keys=[employee_id]
    )
    
    hours_worked: Mapped[Decimal | None] = mapped_column(
        sqlalchemy.Numeric(5, 2),
        nullable=True
    )
    pay_period_end: Mapped[datetime.date] = mapped_column(
        sqlalchemy.Date,
        nullable=False
    )
    pay_period_start: Mapped[datetime.date] = mapped_column(
        sqlalchemy.Date,
        nullable=False
    )
    wages: Mapped[Decimal | None] = mapped_column(
        sqlalchemy.Numeric(10, 2),
        nullable=True
    )

