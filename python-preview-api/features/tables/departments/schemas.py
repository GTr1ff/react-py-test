# ROSETIC:crud-guid




import datetime
from decimal import Decimal
from pydantic import ConfigDict, Field

from core.base_schema import BaseSchema

class DepartmentResponse(BaseSchema):
    department_id: int
    budget: Decimal | None
    created_at: datetime.datetime | None
    department_name: str
    location: str | None
    manager_id: int | None
    updated_at: datetime.datetime | None



class DepartmentCreate(BaseSchema):
    budget: Decimal | None = None
    department_name: str
    location: str | None = None
    manager_id: int | None = None


class DepartmentUpdate(BaseSchema):
    budget: Decimal | None = None
    department_name: str | None = None
    location: str | None = None
    manager_id: int | None = None


class DepartmentFilter(BaseSchema):
    model_config = ConfigDict(extra="forbid")

    budget: Decimal | None= None
    created_at: datetime.datetime | None= None
    department_name: str | None= None
    location: str | None= None
    manager_id: int | None= None
    updated_at: datetime.datetime | None= None
