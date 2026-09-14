# ROSETIC:crud-guid




import datetime

from pydantic import ConfigDict, Field

from core.base_schema import BaseSchema

class MemoResponse(BaseSchema):
    memo_id: int
    cc_employees: list[int] | None
    created_at: datetime.datetime | None
    message: str



class MemoCreate(BaseSchema):
    cc_employees: list[int] | None = None
    message: str


class MemoUpdate(BaseSchema):
    cc_employees: list[int] | None = None
    message: str | None = None


class MemoFilter(BaseSchema):
    model_config = ConfigDict(extra="forbid")

    cc_employees: list[int] | None= None
    created_at: datetime.datetime | None= None
    message: str | None= None
