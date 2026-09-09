from datetime import UTC, datetime

from backend.app.api.deps import get_current_user, get_db
from backend.app.models.notification import Notification, NotificationPreference
from backend.app.models.user import User
from backend.app.schemas.notification import (
    NotificationPreferenceRead,
    NotificationPreferenceUpdate,
    NotificationRead,
)
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/", response_model=list[NotificationRead])
async def list_notifications(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Retrieves all notifications for authenticated user."""
    stmt = (
        select(Notification)
        .where(Notification.user_id == current_user.id)
        .order_by(desc(Notification.created_at))
        .limit(50)
    )
    result = await db.execute(stmt)
    notifications = result.scalars().all()

    # If no notifications exist yet, create initial welcome & tips alerts
    if not notifications:
        welcome_notifs = [
            Notification(
                user_id=current_user.id,
                title="Welcome to AI FinTech Platform",
                message="Your privacy-first financial dashboard is active. Start by adding your bank or cash accounts.",
                notification_type="system",
                severity="info",
            ),
            Notification(
                user_id=current_user.id,
                title="Budget Alert Engine Active",
                message="Set category spending caps to receive automated threshold warnings when approaching limits.",
                notification_type="budget_alert",
                severity="success",
            ),
        ]
        for wn in welcome_notifs:
            db.add(wn)
        await db.flush()
        result = await db.execute(stmt)
        notifications = result.scalars().all()

    return notifications


@router.put("/{notification_id}/read", response_model=NotificationRead)
async def mark_notification_as_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Marks a notification as acknowledged."""
    stmt = select(Notification).where(Notification.id == notification_id, Notification.user_id == current_user.id)
    notif = (await db.execute(stmt)).scalar_one_or_none()
    if not notif:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found.")

    notif.is_read = True
    notif.read_at = datetime.now(UTC)
    await db.flush()
    return notif


@router.get("/preferences", response_model=NotificationPreferenceRead)
async def get_preferences(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Retrieves user notification toggles."""
    stmt = select(NotificationPreference).where(NotificationPreference.user_id == current_user.id)
    prefs = (await db.execute(stmt)).scalar_one_or_none()
    if not prefs:
        prefs = NotificationPreference(user_id=current_user.id)
        db.add(prefs)
        await db.flush()
    return prefs


@router.put("/preferences", response_model=NotificationPreferenceRead)
async def update_preferences(
    prefs_in: NotificationPreferenceUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Updates user notification toggles."""
    stmt = select(NotificationPreference).where(NotificationPreference.user_id == current_user.id)
    prefs = (await db.execute(stmt)).scalar_one_or_none()
    if not prefs:
        prefs = NotificationPreference(user_id=current_user.id)
        db.add(prefs)

    if prefs_in.enable_budget_alerts is not None:
        prefs.enable_budget_alerts = prefs_in.enable_budget_alerts
    if prefs_in.enable_anomaly_alerts is not None:
        prefs.enable_anomaly_alerts = prefs_in.enable_anomaly_alerts
    if prefs_in.enable_loan_reminders is not None:
        prefs.enable_loan_reminders = prefs_in.enable_loan_reminders
    if prefs_in.enable_savings_milestones is not None:
        prefs.enable_savings_milestones = prefs_in.enable_savings_milestones
    if prefs_in.enable_weekly_digest is not None:
        prefs.enable_weekly_digest = prefs_in.enable_weekly_digest

    await db.flush()
    return prefs
