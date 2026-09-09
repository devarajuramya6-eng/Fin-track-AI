from datetime import date
from decimal import Decimal
from typing import Optional

from backend.app.api.deps import get_current_user, get_db
from backend.app.models.budget import Budget, BudgetCategory
from backend.app.models.transaction import Transaction
from backend.app.models.user import User
from backend.app.schemas.budget import (
    BudgetCreate,
    BudgetRead,
)
from fastapi import APIRouter, Depends, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

router = APIRouter()


@router.get("/current", response_model=Optional[BudgetRead])
async def get_current_budget(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Retrieves the active budget for current period with real-time spend calculations."""
    today = date.today()
    stmt = (
        select(Budget)
        .where(
            Budget.user_id == current_user.id,
            Budget.is_active == True,
            Budget.start_date <= today,
            Budget.end_date >= today,
        )
        .options(selectinload(Budget.categories).selectinload(BudgetCategory.category))
    )
    budget = (await db.execute(stmt)).scalar_one_or_none()
    if not budget:
        return None

    # Calculate real-time spend per category within budget period
    total_spent = Decimal("0.00")
    for b_cat in budget.categories:
        tx_stmt = select(func.coalesce(func.sum(Transaction.amount), Decimal("0.00"))).where(
            Transaction.user_id == current_user.id,
            Transaction.category_id == b_cat.category_id,
            Transaction.transaction_type == "expense",
            Transaction.is_excluded_from_budget == False,
            Transaction.transaction_date >= budget.start_date,
            Transaction.transaction_date <= budget.end_date,
        )
        spent = (await db.execute(tx_stmt)).scalar_one()
        b_cat.spent_amount = spent
        b_cat.remaining_amount = max(Decimal("0.00"), b_cat.allocated_limit - spent)
        b_cat.percentage_used = (spent / b_cat.allocated_limit * Decimal("100")) if b_cat.allocated_limit > 0 else Decimal("0.00")
        total_spent += spent

    budget.total_spent = total_spent
    budget.total_remaining = max(Decimal("0.00"), budget.total_budget_limit - total_spent)
    return budget


@router.post("/", response_model=BudgetRead, status_code=status.HTTP_201_CREATED)
async def create_budget(
    budget_in: BudgetCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Configures a new budget and category allocations."""
    budget = Budget(
        user_id=current_user.id,
        name=budget_in.name,
        period_type=budget_in.period_type,
        start_date=budget_in.start_date,
        end_date=budget_in.end_date,
        total_budget_limit=budget_in.total_budget_limit,
        is_active=True,
    )
    db.add(budget)
    await db.flush()

    if budget_in.category_allocations:
        for cat_alloc in budget_in.category_allocations:
            b_cat = BudgetCategory(
                budget_id=budget.id,
                category_id=cat_alloc.category_id,
                allocated_limit=cat_alloc.allocated_limit,
                alert_threshold_percent=cat_alloc.alert_threshold_percent,
            )
            db.add(b_cat)
        await db.flush()

    stmt_reload = (
        select(Budget)
        .where(Budget.id == budget.id)
        .options(selectinload(Budget.categories).selectinload(BudgetCategory.category))
    )
    reloaded = (await db.execute(stmt_reload)).scalar_one()
    reloaded.total_spent = Decimal("0.00")
    reloaded.total_remaining = reloaded.total_budget_limit
    return reloaded
