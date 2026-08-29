# ROSETIC:crud-guid



from __future__ import annotations
import uuid
import sqlalchemy

import datetime
from dataclasses import Field
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base

class DatatypestestModel(Base):

    __tablename__ = "datatypestest"
    __default_sort__ = "keykey"

    keykey: Mapped[int] = mapped_column(
        sqlalchemy.Integer,
        primary_key=True, 
        autoincrement=True
    )

    set_col: Mapped[list | None] = mapped_column(
        sqlalchemy.JSON,
        nullable=True
    )
    boolean_col: Mapped[bool | None] = mapped_column(
        sqlalchemy.Boolean,
        nullable=True
    )
    bytea_col: Mapped[bytes | None] = mapped_column(
        sqlalchemy.LargeBinary,
        nullable=True
    )
    character_col: Mapped[str | None] = mapped_column(
        sqlalchemy.String(10),
        nullable=True
    )
    date_col: Mapped[datetime.date | None] = mapped_column(
        sqlalchemy.Date,
        nullable=True
    )
    numeric_col: Mapped[Decimal | None] = mapped_column(
        sqlalchemy.Numeric(10, 2),
        nullable=True
    )
    double_precision_col: Mapped[float | None] = mapped_column(
        sqlalchemy.Numeric(53),
        nullable=True
    )
    int_array_col: Mapped[list | None] = mapped_column(
        sqlalchemy.JSON,
        nullable=True
    )
    integer_col: Mapped[int | None] = mapped_column(
        sqlalchemy.Integer,
        nullable=True
    )
    real_col: Mapped[float | None] = mapped_column(
        sqlalchemy.Numeric(24),
        nullable=True
    )
    smallint_col: Mapped[int | None] = mapped_column(
        sqlalchemy.Integer,
        nullable=True
    )
    text_array_col: Mapped[list | None] = mapped_column(
        sqlalchemy.JSON,
        nullable=True
    )
    text_col: Mapped[str | None] = mapped_column(
        sqlalchemy.Text,
        nullable=True
    )
    time_col: Mapped[datetime.time | None] = mapped_column(
        sqlalchemy.Time,
        nullable=True
    )
    timestamp_col: Mapped[datetime.datetime | None] = mapped_column(
        sqlalchemy.DateTime,
        nullable=True
    )
    timestamptz_col: Mapped[datetime.datetime | None] = mapped_column(
        sqlalchemy.DateTime(timezone=True),
        nullable=True
    )
    timetz_col: Mapped[datetime.time | None] = mapped_column(
        sqlalchemy.Time(timezone=True),
        nullable=True
    )
    character_varying_col: Mapped[str | None] = mapped_column(
        sqlalchemy.String(100),
        nullable=True
    )
    enum_col: Mapped[str | None] = mapped_column(
        sqlalchemy.Text,
        nullable=True
    )
    ntext_col: Mapped[str | None] = mapped_column(
        sqlalchemy.String(100),
        nullable=True
    )
    tinytext_col: Mapped[str | None] = mapped_column(
        sqlalchemy.Text,
        nullable=True
    )
    mediumtext_col: Mapped[str | None] = mapped_column(
        sqlalchemy.String(100),
        nullable=True
    )
    longtext_col: Mapped[str | None] = mapped_column(
        sqlalchemy.String(100),
        nullable=True
    )
    char_col: Mapped[str | None] = mapped_column(
        sqlalchemy.Text,
        nullable=True
    )
    nchar_col: Mapped[str | None] = mapped_column(
        sqlalchemy.Text,
        nullable=True
    )
    varchar_col: Mapped[str | None] = mapped_column(
        sqlalchemy.String(100),
        nullable=True
    )
    nvarchar_col: Mapped[str | None] = mapped_column(
        sqlalchemy.String(100),
        nullable=True
    )
    xml_col: Mapped[str | None] = mapped_column(
        sqlalchemy.String(100),
        nullable=True
    )
    tinyint_col: Mapped[int | None] = mapped_column(
        sqlalchemy.Integer,
        nullable=True
    )
    mediumint_col: Mapped[int | None] = mapped_column(
        sqlalchemy.Integer,
        nullable=True
    )
    year_col: Mapped[int | None] = mapped_column(
        sqlalchemy.Integer,
        nullable=True
    )
    decimal_col: Mapped[Decimal | None] = mapped_column(
        sqlalchemy.Numeric(4, 2),
        nullable=True
    )
    bigdecimal_col: Mapped[Decimal | None] = mapped_column(
        sqlalchemy.Numeric(4, 2),
        nullable=True
    )
    money_col: Mapped[Decimal | None] = mapped_column(
        sqlalchemy.Numeric(4, 2),
        nullable=True
    )
    smallmoney_col: Mapped[Decimal | None] = mapped_column(
        sqlalchemy.Numeric(4, 2),
        nullable=True
    )
    datetime2_col: Mapped[datetime.datetime | None] = mapped_column(
        sqlalchemy.DateTime,
        nullable=True
    )
    blob_col: Mapped[bytes | None] = mapped_column(
        sqlalchemy.LargeBinary,
        nullable=True
    )
    longblob_col: Mapped[bytes | None] = mapped_column(
        sqlalchemy.LargeBinary,
        nullable=True
    )
    mediumblob_col: Mapped[bytes | None] = mapped_column(
        sqlalchemy.LargeBinary,
        nullable=True
    )
    tinyblob_col: Mapped[bytes | None] = mapped_column(
        sqlalchemy.LargeBinary,
        nullable=True
    )
    binary_col: Mapped[bytes | None] = mapped_column(
        sqlalchemy.LargeBinary,
        nullable=True
    )
    varbinary_col: Mapped[bytes | None] = mapped_column(
        sqlalchemy.LargeBinary,
        nullable=True
    )
    image_col: Mapped[bytes | None] = mapped_column(
        sqlalchemy.LargeBinary,
        nullable=True
    )
    uuid_col: Mapped[uuid.UUID | None] = mapped_column(
        sqlalchemy.Uuid(as_uuid=True),
        nullable=True
    )
    uniqueidentifier_col: Mapped[uuid.UUID | None] = mapped_column(
        sqlalchemy.Uuid(as_uuid=True),
        nullable=True
    )

