# ROSETIC:crud-guid



from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from features.tables.job_history.models import JobHistoryModel

import sqlalchemy

import datetime
from dataclasses import Field
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base

class RoleModel(Base):

    __tablename__ = "roles"
    __default_sort__ = "role_id"

    role_id: Mapped[int] = mapped_column(
        sqlalchemy.Integer,
        primary_key=True, 
        autoincrement=True
    )

    privileges: Mapped[list | None] = mapped_column(
        sqlalchemy.JSON,
        nullable=True
    )
    role_name: Mapped[str] = mapped_column(
        sqlalchemy.String(50),
        nullable=False
    )

    # Child relationships

    job_history_by_role_id: Mapped[list[JobHistoryModel]] = relationship(
        back_populates="role_id_role",
        lazy="noload",
        foreign_keys="JobHistoryModel.role_id"
    )
