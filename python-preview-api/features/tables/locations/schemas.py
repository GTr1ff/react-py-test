# ROSETIC:crud-guid






from pydantic import ConfigDict, Field

from core.base_schema import BaseSchema

class LocationResponse(BaseSchema):
    location_id: int
    address_line_1: str | None
    address_line_2: str | None
    city: str | None
    country: str | None
    location_name: str | None
    state: str | None
    zip_code: str | None



class LocationCreate(BaseSchema):
    address_line_1: str | None = None
    address_line_2: str | None = None
    city: str | None = None
    country: str | None = None
    location_name: str | None = None
    state: str | None = None
    zip_code: str | None = None


class LocationUpdate(BaseSchema):
    address_line_1: str | None = None
    address_line_2: str | None = None
    city: str | None = None
    country: str | None = None
    location_name: str | None = None
    state: str | None = None
    zip_code: str | None = None


class LocationFilter(BaseSchema):
    model_config = ConfigDict(extra="forbid")

    address_line_1: str | None= None
    address_line_2: str | None= None
    city: str | None= None
    country: str | None= None
    location_name: str | None= None
    state: str | None= None
    zip_code: str | None= None
