# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c




import datetime

from pydantic import ConfigDict, Field

from core.base_schema import BaseSchema

class AuditLogResponse(BaseSchema):
    id: int
    user_id: int
    change_type: str
    changed_data: dict
    change_timestamp: datetime.datetime
    created_at: datetime.datetime
    updated_at: datetime.datetime



class AuditLogCreate(BaseSchema):
    user_id: int
    change_type: str
    changed_data: dict
    change_timestamp: datetime.datetime


class AuditLogUpdate(BaseSchema):
    user_id: int | None = None
    change_type: str | None = None
    changed_data: dict | None = None
    change_timestamp: datetime.datetime | None = None


class AuditLogFilter(BaseSchema):
    model_config = ConfigDict(extra="forbid")

    user_id: int | None= None
    change_type: str | None= None
    changed_data: dict | None= None
    change_timestamp: datetime.datetime | None= None
    created_at: datetime.datetime | None= None
    updated_at: datetime.datetime | None= None
