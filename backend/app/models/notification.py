from datetime import datetime

from backend.app.db.base import Base, TimestampMixin
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Notification(Base, TimestampMixin):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    notification_type: Mapped[str] = mapped_column(String(50), nullable=False)  # budget_alert, anomaly_alert, loan_reminder, savings_milestone, system
    severity: Mapped[str] = mapped_column(String(20), default="info", nullable=False)  # info, warning, success, error
    link_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    read_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="notifications")


class NotificationPreference(Base, TimestampMixin):
    __tablename__ = "notification_preferences"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    enable_budget_alerts: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    enable_anomaly_alerts: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    enable_loan_reminders: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    enable_savings_milestones: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    enable_weekly_digest: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
