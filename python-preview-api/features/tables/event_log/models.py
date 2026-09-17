# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c



from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from features.tables.user.models import UserModel

import sqlalchemy

import datetime
from dataclasses import Field
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base

class EventLogModel(Base):

    __tablename__ = "event_log"
    
    __default_sort__ = "id"

    id: Mapped[int] = mapped_column(
        sqlalchemy.Integer,
        primary_key=True, 
        autoincrement=True,
        unique=True, 
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("user.id")
    )
    user_id_user: Mapped[UserModel] = relationship(
        back_populates="event_log_by_user_id", 
        lazy="noload",
        remote_side="UserModel.id",
        foreign_keys=[user_id]
    )
    
    event_type: Mapped[str] = mapped_column(
        sqlalchemy.Text,
        nullable=False, 
        index=True
    )
    event_timestamp: Mapped[datetime.datetime] = mapped_column(
        sqlalchemy.DateTime(timezone=True),
        nullable=False, 
        index=True
    )
    event_data: Mapped[dict | None] = mapped_column(
        sqlalchemy.JSON,
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

