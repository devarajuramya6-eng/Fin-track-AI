from datetime import date
from decimal import Decimal

from ai.recommendations.engine import RecommendationEngine
from backend.app.api.deps import get_current_user, get_db
from backend.app.models.account import Account
from backend.app.models.loan import Loan
from backend.app.models.transaction import Transaction
from backend.app.models.user import User
from backend.app.schemas.analytics import RecommendationRead
from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/", response_model=list[RecommendationRead])
async def list_financial_recommendations(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Generates actionable, explainable financial health recommendations
    based on live balance and transaction metrics.
    """
    start_of_month = date.today().replace(day=1)

    stmt_inc = select(func.coalesce(func.sum(Transaction.amount), Decimal("0.00"))).where(
        Transaction.user_id == current_user.id,
        Transaction.transaction_type == "income",
        Transaction.transaction_date >= start_of_month,
    )
    income = (await db.execute(stmt_inc)).scalar_one()
    if income <= 0:
        income = Decimal("4500.00")

    stmt_exp = select(func.coalesce(func.sum(Transaction.amount), Decimal("0.00"))).where(
        Transaction.user_id == current_user.id,
        Transaction.transaction_type == "expense",
        Transaction.transaction_date >= start_of_month,
    )
    expenses = (await db.execute(stmt_exp)).scalar_one()

    stmt_cash = select(func.coalesce(func.sum(Account.current_balance), Decimal("0.00"))).where(
        Account.user_id == current_user.id,
        Account.account_type.in_(["checking", "savings", "cash"]),
        Account.is_active == True,
    )
    liquid_savings = (await db.execute(stmt_cash)).scalar_one()

    stmt_debt = select(func.coalesce(func.sum(Loan.calculated_emi), Decimal("0.00"))).where(
        Loan.user_id == current_user.id, Loan.is_active == True
    )
    debt = (await db.execute(stmt_debt)).scalar_one()

    raw_recs = RecommendationEngine.generate_recommendations(
        monthly_income=income,
        monthly_expenses=expenses,
        liquid_savings=liquid_savings,
        monthly_debt=debt,
    )

    out = []
    for idx, r in enumerate(raw_recs, start=1):
        out.append(
            RecommendationRead(
                id=idx,
                category=r["category"],
                title=r["title"],
                summary=r["summary"],
                impact_estimate=r.get("impact_estimate"),
                priority=r["priority"],
                is_applied=False,
            )
        )
    return out
