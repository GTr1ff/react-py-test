# ROSETIC:crud-guid




import datetime
from decimal import Decimal
from pydantic import ConfigDict, Field

from core.base_schema import BaseSchema

class ProjectResponse(BaseSchema):
    project_id: int
    budget: Decimal | None
    created_at: datetime.datetime | None
    end_date: datetime.date | None
    project_name: str
    start_date: datetime.date | None
    status: str
    tags: list[str] | None



class ProjectCreate(BaseSchema):
    budget: Decimal | None = None
    end_date: datetime.date | None = None
    project_name: str
    start_date: datetime.date | None = None
    status: str
    tags: list[str] | None = None


class ProjectUpdate(BaseSchema):
    budget: Decimal | None = None
    end_date: datetime.date | None = None
    project_name: str | None = None
    start_date: datetime.date | None = None
    status: str | None = None
    tags: list[str] | None = None


class ProjectFilter(BaseSchema):
    model_config = ConfigDict(extra="forbid")

    budget: Decimal | None= None
    created_at: datetime.datetime | None= None
    end_date: datetime.date | None= None
    project_name: str | None= None
    start_date: datetime.date | None= None
    status: str | None= None
    tags: list[str] | None= None
