from datetime import date, datetime
from decimal import Decimal

from backend.app.schemas.transaction import CategoryRead
from pydantic import BaseModel, Field


class BudgetCategoryCreate(BaseModel):
    category_id: int
    allocated_limit: Decimal = Field(..., gt=Decimal("0.00"))
    alert_threshold_percent: int = Field(default=85, ge=1, le=100)


class BudgetCategoryRead(BaseModel):
    id: int
    budget_id: int
    category_id: int
    allocated_limit: Decimal
    alert_threshold_percent: int
    category: CategoryRead | None = None
    spent_amount: Decimal | None = Decimal("0.00")
    remaining_amount: Decimal | None = Decimal("0.00")
    percentage_used: Decimal | None = Decimal("0.00")

    class Config:
        from_attributes = True


class BudgetCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    period_type: str = Field(default="monthly")
    start_date: date
    end_date: date
    total_budget_limit: Decimal = Field(..., gt=Decimal("0.00"))
    category_allocations: list[BudgetCategoryCreate] | None = None


class BudgetUpdate(BaseModel):
    name: str | None = None
    total_budget_limit: Decimal | None = None
    is_active: bool | None = None


class BudgetRead(BaseModel):
    id: int
    user_id: int
    name: str
    period_type: str
    start_date: date
    end_date: date
    total_budget_limit: Decimal
    is_active: bool
    created_at: datetime
    categories: list[BudgetCategoryRead] = []
    total_spent: Decimal | None = Decimal("0.00")
    total_remaining: Decimal | None = Decimal("0.00")

    class Config:
        from_attributes = True
