from datetime import datetime

from pydantic import BaseModel


class NotificationRead(BaseModel):
    id: int
    user_id: int
    title: str
    message: str
    notification_type: str
    severity: str
    link_url: str | None = None
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True


class NotificationPreferenceRead(BaseModel):
    enable_budget_alerts: bool
    enable_anomaly_alerts: bool
    enable_loan_reminders: bool
    enable_savings_milestones: bool
    enable_weekly_digest: bool

    class Config:
        from_attributes = True


class NotificationPreferenceUpdate(BaseModel):
    enable_budget_alerts: bool | None = None
    enable_anomaly_alerts: bool | None = None
    enable_loan_reminders: bool | None = None
    enable_savings_milestones: bool | None = None
    enable_weekly_digest: bool | None = None
