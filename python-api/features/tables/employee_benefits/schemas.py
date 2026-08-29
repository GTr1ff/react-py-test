# ROSETIC:crud-guid




import datetime

from pydantic import ConfigDict, Field

from core.base_schema import BaseSchema

class EmployeeBenefitResponse(BaseSchema):
    employee_benefit_id: int
    benefit_id: int
    employee_id: int
    enrollment_date: datetime.date



class EmployeeBenefitCreate(BaseSchema):
    benefit_id: int
    employee_id: int
    enrollment_date: datetime.date


class EmployeeBenefitUpdate(BaseSchema):
    benefit_id: int | None = None
    employee_id: int | None = None
    enrollment_date: datetime.date | None = None


class EmployeeBenefitFilter(BaseSchema):
    model_config = ConfigDict(extra="forbid")

    benefit_id: int | None= None
    employee_id: int | None= None
    enrollment_date: datetime.date | None= None
