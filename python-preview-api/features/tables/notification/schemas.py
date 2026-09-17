# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c




import datetime

from pydantic import ConfigDict, Field

from core.base_schema import BaseSchema

class NotificationResponse(BaseSchema):
    id: int
    user_id: int
    title: str
    message: str
    is_read: bool
    sent_at: datetime.datetime
    created_at: datetime.datetime
    updated_at: datetime.datetime



class NotificationCreate(BaseSchema):
    user_id: int
    title: str
    message: str
    is_read: bool
    sent_at: datetime.datetime


class NotificationUpdate(BaseSchema):
    user_id: int | None = None
    title: str | None = None
    message: str | None = None
    is_read: bool | None = None
    sent_at: datetime.datetime | None = None


class NotificationFilter(BaseSchema):
    model_config = ConfigDict(extra="forbid")

    user_id: int | None= None
    title: str | None= None
    message: str | None= None
    is_read: bool | None= None
    sent_at: datetime.datetime | None= None
    created_at: datetime.datetime | None= None
    updated_at: datetime.datetime | None= None
