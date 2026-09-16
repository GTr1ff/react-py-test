# ROSETIC:crud-guid




import datetime

from pydantic import ConfigDict, Field

from core.base_schema import BaseSchema

class EmployeeResponse(BaseSchema):
    employee_id: int
    birth_date: datetime.date | None
    created_at: datetime.datetime | None
    department_id: int | None
    email: str | None
    first_name: str
    hire_date: datetime.date
    is_active: bool | None
    last_name: str
    phone: str | None
    updated_at: datetime.datetime | None



class EmployeeCreate(BaseSchema):
    birth_date: datetime.date | None = None
    department_id: int | None = None
    email: str | None = None
    first_name: str
    hire_date: datetime.date
    is_active: bool | None = None
    last_name: str
    phone: str | None = None


class EmployeeUpdate(BaseSchema):
    birth_date: datetime.date | None = None
    department_id: int | None = None
    email: str | None = None
    first_name: str | None = None
    hire_date: datetime.date | None = None
    is_active: bool | None = None
    last_name: str | None = None
    phone: str | None = None


class EmployeeFilter(BaseSchema):
    model_config = ConfigDict(extra="forbid")

    birth_date: datetime.date | None= None
    created_at: datetime.datetime | None= None
    department_id: int | None= None
    email: str | None= None
    first_name: str | None= None
    hire_date: datetime.date | None= None
    is_active: bool | None= None
    last_name: str | None= None
    phone: str | None= None
    updated_at: datetime.datetime | None= None
