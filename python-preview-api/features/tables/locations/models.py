# ROSETIC:crud-guid



from __future__ import annotations

import sqlalchemy

import datetime
from dataclasses import Field
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base

class LocationModel(Base):

    __tablename__ = "locations"
    __default_sort__ = "location_id"

    location_id: Mapped[int] = mapped_column(
        sqlalchemy.Integer,
        primary_key=True, 
        autoincrement=True
    )

    address_line_1: Mapped[str | None] = mapped_column(
        sqlalchemy.String(100),
        nullable=True
    )
    address_line_2: Mapped[str | None] = mapped_column(
        sqlalchemy.String(100),
        nullable=True
    )
    city: Mapped[str | None] = mapped_column(
        sqlalchemy.String(100),
        nullable=True
    )
    country: Mapped[str | None] = mapped_column(
        sqlalchemy.String(100),
        nullable=True
    )
    location_name: Mapped[str | None] = mapped_column(
        sqlalchemy.String(100),
        nullable=True
    )
    state: Mapped[str | None] = mapped_column(
        sqlalchemy.String(100),
        nullable=True
    )
    zip_code: Mapped[str | None] = mapped_column(
        sqlalchemy.String(20),
        nullable=True
    )

