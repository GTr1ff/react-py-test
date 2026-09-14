# ROSETIC:crud-guid



import base64
import datetime

from pydantic import ConfigDict, Field
from pydantic import field_serializer
from core.base_schema import BaseSchema

class TaskResponse(BaseSchema):
    task_id: int
    assigned_to: int | None
    attachment: bytes | None
    completed: bool | None
    due_date: datetime.date | None
    notes: str | None
    project_id: int

    @field_serializer('attachment')
    def encode_attachment(self, value: bytes | None, _info):
        if value is None:
            return None
        return base64.b64encode(value).decode('ascii')


class TaskCreate(BaseSchema):
    assigned_to: int | None = None
    attachment: bytes | None = None
    completed: bool | None = None
    due_date: datetime.date | None = None
    notes: str | None = None
    project_id: int


class TaskUpdate(BaseSchema):
    assigned_to: int | None = None
    attachment: bytes | None = None
    completed: bool | None = None
    due_date: datetime.date | None = None
    notes: str | None = None
    project_id: int | None = None


class TaskFilter(BaseSchema):
    model_config = ConfigDict(extra="forbid")

    assigned_to: int | None= None
    attachment: bytes | None= None
    completed: bool | None= None
    due_date: datetime.date | None= None
    notes: str | None= None
    project_id: int | None= None
