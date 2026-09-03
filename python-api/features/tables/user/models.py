# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c



from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from features.tables.user_preference.models import UserPreferenceModel
    from features.tables.session_.models import SessionModel
    from features.tables.consent.models import ConsentModel
    from features.tables.inventory_item.models import InventoryItemModel
    from features.tables.shopping_list_item.models import ShoppingListItemModel
    from features.tables.event_log.models import EventLogModel
    from features.tables.audit_log.models import AuditLogModel
    from features.tables.notification.models import NotificationModel

import sqlalchemy

import datetime
from dataclasses import Field
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base

class UserModel(Base):

    __tablename__ = "user"
    __table_args__ = {"schema": "public"}
    __default_sort__ = "id"

    id: Mapped[int] = mapped_column(
        sqlalchemy.BigInteger,
        primary_key=True, 
        autoincrement=True,
        unique=True, 
        index=True
    )

    username: Mapped[str] = mapped_column(
        sqlalchemy.Text,
        nullable=False,
        unique=True, 
        index=True
    )
    email: Mapped[str] = mapped_column(
        sqlalchemy.Text,
        nullable=False,
        unique=True, 
        index=True
    )
    hashed_password: Mapped[str] = mapped_column(
        sqlalchemy.Text,
        nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        sqlalchemy.Boolean,
        nullable=False
    )
    last_login_at: Mapped[datetime.datetime | None] = mapped_column(
        sqlalchemy.DateTime(timezone=True),
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

    # Child relationships

    user_preference_by_user_id: Mapped[list[UserPreferenceModel]] = relationship(
        back_populates="user_id_user",
        lazy="noload",
        foreign_keys="UserPreferenceModel.user_id"
    )
    session__by_user_id: Mapped[list[SessionModel]] = relationship(
        back_populates="user_id_user",
        lazy="noload",
        foreign_keys="SessionModel.user_id"
    )
    consent_by_user_id: Mapped[list[ConsentModel]] = relationship(
        back_populates="user_id_user",
        lazy="noload",
        foreign_keys="ConsentModel.user_id"
    )
    inventory_item_by_user_id: Mapped[list[InventoryItemModel]] = relationship(
        back_populates="user_id_user",
        lazy="noload",
        foreign_keys="InventoryItemModel.user_id"
    )
    shopping_list_item_by_user_id: Mapped[list[ShoppingListItemModel]] = relationship(
        back_populates="user_id_user",
        lazy="noload",
        foreign_keys="ShoppingListItemModel.user_id"
    )
    event_log_by_user_id: Mapped[list[EventLogModel]] = relationship(
        back_populates="user_id_user",
        lazy="noload",
        foreign_keys="EventLogModel.user_id"
    )
    audit_log_by_user_id: Mapped[list[AuditLogModel]] = relationship(
        back_populates="user_id_user",
        lazy="noload",
        foreign_keys="AuditLogModel.user_id"
    )
    notification_by_user_id: Mapped[list[NotificationModel]] = relationship(
        back_populates="user_id_user",
        lazy="noload",
        foreign_keys="NotificationModel.user_id"
    )
