
from backend.app.api.deps import get_current_user, get_db
from backend.app.models.account import Account
from backend.app.models.loan import Loan
from backend.app.models.transaction import Transaction
from backend.app.models.user import User
from backend.app.schemas.user import UserRead
from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/users", response_model=list[UserRead])
async def list_all_users(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Lists registered users (admin directory)."""
    stmt = select(User).order_by(User.id)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/telemetry")
async def get_system_telemetry(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Gathers system operational counts and metrics."""
    users_count = (await db.execute(select(func.count(User.id)))).scalar_one()
    accounts_count = (await db.execute(select(func.count(Account.id)))).scalar_one()
    tx_count = (await db.execute(select(func.count(Transaction.id)))).scalar_one()
    loans_count = (await db.execute(select(func.count(Loan.id)))).scalar_one()

    return {
        "total_users": users_count,
        "total_accounts": accounts_count,
        "total_transactions": tx_count,
        "total_loans": loans_count,
        "database_status": "connected",
        "ai_engine_status": "operational",
    }
