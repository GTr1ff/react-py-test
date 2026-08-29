import math
from typing import Annotated, Generic, TypeVar
from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict, Field, computed_field, field_validator, model_validator
from pydantic.alias_generators import to_camel, to_snake
from sqlalchemy import Select, asc, desc, inspect
from sqlalchemy.orm import DeclarativeBase

from core.base_schema import BaseSchema

T = TypeVar('T')

class PaginationRequest(BaseSchema):
    """
    A common pagination filter used when querying for paginated lists.
    """

    page: Annotated[int, Field(ge=1)] = 1
    size: Annotated[int, Field(ge=0)] = 25
    sort_by: list[str] = Field(default_factory=list)
    sort_order: list[str] = Field(default_factory=list)
    
    @field_validator('sort_order')
    @classmethod
    def validate_sort_order(cls, directions: list[str]) -> list[str]:
        valid_directions = {'asc', 'desc'}
        for direction in directions:
            if direction.lower() not in valid_directions:
                raise ValueError(f'sort_order must be "asc" or "desc", got "{direction}"')
        return [direction.lower() for direction in directions]  # Normalize to lowercase

    @field_validator('sort_by')
    @classmethod
    def validate_sort_by(cls, sort_fields: list[str]) -> list[str]:
        return [to_snake(field) for field in sort_fields]
    
    @model_validator(mode='after')
    def validate_sort_lengths(self) -> 'PaginationRequest':
        if len(self.sort_order) > len(self.sort_by):
            raise ValueError("sort_order has more entries than sort_by")
        return self

class PaginatedResponse(BaseSchema, Generic[T]):
    items: list[T]
    page: Annotated[int, Field(ge=1)] = 1
    size: Annotated[int, Field(ge=0)] = 0
    total: Annotated[int, Field(ge=0)] = 0
    sort_by: list[str] = Field(default_factory=list)
    sort_order: list[str] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)

    @computed_field()
    def pages(self) -> int:
        if self.size > 0:
            return math.ceil(self.total / self.size)
        return 1

    @field_validator('sort_by')
    @classmethod
    def validate_sort_by(cls, sort_fields: list[str]) -> list[str]:
        return [to_camel(field) for field in sort_fields]

def apply_pagination_filter(query: Select, pagination: PaginationRequest, model: type[DeclarativeBase]) -> Select:
    """Apply pagination and ordering to a SQLAlchemy Select query.
    
    Args:
        query: Base SQLAlchemy Select query
        pagination: Pagination parameters
        model: SQLAlchemy model providing the sortable columns
        
    Returns:
        Modified Select query with ordering and pagination applied
        
    Raises:
        HTTPException: 400 if an invalid sort column is provided, or if sort_order
            has more entries than sort_by.
    """
    sort_by = pagination.sort_by or [getattr(model, "__default_sort__", "id")]
    directions = list(pagination.sort_order)
    
    # Ensure every column has a direction
    directions.extend(["asc"] * (len(sort_by) - len(directions)))

    sortable = {c.key for c in inspect(model).mapper.column_attrs}
    
    # Apply ordering
    for field, direction in zip(sort_by, directions):
        # Validate column exists
        if field not in sortable:
            raise HTTPException(status_code=400, detail=f"Invalid sort column: '{field}'")
        
        # Apply ordering
        column = getattr(model, field)
        order_func = asc if direction == "asc" else desc
        query = query.order_by(order_func(column))
    
    # Apply pagination
    if pagination.size > 0:
        offset_value = (pagination.page - 1) * pagination.size
        query = query.offset(offset_value).limit(pagination.size)
    
    return query

def apply_filters(stmt: Select, filters: BaseModel, model: type[DeclarativeBase]) -> Select:
    """Apply filters to a SQLAlchemy Select query.
    
    Args:
        stmt: Base SQLAlchemy Select query
        filters: Filters to apply
        model: Model to apply filters to
    """
    filterable = {c.key for c in inspect(model).mapper.column_attrs}
    items = filters.model_dump(exclude_unset=True).items()
    for key, value in items:
        if key not in filterable:
            raise ValueError(f"Filter field '{key}' has no column on {model.__name__}")
        
        column = getattr(model, key)
        if isinstance(value, str):
            stmt = stmt.where(column.ilike(f"%{value}%"))
        else:
            stmt = stmt.where(column == value)
    return stmt