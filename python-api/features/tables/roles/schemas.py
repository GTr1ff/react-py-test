# ROSETIC:crud-guid






from pydantic import ConfigDict, Field

from core.base_schema import BaseSchema

class RoleResponse(BaseSchema):
    role_id: int
    privileges: list[str] | None
    role_name: str



class RoleCreate(BaseSchema):
    privileges: list[str] | None = None
    role_name: str


class RoleUpdate(BaseSchema):
    privileges: list[str] | None = None
    role_name: str | None = None


class RoleFilter(BaseSchema):
    model_config = ConfigDict(extra="forbid")

    privileges: list[str] | None= None
    role_name: str | None= None
