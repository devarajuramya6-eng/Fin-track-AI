from datetime import date
from decimal import Decimal

from backend.app.db.base import Base, TimestampMixin
from sqlalchemy import Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Investment(Base, TimestampMixin):
    __tablename__ = "investments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    portfolio_name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="investments")
    holdings: Mapped[list["InvestmentHolding"]] = relationship("InvestmentHolding", back_populates="investment", cascade="all, delete-orphan")


class InvestmentHolding(Base, TimestampMixin):
    __tablename__ = "investment_holdings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    investment_id: Mapped[int] = mapped_column(Integer, ForeignKey("investments.id", ondelete="CASCADE"), nullable=False, index=True)
    asset_symbol: Mapped[str] = mapped_column(String(20), nullable=False)
    asset_name: Mapped[str] = mapped_column(String(100), nullable=False)
    asset_class: Mapped[str] = mapped_column(String(50), nullable=False)  # stock, mutual_fund, etf, bond, fixed_deposit, gold, crypto, other

    quantity: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    average_buy_price: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    current_price: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    total_invested_value: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    current_market_value: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    unrealized_profit_loss: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    return_percentage: Mapped[Decimal] = mapped_column(Numeric(8, 2), nullable=False)
    last_valuation_date: Mapped[date] = mapped_column(Date, nullable=False)

    investment: Mapped["Investment"] = relationship("Investment", back_populates="holdings")
    transactions: Mapped[list["InvestmentTransaction"]] = relationship("InvestmentTransaction", back_populates="holding", cascade="all, delete-orphan")


class InvestmentTransaction(Base, TimestampMixin):
    __tablename__ = "investment_transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    holding_id: Mapped[int] = mapped_column(Integer, ForeignKey("investment_holdings.id", ondelete="CASCADE"), nullable=False, index=True)
    transaction_type: Mapped[str] = mapped_column(String(20), nullable=False)  # buy, sell, dividend, split
    quantity: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    price_per_unit: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    transaction_date: Mapped[date] = mapped_column(Date, nullable=False)
    fees: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0.00, nullable=False)
    notes: Mapped[str | None] = mapped_column(String(255), nullable=True)

    holding: Mapped["InvestmentHolding"] = relationship("InvestmentHolding", back_populates="transactions")
