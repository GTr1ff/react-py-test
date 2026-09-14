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

class DocumentModel(Base):

    __tablename__ = "documents"
    __default_sort__ = "document_id"

    document_id: Mapped[int] = mapped_column(
        sqlalchemy.Integer,
        primary_key=True, 
        autoincrement=True
    )

    doc_content: Mapped[bytes | None] = mapped_column(
        sqlalchemy.LargeBinary,
        nullable=True
    )
    doc_name: Mapped[str | None] = mapped_column(
        sqlalchemy.String(100),
        nullable=True
    )
    doc_type: Mapped[str | None] = mapped_column(
        sqlalchemy.String(50),
        nullable=True
    )
    employee_id: Mapped[int] = mapped_column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("employees.employee_id")
    )
    employee_id_employee: Mapped[EmployeeModel] = relationship(
        back_populates="documents_by_employee_id", 
        lazy="noload",
        remote_side="EmployeeModel.employee_id",
        foreign_keys=[employee_id]
    )
    

