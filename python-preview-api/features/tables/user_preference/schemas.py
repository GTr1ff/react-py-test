# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c




import datetime

from pydantic import ConfigDict, Field

from core.base_schema import BaseSchema

class UserPreferenceResponse(BaseSchema):
    id: int
    user_id: int
    theme: str | None
    language: str | None
    notifications_enabled: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime



class UserPreferenceCreate(BaseSchema):
    user_id: int
    theme: str | None = None
    language: str | None = None
    notifications_enabled: bool


class UserPreferenceUpdate(BaseSchema):
    user_id: int | None = None
    theme: str | None = None
    language: str | None = None
    notifications_enabled: bool | None = None


class UserPreferenceFilter(BaseSchema):
    model_config = ConfigDict(extra="forbid")

    user_id: int | None= None
    theme: str | None= None
    language: str | None= None
    notifications_enabled: bool | None= None
    created_at: datetime.datetime | None= None
    updated_at: datetime.datetime | None= None
