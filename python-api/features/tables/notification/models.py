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

class NotificationModel(Base):

    __tablename__ = "notification"
    __table_args__ = {"schema": "public"}
    __default_sort__ = "id"

    id: Mapped[int] = mapped_column(
        sqlalchemy.BigInteger,
        primary_key=True, 
        autoincrement=True,
        unique=True, 
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        sqlalchemy.BigInteger,
        sqlalchemy.ForeignKey("public.user.id")
    )
    user_id_user: Mapped[UserModel] = relationship(
        back_populates="notification_by_user_id", 
        lazy="noload",
        remote_side="UserModel.id",
        foreign_keys=[user_id]
    )
    
    title: Mapped[str] = mapped_column(
        sqlalchemy.Text,
        nullable=False
    )
    message: Mapped[str] = mapped_column(
        sqlalchemy.Text,
        nullable=False
    )
    is_read: Mapped[bool] = mapped_column(
        sqlalchemy.Boolean,
        nullable=False
    )
    sent_at: Mapped[datetime.datetime] = mapped_column(
        sqlalchemy.DateTime(timezone=True),
        nullable=False
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

