# ROSETIC:crud-guid




import datetime

from pydantic import ConfigDict, Field

from core.base_schema import BaseSchema

class PerformanceReviewResponse(BaseSchema):
    review_id: int
    details: dict | None
    employee_id: int
    review_date: datetime.date



class PerformanceReviewCreate(BaseSchema):
    details: dict | None = None
    employee_id: int
    review_date: datetime.date


class PerformanceReviewUpdate(BaseSchema):
    details: dict | None = None
    employee_id: int | None = None
    review_date: datetime.date | None = None


class PerformanceReviewFilter(BaseSchema):
    model_config = ConfigDict(extra="forbid")

    details: dict | None= None
    employee_id: int | None= None
    review_date: datetime.date | None= None
