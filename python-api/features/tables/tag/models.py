# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c



from __future__ import annotations

import sqlalchemy

import datetime
from dataclasses import Field
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base

class TagModel(Base):

    __tablename__ = "tag"
    __table_args__ = {"schema": "public"}
    __default_sort__ = "id"

    id: Mapped[int] = mapped_column(
        sqlalchemy.BigInteger,
        primary_key=True, 
        autoincrement=True,
        unique=True, 
        index=True
    )

    tag_name: Mapped[str] = mapped_column(
        sqlalchemy.Text,
        nullable=False,
        unique=True, 
        index=True
    )
    description: Mapped[str | None] = mapped_column(
        sqlalchemy.Text,
        nullable=True
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        sqlalchemy.DateTime(timezone=True),
        nullable=False, 
        index=True,
        server_default=sqlalchemy.func.now()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        sqlalchemy.DateTime(timezone=True),
        nullable=False, 
        index=True,
        server_default=sqlalchemy.func.now(),
        onupdate=sqlalchemy.func.now()
    )

