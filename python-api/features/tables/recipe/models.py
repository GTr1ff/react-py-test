# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c



from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from features.tables.recipe_ingredient.models import RecipeIngredientModel

import sqlalchemy

import datetime
from dataclasses import Field
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base

class RecipeModel(Base):

    __tablename__ = "recipe"
    
    __default_sort__ = "id"

    id: Mapped[int] = mapped_column(
        sqlalchemy.BigInteger,
        primary_key=True, 
        autoincrement=True,
        unique=True, 
        index=True
    )

    recipe_name: Mapped[str] = mapped_column(
        sqlalchemy.Text,
        nullable=False, 
        index=True
    )
    description: Mapped[str | None] = mapped_column(
        sqlalchemy.Text,
        nullable=True
    )
    instructions: Mapped[str | None] = mapped_column(
        sqlalchemy.Text,
        nullable=True
    )
    prep_time_minutes: Mapped[int | None] = mapped_column(
        sqlalchemy.Integer,
        nullable=True
    )
    cook_time_minutes: Mapped[int | None] = mapped_column(
        sqlalchemy.Integer,
        nullable=True
    )
    servings: Mapped[int | None] = mapped_column(
        sqlalchemy.Integer,
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

    recipe_ingredient_by_recipe_id: Mapped[list[RecipeIngredientModel]] = relationship(
        back_populates="recipe_id_recipe",
        lazy="noload",
        foreign_keys="RecipeIngredientModel.recipe_id"
    )
