# ROSETIC:crud-guid




import datetime

from pydantic import ConfigDict, Field

from core.base_schema import BaseSchema

class TimeLogResponse(BaseSchema):
    time_log_id: int
    clock_in: datetime.datetime
    clock_out: datetime.datetime | None
    employee_id: int
    location: str | None



class TimeLogCreate(BaseSchema):
    clock_in: datetime.datetime
    clock_out: datetime.datetime | None = None
    employee_id: int
    location: str | None = None


class TimeLogUpdate(BaseSchema):
    clock_in: datetime.datetime | None = None
    clock_out: datetime.datetime | None = None
    employee_id: int | None = None
    location: str | None = None


class TimeLogFilter(BaseSchema):
    model_config = ConfigDict(extra="forbid")

    clock_in: datetime.datetime | None= None
    clock_out: datetime.datetime | None= None
    employee_id: int | None= None
    location: str | None= None
