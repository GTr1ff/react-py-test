# ROSETIC:crud-guid


import uuid
import base64
import datetime
from decimal import Decimal
from pydantic import ConfigDict, Field
from pydantic import field_serializer
from core.base_schema import BaseSchema

class DatatypestestResponse(BaseSchema):
    keykey: int
    set_col: list[str] | None
    boolean_col: bool | None
    bytea_col: bytes | None
    character_col: str | None
    date_col: datetime.date | None
    numeric_col: Decimal | None
    double_precision_col: float | None
    int_array_col: list[int] | None
    integer_col: int | None
    real_col: float | None
    smallint_col: int | None
    text_array_col: list[str] | None
    text_col: str | None
    time_col: datetime.time | None
    timestamp_col: datetime.datetime | None
    timestamptz_col: datetime.datetime | None
    timetz_col: datetime.time | None
    character_varying_col: str | None
    enum_col: str | None
    ntext_col: str | None
    tinytext_col: str | None
    mediumtext_col: str | None
    longtext_col: str | None
    char_col: str | None
    nchar_col: str | None
    varchar_col: str | None
    nvarchar_col: str | None
    xml_col: str | None
    tinyint_col: int | None
    mediumint_col: int | None
    year_col: int | None
    decimal_col: Decimal | None
    bigdecimal_col: Decimal | None
    money_col: Decimal | None
    smallmoney_col: Decimal | None
    datetime2_col: datetime.datetime | None
    blob_col: bytes | None
    longblob_col: bytes | None
    mediumblob_col: bytes | None
    tinyblob_col: bytes | None
    binary_col: bytes | None
    varbinary_col: bytes | None
    image_col: bytes | None
    uuid_col: uuid.UUID | None
    uniqueidentifier_col: uuid.UUID | None

    @field_serializer('bytea_col')
    def encode_bytea_col(self, value: bytes | None, _info):
        if value is None:
            return None
        return base64.b64encode(value).decode('ascii')
    @field_serializer('blob_col')
    def encode_blob_col(self, value: bytes | None, _info):
        if value is None:
            return None
        return base64.b64encode(value).decode('ascii')
    @field_serializer('longblob_col')
    def encode_longblob_col(self, value: bytes | None, _info):
        if value is None:
            return None
        return base64.b64encode(value).decode('ascii')
    @field_serializer('mediumblob_col')
    def encode_mediumblob_col(self, value: bytes | None, _info):
        if value is None:
            return None
        return base64.b64encode(value).decode('ascii')
    @field_serializer('tinyblob_col')
    def encode_tinyblob_col(self, value: bytes | None, _info):
        if value is None:
            return None
        return base64.b64encode(value).decode('ascii')
    @field_serializer('binary_col')
    def encode_binary_col(self, value: bytes | None, _info):
        if value is None:
            return None
        return base64.b64encode(value).decode('ascii')
    @field_serializer('varbinary_col')
    def encode_varbinary_col(self, value: bytes | None, _info):
        if value is None:
            return None
        return base64.b64encode(value).decode('ascii')
    @field_serializer('image_col')
    def encode_image_col(self, value: bytes | None, _info):
        if value is None:
            return None
        return base64.b64encode(value).decode('ascii')


class DatatypestestCreate(BaseSchema):
    set_col: list[str] | None = None
    boolean_col: bool | None = None
    bytea_col: bytes | None = None
    character_col: str | None = None
    date_col: datetime.date | None = None
    numeric_col: Decimal | None = None
    double_precision_col: float | None = None
    int_array_col: list[int] | None = None
    integer_col: int | None = None
    real_col: float | None = None
    smallint_col: int | None = None
    text_array_col: list[str] | None = None
    text_col: str | None = None
    time_col: datetime.time | None = None
    timestamp_col: datetime.datetime | None = None
    timestamptz_col: datetime.datetime | None = None
    timetz_col: datetime.time | None = None
    character_varying_col: str | None = None
    enum_col: str | None = None
    ntext_col: str | None = None
    tinytext_col: str | None = None
    mediumtext_col: str | None = None
    longtext_col: str | None = None
    char_col: str | None = None
    nchar_col: str | None = None
    varchar_col: str | None = None
    nvarchar_col: str | None = None
    xml_col: str | None = None
    tinyint_col: int | None = None
    mediumint_col: int | None = None
    year_col: int | None = None
    decimal_col: Decimal | None = None
    bigdecimal_col: Decimal | None = None
    money_col: Decimal | None = None
    smallmoney_col: Decimal | None = None
    datetime2_col: datetime.datetime | None = None
    blob_col: bytes | None = None
    longblob_col: bytes | None = None
    mediumblob_col: bytes | None = None
    tinyblob_col: bytes | None = None
    binary_col: bytes | None = None
    varbinary_col: bytes | None = None
    image_col: bytes | None = None
    uuid_col: uuid.UUID | None = None
    uniqueidentifier_col: uuid.UUID | None = None


