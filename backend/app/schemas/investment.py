from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class HoldingTransactionCreate(BaseModel):
    transaction_type: str = Field(..., description="buy, sell, dividend, split")
    quantity: Decimal = Field(..., gt=Decimal("0.00"))
    price_per_unit: Decimal = Field(..., gt=Decimal("0.00"))
    transaction_date: date
    fees: Decimal = Field(default=Decimal("0.00"))
    notes: str | None = None


class HoldingValuationUpdate(BaseModel):
    current_price: Decimal = Field(..., gt=Decimal("0.00"))
    valuation_date: date


class HoldingCreate(BaseModel):
    asset_symbol: str = Field(..., min_length=1, max_length=20)
    asset_name: str = Field(..., min_length=1, max_length=100)
    asset_class: str = Field(..., description="stock, mutual_fund, etf, bond, fixed_deposit, gold, crypto, other")
    quantity: Decimal = Field(..., gt=Decimal("0.00"))
    buy_price: Decimal = Field(..., gt=Decimal("0.00"))
    current_price: Decimal = Field(..., gt=Decimal("0.00"))
    purchase_date: date


class HoldingRead(BaseModel):
    id: int
    investment_id: int
    asset_symbol: str
    asset_name: str
    asset_class: str
    quantity: Decimal
    average_buy_price: Decimal
    current_price: Decimal
    total_invested_value: Decimal
    current_market_value: Decimal
    unrealized_profit_loss: Decimal
    return_percentage: Decimal
    last_valuation_date: date
    created_at: datetime

    class Config:
        from_attributes = True


class InvestmentCreate(BaseModel):
    portfolio_name: str = Field(..., min_length=1, max_length=100)
    description: str | None = None


class InvestmentPortfolioRead(BaseModel):
    id: int
    user_id: int
    portfolio_name: str
    description: str | None = None
    total_invested_amount: Decimal
    total_current_value: Decimal
    total_unrealized_gain_loss: Decimal
    overall_return_percentage: Decimal
    holdings: list[HoldingRead] = []
    asset_allocation: dict = {}

    class Config:
        from_attributes = True
