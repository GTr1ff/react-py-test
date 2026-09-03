# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c




import datetime

from pydantic import ConfigDict, Field

from core.base_schema import BaseSchema

class SessionResponse(BaseSchema):
    id: int
    user_id: int
    session_token: str
    ip_address: str | None
    user_agent: str | None
    expires_at: datetime.datetime
    created_at: datetime.datetime
    updated_at: datetime.datetime



class SessionCreate(BaseSchema):
    user_id: int
    session_token: str
    ip_address: str | None = None
    user_agent: str | None = None
    expires_at: datetime.datetime


class SessionUpdate(BaseSchema):
    user_id: int | None = None
    session_token: str | None = None
    ip_address: str | None = None
    user_agent: str | None = None
    expires_at: datetime.datetime | None = None


class SessionFilter(BaseSchema):
    model_config = ConfigDict(extra="forbid")

    user_id: int | None= None
    session_token: str | None= None
    ip_address: str | None= None
    user_agent: str | None= None
    expires_at: datetime.datetime | None= None
    created_at: datetime.datetime | None= None
    updated_at: datetime.datetime | None= None
