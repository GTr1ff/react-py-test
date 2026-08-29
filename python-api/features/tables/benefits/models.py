# ROSETIC:crud-guid



from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from features.tables.employee_benefits.models import EmployeeBenefitModel

import sqlalchemy

import datetime
from dataclasses import Field
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base

class BenefitModel(Base):

    __tablename__ = "benefits"
    __default_sort__ = "benefit_id"

    benefit_id: Mapped[int] = mapped_column(
        sqlalchemy.Integer,
        primary_key=True, 
        autoincrement=True
    )

    benefit_name: Mapped[str] = mapped_column(
        sqlalchemy.String(100),
        nullable=False
    )
    benefit_type: Mapped[str | None] = mapped_column(
        sqlalchemy.String(50),
        nullable=True
    )
    coverage_details: Mapped[dict | None] = mapped_column(
        sqlalchemy.JSON,
        nullable=True
    )
    created_at: Mapped[datetime.datetime | None] = mapped_column(
        sqlalchemy.DateTime(timezone=True),
        nullable=True,
        server_default=sqlalchemy.func.now()
    )
    monthly_cost: Mapped[Decimal | None] = mapped_column(
        sqlalchemy.Numeric(10, 2),
        nullable=True
    )

    # Child relationships

    employee_benefits_by_benefit_id: Mapped[list[EmployeeBenefitModel]] = relationship(
        back_populates="benefit_id_benefit",
        lazy="noload",
        foreign_keys="EmployeeBenefitModel.benefit_id"
    )
