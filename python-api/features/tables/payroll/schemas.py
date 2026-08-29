# ROSETIC:crud-guid




import datetime
from decimal import Decimal
from pydantic import ConfigDict, Field

from core.base_schema import BaseSchema

class PayrollResponse(BaseSchema):
    payroll_id: int
    employee_id: int
    hours_worked: Decimal | None
    pay_period_end: datetime.date
    pay_period_start: datetime.date
    wages: Decimal | None



class PayrollCreate(BaseSchema):
    employee_id: int
    hours_worked: Decimal | None = None
    pay_period_end: datetime.date
    pay_period_start: datetime.date
    wages: Decimal | None = None


class PayrollUpdate(BaseSchema):
    employee_id: int | None = None
    hours_worked: Decimal | None = None
    pay_period_end: datetime.date | None = None
    pay_period_start: datetime.date | None = None
    wages: Decimal | None = None


class PayrollFilter(BaseSchema):
    model_config = ConfigDict(extra="forbid")

    employee_id: int | None= None
    hours_worked: Decimal | None= None
    pay_period_end: datetime.date | None= None
    pay_period_start: datetime.date | None= None
    wages: Decimal | None= None
