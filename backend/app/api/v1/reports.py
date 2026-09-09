from datetime import date
from decimal import Decimal

from backend.app.api.deps import get_current_user, get_db
from backend.app.models.account import Account
from backend.app.models.investment import Investment, InvestmentHolding
from backend.app.models.loan import Loan
from backend.app.models.transaction import Transaction, TransactionCategory
from backend.app.models.user import User
from dateutil.relativedelta import relativedelta
from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/dashboard-summary")
async def get_dashboard_summary(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Provides consolidated executive financial metrics for the primary dashboard."""
    today = date.today()
    start_of_month = today.replace(day=1)

    # 1. Total Account Balances (Liquid Assets)
    stmt_acc = select(func.coalesce(func.sum(Account.current_balance), Decimal("0.00"))).where(
        Account.user_id == current_user.id, Account.is_active == True
    )
    total_cash = (await db.execute(stmt_acc)).scalar_one()

    # 2. Total Outstanding Loans (Liabilities)
    stmt_loans = select(func.coalesce(func.sum(Loan.outstanding_balance), Decimal("0.00"))).where(
        Loan.user_id == current_user.id, Loan.is_active == True
    )
    total_debt = (await db.execute(stmt_loans)).scalar_one()

    # 3. Total Investment Value
    stmt_inv = (
        select(func.coalesce(func.sum(InvestmentHolding.current_market_value), Decimal("0.00")))
        .join(Investment)
        .where(Investment.user_id == current_user.id)
    )
    total_investments = (await db.execute(stmt_inv)).scalar_one()

    # 4. Month-to-date Income
    stmt_inc = select(func.coalesce(func.sum(Transaction.amount), Decimal("0.00"))).where(
        Transaction.user_id == current_user.id,
        Transaction.transaction_type == "income",
        Transaction.transaction_date >= start_of_month,
    )
    mtd_income = (await db.execute(stmt_inc)).scalar_one()

    # 5. Month-to-date Expenses
    stmt_exp = select(func.coalesce(func.sum(Transaction.amount), Decimal("0.00"))).where(
        Transaction.user_id == current_user.id,
        Transaction.transaction_type == "expense",
        Transaction.transaction_date >= start_of_month,
    )
    mtd_expense = (await db.execute(stmt_exp)).scalar_one()

    # Net Worth = Liquid Cash + Investments - Debt Liabilities
    net_worth = (total_cash + total_investments) - total_debt

    return {
        "total_cash": total_cash,
        "total_investments": total_investments,
        "total_debt": total_debt,
        "net_worth": net_worth,
        "month_to_date_income": mtd_income,
        "month_to_date_expenses": mtd_expense,
        "net_monthly_savings": max(Decimal("0.00"), mtd_income - mtd_expense),
    }


@router.get("/cash-flow")
async def get_cash_flow_report(
    months: int = Query(6, ge=1, le=24),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Provides historical monthly cash flow breakdown (Income vs Expense vs Net)."""
    today = date.today()
    results = []

    for i in range(months - 1, -1, -1):
        target_month_date = today - relativedelta(months=i)
        month_start = target_month_date.replace(day=1)
        next_month = month_start + relativedelta(months=1)
        month_end = next_month - relativedelta(days=1)

        stmt_inc = select(func.coalesce(func.sum(Transaction.amount), Decimal("0.00"))).where(
            Transaction.user_id == current_user.id,
            Transaction.transaction_type == "income",
            Transaction.transaction_date >= month_start,
            Transaction.transaction_date <= month_end,
        )
        inc = (await db.execute(stmt_inc)).scalar_one()

        stmt_exp = select(func.coalesce(func.sum(Transaction.amount), Decimal("0.00"))).where(
            Transaction.user_id == current_user.id,
            Transaction.transaction_type == "expense",
            Transaction.transaction_date >= month_start,
            Transaction.transaction_date <= month_end,
        )
        exp = (await db.execute(stmt_exp)).scalar_one()

        results.append({
            "period": month_start.strftime("%b %Y"),
            "income": float(inc),
            "expense": float(exp),
            "net": float(inc - exp),
        })

    return results


@router.get("/spending-by-category")
async def get_spending_by_category(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Aggregates current month expenses grouped by category for donut chart visualizations."""
    start_of_month = date.today().replace(day=1)
    stmt = (
        select(TransactionCategory.name, TransactionCategory.color, func.sum(Transaction.amount).label("total"))
        .join(Transaction, Transaction.category_id == TransactionCategory.id)
        .where(
            Transaction.user_id == current_user.id,
            Transaction.transaction_type == "expense",
            Transaction.transaction_date >= start_of_month,
        )
        .group_by(TransactionCategory.name, TransactionCategory.color)
        .order_by(func.sum(Transaction.amount).desc())
    )
    result = await db.execute(stmt)
    rows = result.all()
    return [{"category": r[0], "color": r[1], "amount": float(r[2])} for r in rows]
