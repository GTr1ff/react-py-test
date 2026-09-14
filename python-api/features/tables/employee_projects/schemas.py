# ROSETIC:crud-guid




import datetime

from pydantic import ConfigDict, Field

from core.base_schema import BaseSchema

class EmployeeProjectResponse(BaseSchema):
    employee_project_id: int
    assigned_date: datetime.date | None
    employee_id: int
    project_id: int
    role_name: str | None



class EmployeeProjectCreate(BaseSchema):
    assigned_date: datetime.date | None = None
    employee_id: int
    project_id: int
    role_name: str | None = None


class EmployeeProjectUpdate(BaseSchema):
    assigned_date: datetime.date | None = None
    employee_id: int | None = None
    project_id: int | None = None
    role_name: str | None = None


class EmployeeProjectFilter(BaseSchema):
    model_config = ConfigDict(extra="forbid")

    assigned_date: datetime.date | None= None
    employee_id: int | None= None
    project_id: int | None= None
    role_name: str | None= None
