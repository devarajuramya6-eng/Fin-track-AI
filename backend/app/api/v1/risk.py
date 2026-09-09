from datetime import date
from decimal import Decimal

from ai.risk.engine import RiskScoringEngine
from backend.app.api.deps import get_current_user, get_db
from backend.app.models.account import Account
from backend.app.models.loan import Loan
from backend.app.models.transaction import Transaction
from backend.app.models.user import User
from backend.app.schemas.analytics import RiskScoreRead
from dateutil.relativedelta import relativedelta
from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/score", response_model=RiskScoreRead)
async def get_financial_risk_score(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Computes an explainable 0-100 financial risk score and breakdown factors.
    Runs entirely on local statistical and algorithmic engines.
    """
    today = date.today()
    start_of_month = today.replace(day=1)

    # 1. Monthly income
    stmt_inc = select(func.coalesce(func.sum(Transaction.amount), Decimal("0.00"))).where(
        Transaction.user_id == current_user.id,
        Transaction.transaction_type == "income",
        Transaction.transaction_date >= start_of_month,
    )
    monthly_income = (await db.execute(stmt_inc)).scalar_one()
    if monthly_income <= 0:
        monthly_income = Decimal("4200.00")  # Baseline fallback

    # 2. Monthly debt obligations (EMIs)
    stmt_emi = select(func.coalesce(func.sum(Loan.calculated_emi), Decimal("0.00"))).where(
        Loan.user_id == current_user.id, Loan.is_active == True
    )
    monthly_debt = (await db.execute(stmt_emi)).scalar_one()

    # 3. Liquid savings
    stmt_savings = select(func.coalesce(func.sum(Account.current_balance), Decimal("0.00"))).where(
        Account.user_id == current_user.id,
        Account.account_type.in_(["checking", "savings", "cash"]),
        Account.is_active == True,
    )
    liquid_savings = (await db.execute(stmt_savings)).scalar_one()

    # 4. Monthly expenses
    stmt_exp = select(func.coalesce(func.sum(Transaction.amount), Decimal("0.00"))).where(
        Transaction.user_id == current_user.id,
        Transaction.transaction_type == "expense",
        Transaction.transaction_date >= start_of_month,
    )
    monthly_expenses = (await db.execute(stmt_exp)).scalar_one()
    if monthly_expenses <= 0:
        monthly_expenses = Decimal("2100.00")

    # 5. Historical cash flows over past 4 months
    historical_cfs = []
    for i in range(4):
        m_start = (today - relativedelta(months=i)).replace(day=1)
        m_end = (m_start + relativedelta(months=1)) - relativedelta(days=1)

        m_inc = (await db.execute(
            select(func.coalesce(func.sum(Transaction.amount), Decimal("0.00"))).where(
                Transaction.user_id == current_user.id,
                Transaction.transaction_type == "income",
                Transaction.transaction_date >= m_start,
                Transaction.transaction_date <= m_end,
            )
        )).scalar_one()

        m_exp = (await db.execute(
            select(func.coalesce(func.sum(Transaction.amount), Decimal("0.00"))).where(
                Transaction.user_id == current_user.id,
                Transaction.transaction_type == "expense",
                Transaction.transaction_date >= m_start,
                Transaction.transaction_date <= m_end,
            )
        )).scalar_one()

        historical_cfs.append(m_inc - m_exp)

    score_result = RiskScoringEngine.evaluate_risk(
        monthly_income=monthly_income,
        monthly_debt_obligations=monthly_debt,
        liquid_savings=liquid_savings,
        monthly_expenses=monthly_expenses,
        historical_net_cashflows=historical_cfs,
    )

    # Format risk factors with sequential IDs
    factors = []
    for idx, f in enumerate(score_result["risk_factors"], start=1):
        factors.append({
            "id": idx,
            "factor_name": f["factor_name"],
            "severity": f["severity"],
            "impact_points": f["impact_points"],
            "description": f["description"],
            "mitigation_suggestion": f["mitigation_suggestion"],
        })

    return RiskScoreRead(
        overall_health_score=score_result["overall_health_score"],
        risk_score=score_result["risk_score"],
        risk_level=score_result["risk_level"],
        savings_ratio=score_result["savings_ratio"],
        debt_to_income_ratio=score_result["debt_to_income_ratio"],
        emergency_runway_months=score_result["emergency_runway_months"],
        cash_flow_volatility_score=score_result["cash_flow_volatility_score"],
        summary_explanation=score_result["summary_explanation"],
        risk_factors=factors,
    )
