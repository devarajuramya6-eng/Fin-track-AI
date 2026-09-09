from datetime import date
from decimal import Decimal

from backend.app.db.base import Base, TimestampMixin
from sqlalchemy import Boolean, Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Account(Base, TimestampMixin):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    account_type: Mapped[str] = mapped_column(String(50), nullable=False)  # checking, savings, credit_card, cash, investment, loan, other
    institution_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    account_number_mask: Mapped[str | None] = mapped_column(String(10), nullable=True)
    currency: Mapped[str] = mapped_column(String(10), default="USD", nullable=False)
    current_balance: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0.00, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    color: Mapped[str] = mapped_column(String(20), default="#3b82f6", nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="accounts")
    transactions: Mapped[list["Transaction"]] = relationship("Transaction", back_populates="account", cascade="all, delete-orphan")
    snapshots: Mapped[list["AccountSnapshot"]] = relationship("AccountSnapshot", back_populates="account", cascade="all, delete-orphan")


class AccountSnapshot(Base, TimestampMixin):
    __tablename__ = "account_snapshots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    account_id: Mapped[int] = mapped_column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False, index=True)
    snapshot_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    balance: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)

    account: Mapped["Account"] = relationship("Account", back_populates="snapshots")
