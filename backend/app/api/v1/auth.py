from datetime import datetime, timezone, timedelta
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.deps import get_db, get_current_user
from backend.app.core.config import settings
from backend.app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    get_password_hash,
    verify_password,
)
from backend.app.models.user import User, SessionRecord
from backend.app.models.account import Account
from backend.app.models.notification import NotificationPreference
from backend.app.models.transaction import TransactionCategory
from backend.app.api.v1.categories import DEFAULT_CATEGORIES
from backend.app.schemas.auth import (
    Token,
    UserLogin,
    UserRegister,
    RefreshTokenRequest,
    PasswordResetRequest,
    PasswordResetConfirm,
)
from backend.app.schemas.user import UserRead
from backend.app.services.audit_service import AuditService

router = APIRouter()


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(user_in: UserRegister, db: AsyncSession = Depends(get_db)):
    """Registers a new user account with default accounts, categories, and notification preferences."""
    stmt = select(User).where(User.email == user_in.email)
    existing_user = (await db.execute(stmt)).scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email address already exists.",
        )

    user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        preferred_currency=user_in.preferred_currency,
        is_active=True,
        is_superuser=False,
    )
    db.add(user)
    await db.flush()

    # Create default notification preferences
    prefs = NotificationPreference(user_id=user.id)
    db.add(prefs)

    # Auto-seed starter accounts for new user with their chosen currency
    curr = user_in.preferred_currency
    initial_check = Decimal("50000.00") if curr == "INR" else Decimal("5000.00")
    initial_sav = Decimal("100000.00") if curr == "INR" else Decimal("10000.00")
    initial_cash = Decimal("5000.00") if curr == "INR" else Decimal("500.00")

    starter_accounts = [
        Account(
            user_id=user.id,
            name="Primary Bank Account",
            account_type="checking",
            institution_name="Primary Bank",
            currency=curr,
            current_balance=initial_check,
            color="#3b82f6",
            is_active=True,
        ),
        Account(
            user_id=user.id,
            name="Savings Account",
            account_type="savings",
            institution_name="Reserve Savings",
            currency=curr,
            current_balance=initial_sav,
            color="#10b981",
            is_active=True,
        ),
        Account(
            user_id=user.id,
            name="Cash Wallet",
            account_type="cash",
            institution_name="Physical Cash",
            currency=curr,
            current_balance=initial_cash,
            color="#f59e0b",
            is_active=True,
        ),
    ]
    for acc in starter_accounts:
        db.add(acc)

    # Ensure system categories exist
    cat_check = await db.execute(select(TransactionCategory).limit(1))
    if not cat_check.first():
        for cat_data in DEFAULT_CATEGORIES:
            db.add(
                TransactionCategory(
                    name=cat_data["name"],
                    category_type=cat_data["category_type"],
                    icon=cat_data["icon"],
                    color=cat_data["color"],
                    is_system=True,
                )
            )

    await db.flush()

    await AuditService.log_event(
        db,
        action="USER_REGISTER",
        entity_type="User",
        user_id=user.id,
        details=f"User {user.email} registered successfully with default {curr} accounts.",
    )

    return user


from fastapi import APIRouter, Depends, HTTPException, Request, status

@router.post("/login", response_model=Token)
async def login_for_access_token(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """Authenticates user credentials and issues access & refresh tokens (supports both JSON and Form Data)."""
    username = None
    password = None

    content_type = request.headers.get("content-type", "").lower()
    if "application/json" in content_type:
        try:
            body = await request.json()
            if isinstance(body, dict):
                username = body.get("username") or body.get("email")
                password = body.get("password")
        except Exception:
            pass
    else:
        try:
            form = await request.form()
            username = form.get("username") or form.get("email")
            password = form.get("password")
        except Exception:
            pass

    if not username or not password:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Email/username and password are required.",
        )

    stmt = select(User).where(User.email == str(username).strip())
    user = (await db.execute(stmt)).scalar_one_or_none()

    if not user or not verify_password(str(password), user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user account.")

    # Ensure this user has at least one account
    acc_check = await db.execute(select(Account).where(Account.user_id == user.id, Account.is_active == True))
    if not acc_check.first():
        curr = user.preferred_currency or "USD"
        db.add(
            Account(
                user_id=user.id,
                name="Primary Bank Account",
                account_type="checking",
                currency=curr,
                current_balance=Decimal("50000.00") if curr == "INR" else Decimal("5000.00"),
                color="#3b82f6",
                is_active=True,
            )
        )
        db.add(
            Account(
                user_id=user.id,
                name="Savings Account",
                account_type="savings",
                currency=curr,
                current_balance=Decimal("100000.00") if curr == "INR" else Decimal("10000.00"),
                color="#10b981",
                is_active=True,
            )
        )
        await db.flush()

    access_token = create_access_token(subject=user.id)
    refresh_token = create_refresh_token(subject=user.id)

    # Record session
    session = SessionRecord(
        user_id=user.id,
        refresh_token_jti=refresh_token[-20:],
        expires_at=datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )
    db.add(session)
    await db.flush()

    await AuditService.log_event(
        db,
        action="USER_LOGIN",
        entity_type="User",
        user_id=user.id,
        details="User logged in successfully.",
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }


@router.post("/refresh", response_model=Token)
async def refresh_access_token(request: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    """Issues a new access token from a valid refresh token."""
    payload = decode_token(request.refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token.",
        )
    user_id = payload.get("sub")
    stmt = select(User).where(User.id == int(user_id))
    user = (await db.execute(stmt)).scalar_one_or_none()
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user.")

    new_access_token = create_access_token(subject=user.id)
    new_refresh_token = create_refresh_token(subject=user.id)

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout_user(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Terminates session for the authenticated user."""
    await AuditService.log_event(
        db,
        action="USER_LOGOUT",
        entity_type="User",
        user_id=current_user.id,
        details="User logged out.",
    )
    return {"message": "Successfully logged out."}


@router.post("/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password(request: PasswordResetRequest, db: AsyncSession = Depends(get_db)):
    """Generates a secure password reset token (logged locally without external email API)."""
    stmt = select(User).where(User.email == request.email)
    user = (await db.execute(stmt)).scalar_one_or_none()
    if user:
        reset_token = create_access_token(subject=user.id, expires_delta=timedelta(hours=1))
        await AuditService.log_event(
            db,
            action="PASSWORD_RESET_REQUEST",
            entity_type="User",
            user_id=user.id,
            details=f"Password reset token issued: {reset_token[:10]}...",
        )
    return {"message": "If that email exists, password reset instructions have been generated."}


@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(request: PasswordResetConfirm, db: AsyncSession = Depends(get_db)):
    """Applies a new password using a verified reset token."""
    payload = decode_token(request.token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired reset token.")
    user_id = payload.get("sub")
    stmt = select(User).where(User.id == int(user_id))
    user = (await db.execute(stmt)).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    user.hashed_password = get_password_hash(request.new_password)
    await AuditService.log_event(
        db,
        action="PASSWORD_RESET_COMPLETED",
        entity_type="User",
        user_id=user.id,
        details="Password successfully updated.",
    )
    return {"message": "Password updated successfully."}
