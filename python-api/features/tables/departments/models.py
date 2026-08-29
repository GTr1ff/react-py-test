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

class DepartmentModel(Base):

    __tablename__ = "departments"
    __default_sort__ = "department_id"

    department_id: Mapped[int] = mapped_column(
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
    department_name: Mapped[str] = mapped_column(
        sqlalchemy.String(100),
        nullable=False
    )
    location: Mapped[str | None] = mapped_column(
        sqlalchemy.String(100),
        nullable=True
    )
    manager_id: Mapped[int | None] = mapped_column(
        sqlalchemy.Integer,
        nullable=True
    )
    updated_at: Mapped[datetime.datetime | None] = mapped_column(
        sqlalchemy.DateTime(timezone=True),
        nullable=True,
        server_default=sqlalchemy.func.now(),
        onupdate=sqlalchemy.func.now()
    )

    # Child relationships

    employees_by_department_id: Mapped[list[EmployeeModel]] = relationship(
        back_populates="department_id_department",
        lazy="noload",
        foreign_keys="EmployeeModel.department_id"
    )
