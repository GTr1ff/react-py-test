# ROSETIC:crud-guid



from __future__ import annotations

import sqlalchemy

import datetime
from dataclasses import Field
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base

class SettingModel(Base):

    __tablename__ = "settings"
    __default_sort__ = "setting_id"

    setting_id: Mapped[int] = mapped_column(
        sqlalchemy.Integer,
        primary_key=True, 
        autoincrement=True
    )

    setting_key: Mapped[str] = mapped_column(
        sqlalchemy.Text,
        nullable=False
    )
    setting_value: Mapped[dict | None] = mapped_column(
        sqlalchemy.JSON,
        nullable=True
    )
    updated_at: Mapped[datetime.datetime | None] = mapped_column(
        sqlalchemy.DateTime(timezone=True),
        nullable=True,
        server_default=sqlalchemy.func.now(),
        onupdate=sqlalchemy.func.now()
    )

