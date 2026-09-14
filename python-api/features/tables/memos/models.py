# ROSETIC:crud-guid



from __future__ import annotations

import sqlalchemy

import datetime
from dataclasses import Field
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base

class MemoModel(Base):

    __tablename__ = "memos"
    __default_sort__ = "memo_id"

    memo_id: Mapped[int] = mapped_column(
        sqlalchemy.Integer,
        primary_key=True, 
        autoincrement=True
    )

    cc_employees: Mapped[list | None] = mapped_column(
        sqlalchemy.JSON,
        nullable=True
    )
    created_at: Mapped[datetime.datetime | None] = mapped_column(
        sqlalchemy.DateTime(timezone=True),
        nullable=True,
        server_default=sqlalchemy.func.now()
    )
    message: Mapped[str] = mapped_column(
        sqlalchemy.Text,
        nullable=False
    )

