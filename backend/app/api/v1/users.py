from backend.app.api.deps import get_current_user, get_db
from backend.app.core.security import get_password_hash, verify_password
from backend.app.models.user import User
from backend.app.schemas.user import PasswordChange, UserRead, UserUpdate
from backend.app.services.audit_service import AuditService
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/me", response_model=UserRead)
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Fetches authenticated user's profile details."""
    return current_user


@router.put("/me", response_model=UserRead)
async def update_current_user_profile(
    user_in: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Updates user profile information."""
    if user_in.full_name is not None:
        current_user.full_name = user_in.full_name
    if user_in.preferred_currency is not None:
        current_user.preferred_currency = user_in.preferred_currency
    if user_in.timezone is not None:
        current_user.timezone = user_in.timezone

    await AuditService.log_event(
        db,
        action="USER_PROFILE_UPDATE",
        entity_type="User",
        user_id=current_user.id,
        details="User updated profile details.",
    )
    return current_user


@router.put("/me/password", status_code=status.HTTP_200_OK)
async def update_user_password(
    password_in: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Changes password after verifying existing password."""
    if not verify_password(password_in.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password verification failed.",
        )
    current_user.hashed_password = get_password_hash(password_in.new_password)
    await AuditService.log_event(
        db,
        action="USER_PASSWORD_CHANGE",
        entity_type="User",
        user_id=current_user.id,
        details="User changed password.",
    )
    return {"message": "Password changed successfully."}
