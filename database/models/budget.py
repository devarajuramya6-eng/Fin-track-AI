from datetime import date
from decimal import Decimal

from backend.app.db.base import Base, TimestampMixin
from sqlalchemy import Boolean, Date, ForeignKey, Integer, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Budget(Base, TimestampMixin):
    __tablename__ = "budgets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    period_type: Mapped[str] = mapped_column(String(20), default="monthly", nullable=False)  # monthly, quarterly, annual, custom
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    total_budget_limit: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="budgets")
    categories: Mapped[list["BudgetCategory"]] = relationship("BudgetCategory", back_populates="budget", cascade="all, delete-orphan")


class BudgetCategory(Base, TimestampMixin):
    __tablename__ = "budget_categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    budget_id: Mapped[int] = mapped_column(Integer, ForeignKey("budgets.id", ondelete="CASCADE"), nullable=False, index=True)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("transaction_categories.id", ondelete="CASCADE"), nullable=False, index=True)
    allocated_limit: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    alert_threshold_percent: Mapped[int] = mapped_column(Integer, default=85, nullable=False)  # alert at 85% utilization

    budget: Mapped["Budget"] = relationship("Budget", back_populates="categories")
    category: Mapped["TransactionCategory"] = relationship("TransactionCategory", back_populates="budget_categories")

    __table_args__ = (
        UniqueConstraint("budget_id", "category_id", name="uq_budget_category"),
    )
