from datetime import date
from decimal import Decimal
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.deps import get_db, get_current_user
from backend.app.models.loan import Loan, LoanAmortization, LoanPayment
from backend.app.models.user import User
from backend.app.schemas.loan import (
    LoanCreate,
    LoanRead,
    LoanUpdate,
    AmortizationScheduleItem,
    PrepaymentSimulationRequest,
    PrepaymentSimulationResult,
)
from backend.app.services.loan_service import LoanCalculationService

router = APIRouter()


@router.get("/", response_model=List[LoanRead])
async def list_loans(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Lists all user loans with balances and amortizations."""
    stmt = (
        select(Loan)
        .where(Loan.user_id == current_user.id)
        .options(selectinload(Loan.amortizations))
        .order_by(Loan.id.desc())
    )
    result = await db.execute(stmt)
    loans = result.scalars().all()
    for loan_item in loans:
        loan_item.amortization_schedule = loan_item.amortizations
    return loans


@router.post("/", response_model=LoanRead, status_code=status.HTTP_201_CREATED)
async def create_loan(
    loan_in: LoanCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Calculates EMI, amortizes full schedule, and stores loan liability."""
    emi, total_interest, schedule_items = LoanCalculationService.generate_amortization_schedule(
        principal=loan_in.principal_amount,
        annual_interest_rate=loan_in.annual_interest_rate,
        tenure_months=loan_in.tenure_months,
        start_date=loan_in.start_date,
    )

    loan = Loan(
        user_id=current_user.id,
        loan_name=loan_in.loan_name,
        loan_type=loan_in.loan_type,
        lender_name=loan_in.lender_name,
        principal_amount=loan_in.principal_amount,
        annual_interest_rate=loan_in.annual_interest_rate,
        tenure_months=loan_in.tenure_months,
        start_date=loan_in.start_date,
        calculated_emi=emi,
        total_interest=total_interest,
        total_repayment=loan_in.principal_amount + total_interest,
        outstanding_balance=loan_in.principal_amount,
        is_active=True,
    )
    db.add(loan)
    await db.flush()

    for item in schedule_items:
        db.add(
            LoanAmortization(
                loan_id=loan.id,
                installment_number=item.installment_number,
                due_date=item.due_date,
                beginning_balance=item.beginning_balance,
                emi_amount=item.emi_amount,
                principal_component=item.principal_component,
                interest_component=item.interest_component,
                ending_balance=item.ending_balance,
                is_settled=False,
            )
        )
    await db.flush()

    stmt_reload = (
        select(Loan)
        .where(Loan.id == loan.id)
        .options(selectinload(Loan.amortizations))
    )
    reloaded = (await db.execute(stmt_reload)).scalar_one()
    reloaded.amortization_schedule = reloaded.amortizations
    return reloaded


@router.post("/{loan_id}/simulate-prepayment", response_model=PrepaymentSimulationResult)
async def simulate_loan_prepayment(
    loan_id: int,
    sim_in: PrepaymentSimulationRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Simulates the mathematical interest and tenure savings from a lumpsum prepayment."""
    stmt = select(Loan).where(Loan.id == loan_id, Loan.user_id == current_user.id)
    loan = (await db.execute(stmt)).scalar_one_or_none()
    if not loan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loan not found.")

    result = LoanCalculationService.simulate_prepayment(
        principal=loan.outstanding_balance,
        annual_interest_rate=loan.annual_interest_rate,
        tenure_months=loan.tenure_months,
        extra_amount=sim_in.extra_amount,
        action=sim_in.action,
    )
    return result
