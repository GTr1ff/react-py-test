# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c




import datetime

from pydantic import ConfigDict, Field

from core.base_schema import BaseSchema

class RecipeResponse(BaseSchema):
    id: int
    recipe_name: str
    description: str | None
    instructions: str | None
    prep_time_minutes: int | None
    cook_time_minutes: int | None
    servings: int | None
    created_at: datetime.datetime
    updated_at: datetime.datetime



class RecipeCreate(BaseSchema):
    recipe_name: str
    description: str | None = None
    instructions: str | None = None
    prep_time_minutes: int | None = None
    cook_time_minutes: int | None = None
    servings: int | None = None


class RecipeUpdate(BaseSchema):
    recipe_name: str | None = None
    description: str | None = None
    instructions: str | None = None
    prep_time_minutes: int | None = None
    cook_time_minutes: int | None = None
    servings: int | None = None


class RecipeFilter(BaseSchema):
    model_config = ConfigDict(extra="forbid")

    recipe_name: str | None= None
    description: str | None= None
    instructions: str | None= None
    prep_time_minutes: int | None= None
    cook_time_minutes: int | None= None
    servings: int | None= None
    created_at: datetime.datetime | None= None
    updated_at: datetime.datetime | None= None
