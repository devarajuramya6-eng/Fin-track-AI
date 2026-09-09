
from backend.app.api.deps import get_current_user, get_db
from backend.app.models.account import Account
from backend.app.models.user import User
from backend.app.schemas.account import AccountCreate, AccountRead, AccountUpdate
from backend.app.services.audit_service import AuditService
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/", response_model=list[AccountRead])
async def list_accounts(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Lists all financial accounts owned by the user."""
    stmt = select(Account).where(Account.user_id == current_user.id, Account.is_active == True)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.post("/", response_model=AccountRead, status_code=status.HTTP_201_CREATED)
async def create_account(
    account_in: AccountCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Creates a new financial account (Bank, Card, Wallet, Cash, etc.)."""
    account = Account(
        user_id=current_user.id,
        name=account_in.name,
        account_type=account_in.account_type,
        institution_name=account_in.institution_name,
        account_number_mask=account_in.account_number_mask,
        currency=account_in.currency,
        current_balance=account_in.initial_balance,
        color=account_in.color,
    )
    db.add(account)
    await db.flush()

    await AuditService.log_event(
        db,
        action="ACCOUNT_CREATE",
        entity_type="Account",
        user_id=current_user.id,
        entity_id=str(account.id),
        details=f"Created account '{account.name}' with initial balance {account.current_balance}",
    )
    return account


@router.get("/{account_id}", response_model=AccountRead)
async def get_account(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Retrieves account details by ID."""
    stmt = select(Account).where(Account.id == account_id, Account.user_id == current_user.id)
    account = (await db.execute(stmt)).scalar_one_or_none()
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found.")
    return account


@router.put("/{account_id}", response_model=AccountRead)
async def update_account(
    account_id: int,
    account_in: AccountUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Updates account details."""
    stmt = select(Account).where(Account.id == account_id, Account.user_id == current_user.id)
    account = (await db.execute(stmt)).scalar_one_or_none()
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found.")

    if account_in.name is not None:
        account.name = account_in.name
    if account_in.institution_name is not None:
        account.institution_name = account_in.institution_name
    if account_in.account_number_mask is not None:
        account.account_number_mask = account_in.account_number_mask
    if account_in.color is not None:
        account.color = account_in.color
    if account_in.is_active is not None:
        account.is_active = account_in.is_active

    await db.flush()
    return account


@router.delete("/{account_id}", status_code=status.HTTP_200_OK)
async def delete_account(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Soft-deletes or archives an account."""
    stmt = select(Account).where(Account.id == account_id, Account.user_id == current_user.id)
    account = (await db.execute(stmt)).scalar_one_or_none()
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found.")
    account.is_active = False
    await db.flush()
    return {"message": "Account archived successfully."}
