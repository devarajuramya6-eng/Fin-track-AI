from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class LoanPaymentCreate(BaseModel):
    payment_date: date
    amount: Decimal = Field(..., gt=Decimal("0.00"))
    is_prepayment: bool = False
    notes: str | None = None


class LoanPaymentRead(BaseModel):
    id: int
    loan_id: int
    payment_date: date
    amount: Decimal
    principal_portion: Decimal
    interest_portion: Decimal
    is_prepayment: bool
    notes: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True


class AmortizationScheduleItem(BaseModel):
    installment_number: int
    due_date: date
    beginning_balance: Decimal
    emi_amount: Decimal
    principal_component: Decimal
    interest_component: Decimal
    ending_balance: Decimal
    is_settled: bool

    class Config:
        from_attributes = True


class LoanCreate(BaseModel):
    loan_name: str = Field(..., min_length=1, max_length=100)
    loan_type: str = Field(..., description="personal, home, auto, education, custom")
    lender_name: str = Field(..., min_length=1, max_length=100)
    principal_amount: Decimal = Field(..., gt=Decimal("0.00"))
    annual_interest_rate: Decimal = Field(..., gt=Decimal("0.00"), description="Annual percentage rate, e.g. 8.5")
    tenure_months: int = Field(..., gt=0, le=480)
    start_date: date


class LoanUpdate(BaseModel):
    loan_name: str | None = None
    is_active: bool | None = None


class LoanRead(BaseModel):
    id: int
    user_id: int
    loan_name: str
    loan_type: str
    lender_name: str
    principal_amount: Decimal
    annual_interest_rate: Decimal
    tenure_months: int
    start_date: date
    calculated_emi: Decimal
    total_interest: Decimal
    total_repayment: Decimal
    outstanding_balance: Decimal
    is_active: bool
    created_at: datetime
    amortization_schedule: list[AmortizationScheduleItem] | None = []

    class Config:
        from_attributes = True


class PrepaymentSimulationRequest(BaseModel):
    extra_amount: Decimal = Field(..., gt=Decimal("0.00"))
    action: str = Field(default="reduce_tenure", description="'reduce_tenure' or 'reduce_emi'")


class PrepaymentSimulationResult(BaseModel):
    original_tenure_months: int
    new_tenure_months: int
    months_saved: int
    original_total_interest: Decimal
    new_total_interest: Decimal
    interest_savings: Decimal
    new_emi: Decimal
