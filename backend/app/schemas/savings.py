from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class SavingsContributionCreate(BaseModel):
    amount: Decimal = Field(..., gt=Decimal("0.00"))
    contribution_date: date
    notes: str | None = None


class SavingsContributionRead(BaseModel):
    id: int
    goal_id: int
    amount: Decimal
    contribution_date: date
    notes: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True


class SavingsGoalCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    goal_category: str = Field(..., description="emergency_fund, education, travel, vehicle, house, retirement, custom")
    target_amount: Decimal = Field(..., gt=Decimal("0.00"))
    current_amount: Decimal = Field(default=Decimal("0.00"), ge=Decimal("0.00"))
    target_date: date
    color: str = Field(default="#10b981")
    notes: str | None = None


class SavingsGoalUpdate(BaseModel):
    name: str | None = None
    target_amount: Decimal | None = None
    current_amount: Decimal | None = None
    target_date: date | None = None
    is_completed: bool | None = None
    color: str | None = None
    notes: str | None = None


class SavingsGoalRead(BaseModel):
    id: int
    user_id: int
    name: str
    goal_category: str
    target_amount: Decimal
    current_amount: Decimal
    target_date: date
    is_completed: bool
    color: str
    notes: str | None = None
    created_at: datetime
    progress_percentage: Decimal | None = Decimal("0.00")
    required_monthly_savings: Decimal | None = Decimal("0.00")
    contributions: list[SavingsContributionRead] = []

    class Config:
        from_attributes = True
