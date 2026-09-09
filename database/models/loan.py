from datetime import date
from decimal import Decimal

from backend.app.db.base import Base, TimestampMixin
from sqlalchemy import Boolean, Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Loan(Base, TimestampMixin):
    __tablename__ = "loans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    loan_name: Mapped[str] = mapped_column(String(100), nullable=False)
    loan_type: Mapped[str] = mapped_column(String(50), nullable=False)  # personal, home, auto, education, custom
    lender_name: Mapped[str] = mapped_column(String(100), nullable=False)

    principal_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    annual_interest_rate: Mapped[Decimal] = mapped_column(Numeric(6, 3), nullable=False)  # e.g. 7.500%
    tenure_months: Mapped[int] = mapped_column(Integer, nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)

    calculated_emi: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    total_interest: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    total_repayment: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    outstanding_balance: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="loans")
    payments: Mapped[list["LoanPayment"]] = relationship("LoanPayment", back_populates="loan", cascade="all, delete-orphan")
    amortizations: Mapped[list["LoanAmortization"]] = relationship("LoanAmortization", back_populates="loan", cascade="all, delete-orphan")


class LoanPayment(Base, TimestampMixin):
    __tablename__ = "loan_payments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    loan_id: Mapped[int] = mapped_column(Integer, ForeignKey("loans.id", ondelete="CASCADE"), nullable=False, index=True)
    payment_date: Mapped[date] = mapped_column(Date, nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    principal_portion: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    interest_portion: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    is_prepayment: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    notes: Mapped[str | None] = mapped_column(String(255), nullable=True)

    loan: Mapped["Loan"] = relationship("Loan", back_populates="payments")


class LoanAmortization(Base, TimestampMixin):
    __tablename__ = "loan_amortizations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    loan_id: Mapped[int] = mapped_column(Integer, ForeignKey("loans.id", ondelete="CASCADE"), nullable=False, index=True)
    installment_number: Mapped[int] = mapped_column(Integer, nullable=False)
    due_date: Mapped[date] = mapped_column(Date, nullable=False)
    beginning_balance: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    emi_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    principal_component: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    interest_component: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    ending_balance: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    is_settled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    loan: Mapped["Loan"] = relationship("Loan", back_populates="amortizations")
