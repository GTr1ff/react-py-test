# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c




import datetime

from pydantic import ConfigDict, Field

from core.base_schema import BaseSchema

class IngredientResponse(BaseSchema):
    id: int
    name: str
    description: str | None
    category_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime



class IngredientCreate(BaseSchema):
    name: str
    description: str | None = None
    category_id: int


class IngredientUpdate(BaseSchema):
    name: str | None = None
    description: str | None = None
    category_id: int | None = None


class IngredientFilter(BaseSchema):
    model_config = ConfigDict(extra="forbid")

    name: str | None= None
    description: str | None= None
    category_id: int | None= None
    created_at: datetime.datetime | None= None
    updated_at: datetime.datetime | None= None
