# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c




import datetime

from pydantic import ConfigDict, Field

from core.base_schema import BaseSchema

class UserResponse(BaseSchema):
    id: int
    username: str
    email: str
    hashed_password: str
    is_active: bool
    last_login_at: datetime.datetime | None
    created_at: datetime.datetime
    updated_at: datetime.datetime



class UserCreate(BaseSchema):
    username: str
    email: str
    hashed_password: str
    is_active: bool
    last_login_at: datetime.datetime | None = None


class UserUpdate(BaseSchema):
    username: str | None = None
    email: str | None = None
    hashed_password: str | None = None
    is_active: bool | None = None
    last_login_at: datetime.datetime | None = None


class UserFilter(BaseSchema):
    model_config = ConfigDict(extra="forbid")

    username: str | None= None
    email: str | None= None
    hashed_password: str | None= None
    is_active: bool | None= None
    last_login_at: datetime.datetime | None= None
    created_at: datetime.datetime | None= None
    updated_at: datetime.datetime | None= None
