# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c




import datetime
from decimal import Decimal
from pydantic import ConfigDict, Field

from core.base_schema import BaseSchema

class ShoppingListItemResponse(BaseSchema):
    id: int
    user_id: int
    item_name: str
    quantity: Decimal | None
    notes: str | None
    created_at: datetime.datetime
    updated_at: datetime.datetime



class ShoppingListItemCreate(BaseSchema):
    user_id: int
    item_name: str
    quantity: Decimal | None = None
    notes: str | None = None


class ShoppingListItemUpdate(BaseSchema):
    user_id: int | None = None
    item_name: str | None = None
    quantity: Decimal | None = None
    notes: str | None = None


class ShoppingListItemFilter(BaseSchema):
    model_config = ConfigDict(extra="forbid")

    user_id: int | None= None
    item_name: str | None= None
    quantity: Decimal | None= None
    notes: str | None= None
    created_at: datetime.datetime | None= None
    updated_at: datetime.datetime | None= None
