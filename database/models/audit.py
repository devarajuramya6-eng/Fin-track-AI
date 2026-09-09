from typing import Optional

from backend.app.db.base import Base, TimestampMixin
from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


class AuditLog(Base, TimestampMixin):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    action: Mapped[str] = mapped_column(String(100), nullable=False, index=True)  # LOGIN, LOGOUT, CREATE_TRANSACTION, UPDATE_BUDGET, etc.
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False)  # User, Transaction, Account, Loan, etc.
    entity_id: Mapped[str | None] = mapped_column(String(50), nullable=True)
    details: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON or descriptive text
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(255), nullable=True)

    user: Mapped[Optional["User"]] = relationship("User", back_populates="audit_logs")