class DatatypestestUpdate(BaseSchema):
    set_col: list[str] | None = None
    boolean_col: bool | None = None
    bytea_col: bytes | None = None
    character_col: str | None = None
    date_col: datetime.date | None = None
    numeric_col: Decimal | None = None
    double_precision_col: float | None = None
    int_array_col: list[int] | None = None
    integer_col: int | None = None
    real_col: float | None = None
    smallint_col: int | None = None
    text_array_col: list[str] | None = None
    text_col: str | None = None
    time_col: datetime.time | None = None
    timestamp_col: datetime.datetime | None = None
    timestamptz_col: datetime.datetime | None = None
    timetz_col: datetime.time | None = None
    character_varying_col: str | None = None
    enum_col: str | None = None
    ntext_col: str | None = None
    tinytext_col: str | None = None
    mediumtext_col: str | None = None
    longtext_col: str | None = None
    char_col: str | None = None
    nchar_col: str | None = None
    varchar_col: str | None = None
    nvarchar_col: str | None = None
    xml_col: str | None = None
    tinyint_col: int | None = None
    mediumint_col: int | None = None
    year_col: int | None = None
    decimal_col: Decimal | None = None
    bigdecimal_col: Decimal | None = None
    money_col: Decimal | None = None
    smallmoney_col: Decimal | None = None
    datetime2_col: datetime.datetime | None = None
    blob_col: bytes | None = None
    longblob_col: bytes | None = None
    mediumblob_col: bytes | None = None
    tinyblob_col: bytes | None = None
    binary_col: bytes | None = None
    varbinary_col: bytes | None = None
    image_col: bytes | None = None
    uuid_col: uuid.UUID | None = None
    uniqueidentifier_col: uuid.UUID | None = None


class DatatypestestFilter(BaseSchema):
    model_config = ConfigDict(extra="forbid")

    set_col: list[str] | None= None
    boolean_col: bool | None= None
    bytea_col: bytes | None= None
    character_col: str | None= None
    date_col: datetime.date | None= None
    numeric_col: Decimal | None= None
    double_precision_col: float | None= None
    int_array_col: list[int] | None= None
    integer_col: int | None= None
    real_col: float | None= None
    smallint_col: int | None= None
    text_array_col: list[str] | None= None
    text_col: str | None= None
    time_col: datetime.time | None= None
    timestamp_col: datetime.datetime | None= None
    timestamptz_col: datetime.datetime | None= None
    timetz_col: datetime.time | None= None
    character_varying_col: str | None= None
    enum_col: str | None= None
    ntext_col: str | None= None
    tinytext_col: str | None= None
    mediumtext_col: str | None= None
    longtext_col: str | None= None
    char_col: str | None= None
    nchar_col: str | None= None
    varchar_col: str | None= None
    nvarchar_col: str | None= None
    xml_col: str | None= None
    tinyint_col: int | None= None
    mediumint_col: int | None= None
    year_col: int | None= None
    decimal_col: Decimal | None= None
    bigdecimal_col: Decimal | None= None
    money_col: Decimal | None= None
    smallmoney_col: Decimal | None= None
    datetime2_col: datetime.datetime | None= None
    blob_col: bytes | None= None
    longblob_col: bytes | None= None
    mediumblob_col: bytes | None= None
    tinyblob_col: bytes | None= None
    binary_col: bytes | None= None
    varbinary_col: bytes | None= None
    image_col: bytes | None= None
    uuid_col: uuid.UUID | None= None
    uniqueidentifier_col: uuid.UUID | None= None
