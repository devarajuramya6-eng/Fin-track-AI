from datetime import date
from decimal import Decimal

from ai.forecasting.engine import ForecastingEngine
from backend.app.api.deps import get_current_user, get_db
from backend.app.models.transaction import Transaction
from backend.app.models.user import User
from backend.app.schemas.analytics import ForecastResponse
from dateutil.relativedelta import relativedelta
from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/cashflow", response_model=ForecastResponse)
async def forecast_monthly_expenses(
    periods: int = Query(3, ge=1, le=12),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Generates local predictive trend forecast for monthly expense commitments."""
    today = date.today()
    monthly_historical = []

    for i in range(5, -1, -1):
        m_start = (today - relativedelta(months=i)).replace(day=1)
        m_end = (m_start + relativedelta(months=1)) - relativedelta(days=1)

        stmt = select(func.coalesce(func.sum(Transaction.amount), Decimal("0.00"))).where(
            Transaction.user_id == current_user.id,
            Transaction.transaction_type == "expense",
            Transaction.transaction_date >= m_start,
            Transaction.transaction_date <= m_end,
        )
        spent = (await db.execute(stmt)).scalar_one()
        monthly_historical.append(spent if spent > 0 else Decimal("2100.00"))

    forecast_data = ForecastingEngine.forecast_linear_trend(
        historical_monthly_data=monthly_historical,
        start_date=today,
        periods_ahead=periods,
        metric_name="monthly_expenses",
    )
    return forecast_data
