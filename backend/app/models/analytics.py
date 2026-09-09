from datetime import date, datetime
from decimal import Decimal

from backend.app.db.base import Base, TimestampMixin
from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


class FinancialScore(Base, TimestampMixin):
    __tablename__ = "financial_scores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    calculation_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    overall_health_score: Mapped[int] = mapped_column(Integer, nullable=False)  # 0 to 100
    risk_score: Mapped[int] = mapped_column(Integer, nullable=False)  # 0 (lowest) to 100 (highest risk)
    risk_level: Mapped[str] = mapped_column(String(20), nullable=False)  # Low, Moderate, High, Severe

    savings_ratio: Mapped[Decimal] = mapped_column(Numeric(6, 2), nullable=False)
    debt_to_income_ratio: Mapped[Decimal] = mapped_column(Numeric(6, 2), nullable=False)
    emergency_runway_months: Mapped[Decimal] = mapped_column(Numeric(6, 2), nullable=False)
    cash_flow_volatility_score: Mapped[Decimal] = mapped_column(Numeric(6, 2), nullable=False)
    summary_explanation: Mapped[str] = mapped_column(Text, nullable=False)

    risk_factors: Mapped[list["RiskFactor"]] = relationship("RiskFactor", back_populates="score", cascade="all, delete-orphan")


class RiskFactor(Base, TimestampMixin):
    __tablename__ = "risk_factors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    score_id: Mapped[int] = mapped_column(Integer, ForeignKey("financial_scores.id", ondelete="CASCADE"), nullable=False, index=True)
    factor_name: Mapped[str] = mapped_column(String(100), nullable=False)
    severity: Mapped[str] = mapped_column(String(20), nullable=False)  # low, medium, high, critical
    impact_points: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    mitigation_suggestion: Mapped[str] = mapped_column(String(255), nullable=False)

    score: Mapped["FinancialScore"] = relationship("FinancialScore", back_populates="risk_factors")


class Anomaly(Base, TimestampMixin):
    __tablename__ = "anomalies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    transaction_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("transactions.id", ondelete="SET NULL"), nullable=True, index=True)
    anomaly_type: Mapped[str] = mapped_column(String(50), nullable=False)  # amount_outlier, surge_frequency, duplicate, unusual_category
    severity: Mapped[str] = mapped_column(String(20), default="warning", nullable=False)  # info, warning, high
    detection_method: Mapped[str] = mapped_column(String(50), nullable=False)  # z_score, iqr, isolation_forest, rule_heuristic
    score_value: Mapped[Decimal] = mapped_column(Numeric(8, 3), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    is_resolved: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class Forecast(Base, TimestampMixin):
    __tablename__ = "forecasts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    metric_name: Mapped[str] = mapped_column(String(50), nullable=False)  # monthly_expense, monthly_income, savings_trajectory
    forecast_date: Mapped[date] = mapped_column(Date, nullable=False)
    predicted_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    lower_bound: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    upper_bound: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    confidence_level: Mapped[Decimal] = mapped_column(Numeric(4, 2), default=0.90, nullable=False)
    algorithm_used: Mapped[str] = mapped_column(String(50), default="holt_winters", nullable=False)


class Recommendation(Base, TimestampMixin):
    __tablename__ = "recommendations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(50), nullable=False)  # debt, budgeting, emergency_fund, investment, general
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    impact_estimate: Mapped[str | None] = mapped_column(String(100), nullable=True)
    priority: Mapped[str] = mapped_column(String(20), default="medium", nullable=False)  # low, medium, high, urgent
    is_dismissed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_applied: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
