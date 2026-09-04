# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c



from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from features.tables.recipe.models import RecipeModel
    from features.tables.ingredient.models import IngredientModel

import sqlalchemy

import datetime
from dataclasses import Field
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base

class RecipeIngredientModel(Base):

    __tablename__ = "recipe_ingredient"
    
    __default_sort__ = "recipe_id"

    recipe_id: Mapped[int] = mapped_column(
        sqlalchemy.BigInteger,
        sqlalchemy.ForeignKey("recipe.id"),
        primary_key=True, 
        autoincrement=True, 
        index=True
    )
    ingredient_id: Mapped[int] = mapped_column(
        sqlalchemy.BigInteger,
        sqlalchemy.ForeignKey("ingredient.id"),
        index=True
    )

    recipe_id_recipe: Mapped[RecipeModel] = relationship(
        back_populates="recipe_ingredient_by_recipe_id", 
        lazy="noload",
        remote_side="RecipeModel.id",
        foreign_keys=[recipe_id]
    )
    
    ingredient_id_ingredient: Mapped[IngredientModel] = relationship(
        back_populates="recipe_ingredient_by_ingredient_id", 
        lazy="noload",
        remote_side="IngredientModel.id",
        foreign_keys=[ingredient_id]
    )
    
    quantity: Mapped[Decimal] = mapped_column(
        sqlalchemy.Numeric(12, 2),
        nullable=False
    )
    unit: Mapped[str | None] = mapped_column(
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

