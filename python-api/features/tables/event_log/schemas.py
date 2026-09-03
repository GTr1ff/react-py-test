# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c




import datetime

from pydantic import ConfigDict, Field

from core.base_schema import BaseSchema

class EventLogResponse(BaseSchema):
    id: int
    user_id: int
    event_type: str
    event_timestamp: datetime.datetime
    event_data: dict | None
    created_at: datetime.datetime
    updated_at: datetime.datetime



class EventLogCreate(BaseSchema):
    user_id: int
    event_type: str
    event_timestamp: datetime.datetime
    event_data: dict | None = None


class EventLogUpdate(BaseSchema):
    user_id: int | None = None
    event_type: str | None = None
    event_timestamp: datetime.datetime | None = None
    event_data: dict | None = None


class EventLogFilter(BaseSchema):
    model_config = ConfigDict(extra="forbid")

    user_id: int | None= None
    event_type: str | None= None
    event_timestamp: datetime.datetime | None= None
    event_data: dict | None= None
    created_at: datetime.datetime | None= None
    updated_at: datetime.datetime | None= None
