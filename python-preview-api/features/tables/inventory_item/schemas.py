# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c




import datetime
from decimal import Decimal
from pydantic import ConfigDict, Field

from core.base_schema import BaseSchema

class InventoryItemResponse(BaseSchema):
    id: int
    user_id: int
    ingredient_id: int
    quantity: Decimal
    unit: str | None
    created_at: datetime.datetime
    updated_at: datetime.datetime



class InventoryItemCreate(BaseSchema):
    user_id: int
    ingredient_id: int
    quantity: Decimal
    unit: str | None = None


class InventoryItemUpdate(BaseSchema):
    user_id: int | None = None
    ingredient_id: int | None = None
    quantity: Decimal | None = None
    unit: str | None = None


class InventoryItemFilter(BaseSchema):
    model_config = ConfigDict(extra="forbid")

    user_id: int | None= None
    ingredient_id: int | None= None
    quantity: Decimal | None= None
    unit: str | None= None
    created_at: datetime.datetime | None= None
    updated_at: datetime.datetime | None= None
