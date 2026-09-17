# ROSETIC:17d9b513-4ff0-45ef-a308-5754c503176c




import datetime

from pydantic import ConfigDict, Field

from core.base_schema import BaseSchema

class ConsentResponse(BaseSchema):
    id: int
    user_id: int
    consent_type: str
    consent_given_at: datetime.datetime
    consent_revoked_at: datetime.datetime | None
    created_at: datetime.datetime
    updated_at: datetime.datetime



class ConsentCreate(BaseSchema):
    user_id: int
    consent_type: str
    consent_given_at: datetime.datetime
    consent_revoked_at: datetime.datetime | None = None


class ConsentUpdate(BaseSchema):
    user_id: int | None = None
    consent_type: str | None = None
    consent_given_at: datetime.datetime | None = None
    consent_revoked_at: datetime.datetime | None = None


class ConsentFilter(BaseSchema):
    model_config = ConfigDict(extra="forbid")

    user_id: int | None= None
    consent_type: str | None= None
    consent_given_at: datetime.datetime | None= None
    consent_revoked_at: datetime.datetime | None= None
    created_at: datetime.datetime | None= None
    updated_at: datetime.datetime | None= None
