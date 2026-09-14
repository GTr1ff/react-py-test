# ROSETIC:crud-guid




import datetime
from decimal import Decimal
from pydantic import ConfigDict, Field

from core.base_schema import BaseSchema

class BenefitResponse(BaseSchema):
    benefit_id: int
    benefit_name: str
    benefit_type: str | None
    coverage_details: dict | None
    created_at: datetime.datetime | None
    monthly_cost: Decimal | None



class BenefitCreate(BaseSchema):
    benefit_name: str
    benefit_type: str | None = None
    coverage_details: dict | None = None
    monthly_cost: Decimal | None = None


class BenefitUpdate(BaseSchema):
    benefit_name: str | None = None
    benefit_type: str | None = None
    coverage_details: dict | None = None
    monthly_cost: Decimal | None = None


class BenefitFilter(BaseSchema):
    model_config = ConfigDict(extra="forbid")

    benefit_name: str | None= None
    benefit_type: str | None= None
    coverage_details: dict | None= None
    created_at: datetime.datetime | None= None
    monthly_cost: Decimal | None= None
