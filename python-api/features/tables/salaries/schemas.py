# ROSETIC:crud-guid




import datetime
from decimal import Decimal
from pydantic import ConfigDict, Field

from core.base_schema import BaseSchema

class SalaryResponse(BaseSchema):
    salary_id: int
    currency: str
    effective_date: datetime.date
    employee_id: int
    salary: Decimal



class SalaryCreate(BaseSchema):
    currency: str
    effective_date: datetime.date
    employee_id: int
    salary: Decimal


class SalaryUpdate(BaseSchema):
    currency: str | None = None
    effective_date: datetime.date | None = None
    employee_id: int | None = None
    salary: Decimal | None = None


class SalaryFilter(BaseSchema):
    model_config = ConfigDict(extra="forbid")

    currency: str | None= None
    effective_date: datetime.date | None= None
    employee_id: int | None= None
    salary: Decimal | None= None
