from datetime import date
from decimal import Decimal

from backend.app.db.base import Base, TimestampMixin
from sqlalchemy import Boolean, Date, ForeignKey, Index, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


class TransactionCategory(Base, TimestampMixin):
    __tablename__ = "transaction_categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    category_type: Mapped[str] = mapped_column(String(20), nullable=False)  # income, expense, transfer
    icon: Mapped[str | None] = mapped_column(String(50), default="Tag")
    color: Mapped[str | None] = mapped_column(String(20), default="#6b7280")
    parent_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("transaction_categories.id", ondelete="SET NULL"), nullable=True)
    is_system: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    transactions: Mapped[list["Transaction"]] = relationship("Transaction", back_populates="category")
    budget_categories: Mapped[list["BudgetCategory"]] = relationship("BudgetCategory", back_populates="category")


class TransactionTag(Base, TimestampMixin):
    __tablename__ = "transaction_tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    color: Mapped[str] = mapped_column(String(20), default="#3b82f6")

    tag_maps: Mapped[list["TransactionTagMap"]] = relationship("TransactionTagMap", back_populates="tag", cascade="all, delete-orphan")


class TransactionTagMap(Base, TimestampMixin):
    __tablename__ = "transaction_tag_maps"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    transaction_id: Mapped[int] = mapped_column(Integer, ForeignKey("transactions.id", ondelete="CASCADE"), nullable=False, index=True)
    tag_id: Mapped[int] = mapped_column(Integer, ForeignKey("transaction_tags.id", ondelete="CASCADE"), nullable=False, index=True)

    transaction: Mapped["Transaction"] = relationship("Transaction", back_populates="tag_maps")
    tag: Mapped["TransactionTag"] = relationship("TransactionTag", back_populates="tag_maps")


class Transaction(Base, TimestampMixin):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    account_id: Mapped[int] = mapped_column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False, index=True)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("transaction_categories.id", ondelete="RESTRICT"), nullable=False, index=True)

    amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    transaction_type: Mapped[str] = mapped_column(String(20), nullable=False)  # income, expense, transfer
    transaction_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    payee_or_merchant: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    payment_method: Mapped[str] = mapped_column(String(50), default="other", nullable=False)  # card, bank_transfer, cash, check, upi, other
    is_recurring: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    recurring_rule_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_excluded_from_budget: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    reference_number: Mapped[str | None] = mapped_column(String(100), nullable=True)

    account: Mapped["Account"] = relationship("Account", back_populates="transactions")
    category: Mapped["TransactionCategory"] = relationship("TransactionCategory", back_populates="transactions")
    tag_maps: Mapped[list["TransactionTagMap"]] = relationship("TransactionTagMap", back_populates="transaction", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_transactions_user_date", "user_id", "transaction_date"),
        Index("idx_transactions_user_category", "user_id", "category_id"),
    )


class RecurringTransaction(Base, TimestampMixin):
    __tablename__ = "recurring_transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    account_id: Mapped[int] = mapped_column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False, index=True)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("transaction_categories.id", ondelete="RESTRICT"), nullable=False)

    amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    transaction_type: Mapped[str] = mapped_column(String(20), nullable=False)
    payee_or_merchant: Mapped[str] = mapped_column(String(150), nullable=False)
    frequency: Mapped[str] = mapped_column(String(20), nullable=False)  # daily, weekly, biweekly, monthly, quarterly, annually
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    next_occurrence: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    auto_post: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
