from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class CategoryRead(BaseModel):
    id: int
    name: str
    category_type: str
    icon: str | None = "Tag"
    color: str | None = "#6b7280"
    parent_id: int | None = None
    is_system: bool

    class Config:
        from_attributes = True


class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    category_type: str = Field(..., description="income, expense, transfer")
    icon: str | None = "Tag"
    color: str | None = "#6b7280"
    parent_id: int | None = None


class TagRead(BaseModel):
    id: int
    name: str
    color: str

    class Config:
        from_attributes = True


class TagCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    color: str = Field(default="#3b82f6")


class TransactionBase(BaseModel):
    account_id: int
    category_id: int
    amount: Decimal = Field(..., gt=Decimal("0.00"))
    transaction_type: str = Field(..., description="income, expense, transfer")
    transaction_date: date
    payee_or_merchant: str = Field(..., min_length=1, max_length=150)
    description: str | None = None
    notes: str | None = None
    payment_method: str = Field(default="other")
    is_excluded_from_budget: bool = False
    reference_number: str | None = None


class TransactionCreate(TransactionBase):
    tag_ids: list[int] | None = None


class TransactionUpdate(BaseModel):
    account_id: int | None = None
    category_id: int | None = None
    amount: Decimal | None = Field(None, gt=Decimal("0.00"))
    transaction_type: str | None = None
    transaction_date: date | None = None
    payee_or_merchant: str | None = None
    description: str | None = None
    notes: str | None = None
    payment_method: str | None = None
    is_excluded_from_budget: bool | None = None
    reference_number: str | None = None
    tag_ids: list[int] | None = None


class TransactionRead(TransactionBase):
    id: int
    user_id: int
    is_recurring: bool
    created_at: datetime
    category: CategoryRead | None = None

    class Config:
        from_attributes = True


class CSVImportResult(BaseModel):
    total_processed: int
    imported_count: int
    duplicates_skipped: int
    errors: list[str]
