# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c



from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from features.tables.inventory_item.models import InventoryItemModel
    from features.tables.recipe_ingredient.models import RecipeIngredientModel
    from features.tables.category.models import CategoryModel

import sqlalchemy

import datetime
from dataclasses import Field
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base

class IngredientModel(Base):

    __tablename__ = "ingredient"
    
    __default_sort__ = "id"

    id: Mapped[int] = mapped_column(
        sqlalchemy.BigInteger,
        primary_key=True, 
        autoincrement=True,
        unique=True, 
        index=True
    )

    name: Mapped[str] = mapped_column(
        sqlalchemy.Text,
        nullable=False,
        unique=True, 
        index=True
    )
    description: Mapped[str | None] = mapped_column(
        sqlalchemy.Text,
        nullable=True
    )
    category_id: Mapped[int] = mapped_column(
        sqlalchemy.BigInteger,
        sqlalchemy.ForeignKey("category.id")
    )
    category_id_category: Mapped[CategoryModel] = relationship(
        back_populates="ingredient_by_category_id", 
        lazy="noload",
        remote_side="CategoryModel.id",
        foreign_keys=[category_id]
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

    inventory_item_by_ingredient_id: Mapped[list[InventoryItemModel]] = relationship(
        back_populates="ingredient_id_ingredient",
        lazy="noload",
        foreign_keys="InventoryItemModel.ingredient_id"
    )
    recipe_ingredient_by_ingredient_id: Mapped[list[RecipeIngredientModel]] = relationship(
        back_populates="ingredient_id_ingredient",
        lazy="noload",
        foreign_keys="RecipeIngredientModel.ingredient_id"
    )
