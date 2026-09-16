"""
Unit tests for the core pagination utilities.
"""
from fastapi import HTTPException
from pydantic import BaseModel, ValidationError
import pytest
import datetime
from decimal import Decimal
import sqlalchemy
from sqlalchemy import Select, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from core.pagination import PaginationRequest, PaginatedResponse, apply_pagination_filter, apply_filters

class MockBase(DeclarativeBase):
    pass

class MockProductFilter(BaseModel):
    name: str | None = None
    category: str | None = None
    product_id: int | None = None
    
# ─── Mock Model for Testing ──────────────────────────────────
class MockProduct(MockBase):
    """Mock Product model for testing pagination utilities."""
    __tablename__ = "products"
    __default_sort__ = "product_id"
    
    product_id: Mapped[int] = mapped_column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(
        sqlalchemy.String,
        nullable=False
    )
    category: Mapped[str] = mapped_column(
        sqlalchemy.String,
        nullable=True
    )
    price: Mapped[Decimal] = mapped_column(
        sqlalchemy.Numeric,
        nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        sqlalchemy.Boolean,
        default=True
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        sqlalchemy.DateTime,
        nullable=False
    )


class TestApplyPaginationFilter:
    """Test cases for apply_pagination_filter utility function."""

    def get_offset(self, pagination: PaginationRequest) -> int:
        return (pagination.page - 1) * pagination.size

    # ─── Pagination tests ──────────────────────────────────
    def test_apply_pagination_filter_base_case(self):
        """Test pagination returns Select type."""
        # Arrange
        pagination = PaginationRequest()
        query = select(MockProduct)
        
        # Act
        result_query = apply_pagination_filter(query, pagination, MockProduct)
        
        # Assert
        assert isinstance(result_query, Select)

    def test_apply_pagination_filter_default_values(self):
        """Test pagination with default values uses model's default sort column."""
        # Arrange
        pagination = PaginationRequest()
        query = select(MockProduct)
        
        # Act
        result_query = apply_pagination_filter(query, pagination, MockProduct)
        
        # Assert
        assert isinstance(result_query, Select)
        
        expected_offset = self.get_offset(pagination)
        assert result_query._offset == expected_offset
        assert result_query._limit == pagination.size
        
        assert "ORDER BY products.product_id ASC" in str(result_query)

    def test_apply_pagination_filter_custom_page_values(self):
        """Test pagination with custom page index and size."""
        # Arrange
        page = 3
        size = 10
        pagination = PaginationRequest(page=page, size=size)

        expected_offset = self.get_offset(pagination)
        
        # Act
        query = select(MockProduct)
        result_query = apply_pagination_filter(query, pagination, MockProduct)
        
        # Assert
        assert result_query._offset == expected_offset
        assert result_query._limit == size

    def test_apply_pagination_filter_custom_ordering_asc(self):
        """Test pagination with custom single column ordering ascending."""
        # Arrange
        page = 2
        size = 20
        pagination = PaginationRequest(
            page=page,
            size=size,
            sort_by=["name"],
            sort_order=["asc"]
        )
        query = select(MockProduct)
        
        # Act
        result_query = apply_pagination_filter(query, pagination, MockProduct)
        
        # Assert
        expected_offset = self.get_offset(pagination)

        assert result_query._offset == expected_offset
        assert result_query._limit == size
        assert "ORDER BY products.name ASC" in str(result_query)

    def test_apply_pagination_filter_custom_ordering_desc(self):
        """Test pagination with custom single column ordering descending."""
        # Arrange
        page = 2
        size = 20
        pagination = PaginationRequest(
            page=page,
            size=size,
            sort_by=["name"],
            sort_order=["desc"]
        )
        query = select(MockProduct)
        
        # Act
        result_query = apply_pagination_filter(query, pagination, MockProduct)
        
        # Assert
        expected_offset = self.get_offset(pagination)

        assert result_query._offset == expected_offset
        assert result_query._limit == size
        assert "ORDER BY products.name DESC" in str(result_query)

    def test_apply_pagination_filter_multiple_columns(self):
        """Test pagination with multiple column ordering."""
        # Arrange
        pagination = PaginationRequest(
            sort_by=["category", "name"],
            sort_order=["asc", "desc"]
        )
        
        # Act
        query = select(MockProduct)
        result_query = apply_pagination_filter(query, pagination, MockProduct)
        
        # Assert
        query_str = str(result_query)        
        assert "ORDER BY products.category ASC" in query_str
        assert "products.name DESC" in query_str

    def test_calculate_pages_with_total_and_size(self):
        """Test pages calculation with valid total and size."""
        pagination = PaginatedResponse(
            items=[],
            page=1,
            size=10,
            total=100
        )
        
        assert pagination.pages == 10

    def test_calculate_pages_with_partial_page(self):
        """Test pages calculation rounds up for partial pages."""
        pagination = PaginatedResponse(
            items=[],
            page=1,
            size=10,
            total=95
        )
        
        assert pagination.pages == 10

    def test_calculate_pages_with_single_item(self):
        """Test pages calculation with single item."""
        pagination = PaginatedResponse(
            items=[],
            page=1,
            size=10,
            total=1
        )
        
        assert pagination.pages == 1

    def test_calculate_pages_with_zero_total(self):
        """Test pages calculation with zero total items."""
        pagination = PaginatedResponse(
            items=[],
            page=1,
            size=10,
            total=0
        )

        assert pagination.pages == 0

    def test_apply_pagination_filter_missing_directions_filled(self):
        """Test that missing directions are filled with the default'asc'."""
        # Arrange
        pagination = PaginationRequest(
            items=[],
            page=1,
            size=10,
            sort_by=["name", "price", "created_at"],
            sort_order=["desc"]
        )
        
        # Act
        query = select(MockProduct)
        result_query = apply_pagination_filter(query, pagination, MockProduct)
        
        # Assert
        query_str = str(result_query)
        assert "products.name DESC" in query_str
        assert "products.price ASC" in query_str
        assert "products.created_at ASC" in query_str

    def test_apply_pagination_filter_zero_size(self):
        """Test pagination with zero size doesn't apply LIMIT/OFFSET."""
        # Arrange
        pagination = PaginationRequest(
            items=[],
            page=1,
            size=0,
            sort_by=["name"]
        )
        
        # Act
        query = select(MockProduct)
        result_query = apply_pagination_filter(query, pagination, MockProduct)
        
        # Assert
        assert result_query._offset is None
        assert result_query._limit is None
        
        query_str = str(result_query)
        assert "ORDER BY products.name ASC" in query_str

    def test_apply_pagination_filter_invalid_column_raises_error(self):
        """Test that invalid column names raise HTTPException 400 with helpful message."""
        # Arrange
        pagination = PaginationRequest(
            sort_by=["invalid_column"],
        )
        query = select(MockProduct)
        
        # Act
        with pytest.raises(HTTPException) as exc_info:
            apply_pagination_filter(query, pagination, MockProduct)
        
        # Assert
        assert exc_info.value.status_code == 400
        assert "Invalid sort column: 'invalid_column'" in exc_info.value.detail

    def test_apply_pagination_filter_mixed_valid_invalid_columns(self):
        """Test that mix of valid and invalid columns fails on first invalid with 400."""
        # Arrange
        pagination = PaginationRequest(
            sort_by=["name", "invalid_column", "price"],
            sort_order=["asc", "desc", "asc"]
        )
        
        # Act
        query = select(MockProduct)
        with pytest.raises(HTTPException) as exc_info:
            apply_pagination_filter(query, pagination, MockProduct)

        # Assert
        assert exc_info.value.status_code == 400
        assert "Invalid sort column: 'invalid_column'" in exc_info.value.detail

    def test_pagination_request_sort_order_longer_than_sort_by_raises(self):
        """Test that more sort_order entries than sort_by fails at schema validation."""
        # Act / Assert
        with pytest.raises(ValidationError, match="sort_order has more entries than sort_by"):
            PaginationRequest(sort_by=["name"], sort_order=["asc", "desc"])

    # ─── Filter tests ──────────────────────────────────
    def test_apply_filters_empty_filters(self):
        """Test apply_filters with empty filters dictionary."""
        # Arrange
        query = select(MockProduct)
        filters = MockProductFilter()
        
        # Act
        result_query = apply_filters(query, filters, MockProduct)
        
        # Assert
        assert isinstance(result_query, Select)
        assert "WHERE" not in str(result_query)

    def test_apply_filters_single_string_filter(self):
        """Test apply_filters with single string filter (uses ILIKE)."""
        # Arrange
        query = select(MockProduct)
        filters = MockProductFilter(name="Software")
        
        # Act
        result_query = apply_filters(query, filters, MockProduct)
        
        # Assert
        assert "WHERE lower(products.name) LIKE" in str(result_query)

    def test_apply_filters_single_integer_filter(self):
        """Test apply_filters with single integer filter (uses exact match)."""
        # Arrange
        query = select(MockProduct)
        filters = MockProductFilter(product_id=123)
        
        # Act
        result_query = apply_filters(query, filters, MockProduct)
        
        # Assert
        assert "WHERE products.product_id =" in str(result_query)

    def test_apply_filters_multiple_filters(self):
        """Test apply_filters with multiple filters."""
        # Arrange
        query = select(MockProduct)
        filters = MockProductFilter(product_id=456, name="Tech", category="Hardware")
        
        # Act
        result_query = apply_filters(query, filters, MockProduct)
        
        # Assert
        query_str = str(result_query)
        assert "products.product_id =" in query_str
        assert "lower(products.name) LIKE" in query_str
        assert "lower(products.category) LIKE" in query_str

    def test_apply_filters_none_values_ignored(self):
        """Test apply_filters ignores None values."""
        # Arrange
        query = select(MockProduct)
        filters = MockProductFilter(name="Valid", product_id=None)
        
        # Act
        result_query = apply_filters(query, filters, MockProduct)
        
        # Assert
        assert isinstance(result_query, Select)
        query_str = str(result_query)
        assert "lower(products.name) LIKE" in query_str
        assert "products.product_id =" not in query_str

    def test_apply_filters_invalid_columns_raises(self) -> None:
        """Filter schema field with no matching column raises ValueError."""
        # Arrange
        class BadFilter(BaseModel):
            name: str | None = None
            nonexistent_col: str | None = None

        filters = BadFilter(nonexistent_col="oops")

        # Act / Assert
        with pytest.raises(ValueError, match="no column on MockProduct"):
            apply_filters(select(MockProduct), filters, MockProduct)

    def test_apply_filters_empty_string_values(self):
        """Test apply_filters with empty string values."""
        # Arrange
        query = select(MockProduct)
        filters = MockProductFilter(name="", category=" ")
        
        # Act
        result_query = apply_filters(query, filters, MockProduct)
        
        # Assert
        assert isinstance(result_query, Select)
        query_str = str(result_query)
        assert "lower(products.name) like" in query_str.lower()
        assert "lower(products.category) like" in query_str.lower()