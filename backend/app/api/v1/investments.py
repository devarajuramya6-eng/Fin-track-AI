from decimal import Decimal

from backend.app.api.deps import get_current_user, get_db
from backend.app.models.investment import Investment, InvestmentHolding, InvestmentTransaction
from backend.app.models.user import User
from backend.app.schemas.investment import (
    HoldingCreate,
    HoldingRead,
    HoldingValuationUpdate,
    InvestmentPortfolioRead,
)
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

router = APIRouter()


@router.get("/portfolio", response_model=InvestmentPortfolioRead)
async def get_investment_portfolio(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Fetches user investment portfolio, asset class allocation, and total performance."""
    stmt = (
        select(Investment)
        .where(Investment.user_id == current_user.id)
        .options(selectinload(Investment.holdings))
    )
    portfolio = (await db.execute(stmt)).scalar_one_or_none()

    if not portfolio:
        # Create default primary portfolio
        portfolio = Investment(
            user_id=current_user.id,
            portfolio_name="Primary Wealth Portfolio",
            description="Consolidated portfolio of stocks, funds, and fixed assets.",
        )
        db.add(portfolio)
        await db.flush()
        stmt_reload = select(Investment).where(Investment.id == portfolio.id).options(selectinload(Investment.holdings))
        portfolio = (await db.execute(stmt_reload)).scalar_one()

    total_invested = Decimal("0.00")
    total_value = Decimal("0.00")
    allocation = {}

    for h in portfolio.holdings:
        total_invested += h.total_invested_value
        total_value += h.current_market_value
        asset_cls = h.asset_class.title().replace("_", " ")
        allocation[asset_cls] = allocation.get(asset_cls, Decimal("0.00")) + h.current_market_value

    unrealized = total_value - total_invested
    ret_pct = ((unrealized / total_invested) * Decimal("100")) if total_invested > 0 else Decimal("0.00")

    # Format asset allocation breakdown percentages
    alloc_breakdown = {}
    for k, v in allocation.items():
        alloc_breakdown[k] = float((v / total_value * Decimal("100")).quantize(Decimal("0.1"))) if total_value > 0 else 0.0

    return InvestmentPortfolioRead(
        id=portfolio.id,
        user_id=portfolio.user_id,
        portfolio_name=portfolio.portfolio_name,
        description=portfolio.description,
        total_invested_amount=total_invested,
        total_current_value=total_value,
        total_unrealized_gain_loss=unrealized,
        overall_return_percentage=ret_pct.quantize(Decimal("0.01")),
        holdings=portfolio.holdings,
        asset_allocation=alloc_breakdown,
    )


@router.post("/holdings", response_model=HoldingRead, status_code=status.HTTP_201_CREATED)
async def add_holding(
    holding_in: HoldingCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Adds a new asset holding (Stock, Fund, ETF, Gold, FD, etc.) to portfolio."""
    stmt = select(Investment).where(Investment.user_id == current_user.id)
    portfolio = (await db.execute(stmt)).scalar_one_or_none()
    if not portfolio:
        portfolio = Investment(user_id=current_user.id, portfolio_name="Primary Portfolio")
        db.add(portfolio)
        await db.flush()

    invested_val = (holding_in.quantity * holding_in.buy_price).quantize(Decimal("0.01"))
    market_val = (holding_in.quantity * holding_in.current_price).quantize(Decimal("0.01"))
    pnl = market_val - invested_val
    ret_pct = ((pnl / invested_val) * Decimal("100")).quantize(Decimal("0.01")) if invested_val > 0 else Decimal("0.00")

    holding = InvestmentHolding(
        investment_id=portfolio.id,
        asset_symbol=holding_in.asset_symbol.upper(),
        asset_name=holding_in.asset_name,
        asset_class=holding_in.asset_class,
        quantity=holding_in.quantity,
        average_buy_price=holding_in.buy_price,
        current_price=holding_in.current_price,
        total_invested_value=invested_val,
        current_market_value=market_val,
        unrealized_profit_loss=pnl,
        return_percentage=ret_pct,
        last_valuation_date=holding_in.purchase_date,
    )
    db.add(holding)
    await db.flush()

    # Record buy transaction
    tx = InvestmentTransaction(
        holding_id=holding.id,
        transaction_type="buy",
        quantity=holding_in.quantity,
        price_per_unit=holding_in.buy_price,
        total_amount=invested_val,
        transaction_date=holding_in.purchase_date,
    )
    db.add(tx)
    await db.flush()

    return holding


@router.put("/holdings/{holding_id}/valuation", response_model=HoldingRead)
async def update_holding_valuation(
    holding_id: int,
    val_in: HoldingValuationUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Manually updates current market price for an asset."""
    stmt = (
        select(InvestmentHolding)
        .join(Investment)
        .where(InvestmentHolding.id == holding_id, Investment.user_id == current_user.id)
    )
    holding = (await db.execute(stmt)).scalar_one_or_none()
    if not holding:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Holding not found.")

    holding.current_price = val_in.current_price
    holding.current_market_value = (holding.quantity * val_in.current_price).quantize(Decimal("0.01"))
    holding.unrealized_profit_loss = holding.current_market_value - holding.total_invested_value
    holding.return_percentage = (
        ((holding.unrealized_profit_loss / holding.total_invested_value) * Decimal("100")).quantize(Decimal("0.01"))
        if holding.total_invested_value > 0
        else Decimal("0.00")
    )
    holding.last_valuation_date = val_in.valuation_date
    await db.flush()
    return holding
