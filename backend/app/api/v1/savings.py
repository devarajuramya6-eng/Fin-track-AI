from datetime import date
from decimal import Decimal
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.deps import get_db, get_current_user
from backend.app.models.savings import SavingsGoal, SavingsContribution
from backend.app.models.user import User
from backend.app.schemas.savings import (
    SavingsGoalCreate,
    SavingsGoalRead,
    SavingsGoalUpdate,
    SavingsContributionCreate,
    SavingsContributionRead,
)

router = APIRouter()


@router.get("/", response_model=List[SavingsGoalRead])
async def list_savings_goals(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Lists all active and completed savings goals with progress and monthly target formulas."""
    stmt = (
        select(SavingsGoal)
        .where(SavingsGoal.user_id == current_user.id)
        .options(selectinload(SavingsGoal.contributions))
        .order_by(SavingsGoal.id.desc())
    )
    result = await db.execute(stmt)
    goals = result.scalars().all()

    today = date.today()
    for g in goals:
        g.progress_percentage = (
            (g.current_amount / g.target_amount * Decimal("100")) if g.target_amount > 0 else Decimal("0.00")
        )
        remaining_target = max(Decimal("0.00"), g.target_amount - g.current_amount)
        diff_months = (g.target_date.year - today.year) * 12 + (g.target_date.month - today.month)
        if diff_months > 0:
            g.required_monthly_savings = (remaining_target / Decimal(diff_months)).quantize(Decimal("0.01"))
        else:
            g.required_monthly_savings = remaining_target

    return goals


@router.post("/", response_model=SavingsGoalRead, status_code=status.HTTP_201_CREATED)
async def create_savings_goal(
    goal_in: SavingsGoalCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Creates a new savings milestone goal."""
    goal = SavingsGoal(
        user_id=current_user.id,
        name=goal_in.name,
        goal_category=goal_in.goal_category,
        target_amount=goal_in.target_amount,
        current_amount=goal_in.current_amount,
        target_date=goal_in.target_date,
        color=goal_in.color or "#10b981",
        notes=goal_in.notes,
        is_completed=goal_in.current_amount >= goal_in.target_amount,
    )
    db.add(goal)
    await db.flush()

    # Reload with selectinload so relationship serialization works without greenlet errors
    stmt_reload = (
        select(SavingsGoal)
        .where(SavingsGoal.id == goal.id)
        .options(selectinload(SavingsGoal.contributions))
    )
    reloaded = (await db.execute(stmt_reload)).scalar_one()

    today = date.today()
    reloaded.progress_percentage = (
        (reloaded.current_amount / reloaded.target_amount * Decimal("100")) if reloaded.target_amount > 0 else Decimal("0.00")
    )
    diff = (reloaded.target_date.year - today.year) * 12 + (reloaded.target_date.month - today.month)
    reloaded.required_monthly_savings = (
        (max(Decimal("0.00"), reloaded.target_amount - reloaded.current_amount) / Decimal(max(1, diff))).quantize(Decimal("0.01"))
    )
    return reloaded


@router.post("/{goal_id}/contribute", response_model=SavingsContributionRead, status_code=status.HTTP_201_CREATED)
async def add_savings_contribution(
    goal_id: int,
    contrib_in: SavingsContributionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Logs a deposit towards a savings goal and increases current progress."""
    stmt = select(SavingsGoal).where(SavingsGoal.id == goal_id, SavingsGoal.user_id == current_user.id)
    goal = (await db.execute(stmt)).scalar_one_or_none()
    if not goal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found.")

    contrib = SavingsContribution(
        goal_id=goal.id,
        amount=contrib_in.amount,
        contribution_date=contrib_in.contribution_date,
        notes=contrib_in.notes,
    )
    db.add(contrib)
    goal.current_amount += contrib_in.amount
    if goal.current_amount >= goal.target_amount:
        goal.is_completed = True

    await db.flush()
    return contrib
