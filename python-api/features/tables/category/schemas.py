# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c




import datetime

from pydantic import ConfigDict, Field

from core.base_schema import BaseSchema

class CategoryResponse(BaseSchema):
    id: int
    category_name: str
    description: str | None
    created_at: datetime.datetime
    updated_at: datetime.datetime



class CategoryCreate(BaseSchema):
    category_name: str
    description: str | None = None


class CategoryUpdate(BaseSchema):
    category_name: str | None = None
    description: str | None = None


class CategoryFilter(BaseSchema):
    model_config = ConfigDict(extra="forbid")

    category_name: str | None= None
    description: str | None= None
    created_at: datetime.datetime | None= None
    updated_at: datetime.datetime | None= None
