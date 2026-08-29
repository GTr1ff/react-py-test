# ROSETIC:crud-guid



from __future__ import annotations

import sqlalchemy

import datetime
from dataclasses import Field
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base

class HolidayCalendarModel(Base):

    __tablename__ = "holiday_calendar"
    __default_sort__ = "holiday_id"

    holiday_id: Mapped[int] = mapped_column(
        sqlalchemy.Integer,
        primary_key=True, 
        autoincrement=True
    )

    holiday_date: Mapped[datetime.date] = mapped_column(
        sqlalchemy.Date,
        nullable=False
    )
    holiday_name: Mapped[str] = mapped_column(
        sqlalchemy.String(100),
        nullable=False
    )
    is_national: Mapped[bool | None] = mapped_column(
        sqlalchemy.Boolean,
        nullable=True,
        server_default=sqlalchemy.text("true")
    )

