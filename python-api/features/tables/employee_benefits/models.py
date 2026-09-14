# ROSETIC:crud-guid



from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from features.tables.employees.models import EmployeeModel
    from features.tables.benefits.models import BenefitModel

import sqlalchemy

import datetime
from dataclasses import Field
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base

class EmployeeBenefitModel(Base):

    __tablename__ = "employee_benefits"
    __default_sort__ = "employee_benefit_id"

    employee_benefit_id: Mapped[int] = mapped_column(
        sqlalchemy.Integer,
        primary_key=True, 
        autoincrement=True
    )

    benefit_id: Mapped[int] = mapped_column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("benefits.benefit_id")
    )
    benefit_id_benefit: Mapped[BenefitModel] = relationship(
        back_populates="employee_benefits_by_benefit_id", 
        lazy="noload",
        remote_side="BenefitModel.benefit_id",
        foreign_keys=[benefit_id]
    )
    
    employee_id: Mapped[int] = mapped_column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("employees.employee_id")
    )
    employee_id_employee: Mapped[EmployeeModel] = relationship(
        back_populates="employee_benefits_by_employee_id", 
        lazy="noload",
        remote_side="EmployeeModel.employee_id",
        foreign_keys=[employee_id]
    )
    
    enrollment_date: Mapped[datetime.date] = mapped_column(
        sqlalchemy.Date,
        nullable=False,
        server_default=sqlalchemy.func.current_date()
    )

