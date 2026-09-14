# ROSETIC:crud-guid




import datetime

from pydantic import ConfigDict, Field

from core.base_schema import BaseSchema

class HolidayCalendarResponse(BaseSchema):
    holiday_id: int
    holiday_date: datetime.date
    holiday_name: str
    is_national: bool | None



class HolidayCalendarCreate(BaseSchema):
    holiday_date: datetime.date
    holiday_name: str
    is_national: bool | None = None


class HolidayCalendarUpdate(BaseSchema):
    holiday_date: datetime.date | None = None
    holiday_name: str | None = None
    is_national: bool | None = None


class HolidayCalendarFilter(BaseSchema):
    model_config = ConfigDict(extra="forbid")

    holiday_date: datetime.date | None= None
    holiday_name: str | None= None
    is_national: bool | None= None
