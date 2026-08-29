# ROSETIC:crud-guid



import base64


from pydantic import ConfigDict, Field
from pydantic import field_serializer
from core.base_schema import BaseSchema

class DocumentResponse(BaseSchema):
    document_id: int
    doc_content: bytes | None
    doc_name: str | None
    doc_type: str | None
    employee_id: int

    @field_serializer('doc_content')
    def encode_doc_content(self, value: bytes | None, _info):
        if value is None:
            return None
        return base64.b64encode(value).decode('ascii')


class DocumentCreate(BaseSchema):
    doc_content: bytes | None = None
    doc_name: str | None = None
    doc_type: str | None = None
    employee_id: int


class DocumentUpdate(BaseSchema):
    doc_content: bytes | None = None
    doc_name: str | None = None
    doc_type: str | None = None
    employee_id: int | None = None


class DocumentFilter(BaseSchema):
    model_config = ConfigDict(extra="forbid")

    doc_content: bytes | None= None
    doc_name: str | None= None
    doc_type: str | None= None
    employee_id: int | None= None
