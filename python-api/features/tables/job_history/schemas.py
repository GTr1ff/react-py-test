# ROSETIC:crud-guid




import datetime

from pydantic import ConfigDict, Field

from core.base_schema import BaseSchema

class JobHistoryResponse(BaseSchema):
    job_history_id: int
    employee_id: int
    end_date: datetime.date | None
    role_id: int
    start_date: datetime.date



class JobHistoryCreate(BaseSchema):
    employee_id: int
    end_date: datetime.date | None = None
    role_id: int
    start_date: datetime.date


class JobHistoryUpdate(BaseSchema):
    employee_id: int | None = None
    end_date: datetime.date | None = None
    role_id: int | None = None
    start_date: datetime.date | None = None


class JobHistoryFilter(BaseSchema):
    model_config = ConfigDict(extra="forbid")

    employee_id: int | None= None
    end_date: datetime.date | None= None
    role_id: int | None= None
    start_date: datetime.date | None= None
