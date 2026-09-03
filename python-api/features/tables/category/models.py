# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c



from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from features.tables.ingredient.models import IngredientModel

import sqlalchemy

import datetime
from dataclasses import Field
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base

class CategoryModel(Base):

    __tablename__ = "category"
    __table_args__ = {"schema": "public"}
    __default_sort__ = "id"

    id: Mapped[int] = mapped_column(
        sqlalchemy.BigInteger,
        primary_key=True, 
        autoincrement=True,
        unique=True, 
        index=True
    )

    category_name: Mapped[str] = mapped_column(
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

    # Child relationships

    ingredient_by_category_id: Mapped[list[IngredientModel]] = relationship(
        back_populates="category_id_category",
        lazy="noload",
        foreign_keys="IngredientModel.category_id"
    )
