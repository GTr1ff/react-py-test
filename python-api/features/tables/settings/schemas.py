# ROSETIC:crud-guid




import datetime

from pydantic import ConfigDict, Field

from core.base_schema import BaseSchema

class SettingResponse(BaseSchema):
    setting_id: int
    setting_key: str
    setting_value: dict | None
    updated_at: datetime.datetime | None



class SettingCreate(BaseSchema):
    setting_key: str
    setting_value: dict | None = None


class SettingUpdate(BaseSchema):
    setting_key: str | None = None
    setting_value: dict | None = None


class SettingFilter(BaseSchema):
    model_config = ConfigDict(extra="forbid")

    setting_key: str | None= None
    setting_value: dict | None= None
    updated_at: datetime.datetime | None= None
