# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c




import datetime
from decimal import Decimal
from pydantic import ConfigDict, Field

from core.base_schema import BaseSchema

class RecipeIngredientResponse(BaseSchema):
    recipe_id: int
    ingredient_id: int
    quantity: Decimal
    unit: str | None
    created_at: datetime.datetime
    updated_at: datetime.datetime



class RecipeIngredientCreate(BaseSchema):
    recipe_id: int
    ingredient_id: int
    quantity: Decimal
    unit: str | None = None


class RecipeIngredientUpdate(BaseSchema):
    recipe_id: int | None = None
    ingredient_id: int | None = None
    quantity: Decimal | None = None
    unit: str | None = None


class RecipeIngredientFilter(BaseSchema):
    model_config = ConfigDict(extra="forbid")

    quantity: Decimal | None= None
    unit: str | None= None
    created_at: datetime.datetime | None= None
    updated_at: datetime.datetime | None= None
