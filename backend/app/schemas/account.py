from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class AccountBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    account_type: str = Field(..., description="checking, savings, credit_card, cash, investment, loan, other")
    institution_name: str | None = Field(None, max_length=100)
    account_number_mask: str | None = Field(None, max_length=10)
    currency: str = Field(default="USD", max_length=10)
    color: str = Field(default="#3b82f6", max_length=20)


class AccountCreate(AccountBase):
    initial_balance: Decimal = Field(default=Decimal("0.00"))


class AccountUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    institution_name: str | None = None
    account_number_mask: str | None = None
    color: str | None = None
    is_active: bool | None = None


class AccountRead(AccountBase):
    id: int
    user_id: int
    current_balance: Decimal
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
