# ROSETIC:crud-guid




import datetime

from pydantic import ConfigDict, Field

from core.base_schema import BaseSchema

class LeafResponse(BaseSchema):
    leave_id: int
    approval_status: str | None
    approved_by: int | None
    employee_id: int
    end_date: datetime.date
    reason: str | None
    start_date: datetime.date



class LeafCreate(BaseSchema):
    approval_status: str | None = None
    approved_by: int | None = None
    employee_id: int
    end_date: datetime.date
    reason: str | None = None
    start_date: datetime.date


class LeafUpdate(BaseSchema):
    approval_status: str | None = None
    approved_by: int | None = None
    employee_id: int | None = None
    end_date: datetime.date | None = None
    reason: str | None = None
    start_date: datetime.date | None = None


class LeafFilter(BaseSchema):
    model_config = ConfigDict(extra="forbid")

    approval_status: str | None= None
    approved_by: int | None= None
    employee_id: int | None= None
    end_date: datetime.date | None= None
    reason: str | None= None
    start_date: datetime.date | None= None
