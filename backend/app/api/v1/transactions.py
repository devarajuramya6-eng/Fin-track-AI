import csv
import io
from datetime import date

from backend.app.api.deps import get_current_user, get_db
from backend.app.models.account import Account
from backend.app.models.transaction import (
    Transaction,
    TransactionTagMap,
)
from backend.app.models.user import User
from backend.app.schemas.transaction import (
    TransactionCreate,
    TransactionRead,
    TransactionUpdate,
)
from backend.app.services.audit_service import AuditService
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

router = APIRouter()


@router.get("/", response_model=list[TransactionRead])
async def list_transactions(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    account_id: int | None = None,
    category_id: int | None = None,
    transaction_type: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    search: str | None = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Retrieves paginated, filtered, and searchable transactions."""
    query = (
        select(Transaction)
        .where(Transaction.user_id == current_user.id)
        .options(selectinload(Transaction.category))
        .order_by(desc(Transaction.transaction_date), desc(Transaction.id))
    )

    if account_id:
        query = query.where(Transaction.account_id == account_id)
    if category_id:
        query = query.where(Transaction.category_id == category_id)
    if transaction_type:
        query = query.where(Transaction.transaction_type == transaction_type)
    if start_date:
        query = query.where(Transaction.transaction_date >= start_date)
    if end_date:
        query = query.where(Transaction.transaction_date <= end_date)
    if search:
        search_pattern = f"%{search}%"
        query = query.where(
            (Transaction.payee_or_merchant.ilike(search_pattern))
            | (Transaction.description.ilike(search_pattern))
            | (Transaction.notes.ilike(search_pattern))
        )

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/", response_model=TransactionRead, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    tx_in: TransactionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Records a new transaction and automatically synchronizes the corresponding account balance."""
    # Verify account ownership
    stmt_acc = select(Account).where(Account.id == tx_in.account_id, Account.user_id == current_user.id)
    account = (await db.execute(stmt_acc)).scalar_one_or_none()
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found.")

    tx = Transaction(
        user_id=current_user.id,
        account_id=tx_in.account_id,
        category_id=tx_in.category_id,
        amount=tx_in.amount,
        transaction_type=tx_in.transaction_type,
        transaction_date=tx_in.transaction_date,
        payee_or_merchant=tx_in.payee_or_merchant,
        description=tx_in.description,
        notes=tx_in.notes,
        payment_method=tx_in.payment_method,
        is_excluded_from_budget=tx_in.is_excluded_from_budget,
        reference_number=tx_in.reference_number,
    )
    db.add(tx)
    await db.flush()

    # Synchronize account balance
    if tx_in.transaction_type == "income":
        account.current_balance += tx_in.amount
    elif tx_in.transaction_type == "expense":
        account.current_balance -= tx_in.amount

    # Map tags if provided
    if tx_in.tag_ids:
        for tid in tx_in.tag_ids:
            db.add(TransactionTagMap(transaction_id=tx.id, tag_id=tid))

    await db.flush()

    # Reload with category for serialization
    stmt_reload = select(Transaction).where(Transaction.id == tx.id).options(selectinload(Transaction.category))
    reloaded_tx = (await db.execute(stmt_reload)).scalar_one()

    await AuditService.log_event(
        db,
        action="TRANSACTION_CREATE",
        entity_type="Transaction",
        user_id=current_user.id,
        entity_id=str(tx.id),
        details=f"Created {tx.transaction_type} of ${tx.amount} at '{tx.payee_or_merchant}'",
    )

    return reloaded_tx


@router.get("/{transaction_id}", response_model=TransactionRead)
async def get_transaction(
    transaction_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Retrieves single transaction details."""
    stmt = (
        select(Transaction)
        .where(Transaction.id == transaction_id, Transaction.user_id == current_user.id)
        .options(selectinload(Transaction.category))
    )
    tx = (await db.execute(stmt)).scalar_one_or_none()
    if not tx:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found.")
    return tx


@router.put("/{transaction_id}", response_model=TransactionRead)
async def update_transaction(
    transaction_id: int,
    tx_in: TransactionUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Updates transaction details."""
    stmt = (
        select(Transaction)
        .where(Transaction.id == transaction_id, Transaction.user_id == current_user.id)
        .options(selectinload(Transaction.category))
    )
    tx = (await db.execute(stmt)).scalar_one_or_none()
    if not tx:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found.")

    if tx_in.amount is not None:
        tx.amount = tx_in.amount
    if tx_in.category_id is not None:
        tx.category_id = tx_in.category_id
    if tx_in.transaction_type is not None:
        tx.transaction_type = tx_in.transaction_type
    if tx_in.transaction_date is not None:
        tx.transaction_date = tx_in.transaction_date
    if tx_in.payee_or_merchant is not None:
        tx.payee_or_merchant = tx_in.payee_or_merchant
    if tx_in.description is not None:
        tx.description = tx_in.description
    if tx_in.notes is not None:
        tx.notes = tx_in.notes
    if tx_in.payment_method is not None:
        tx.payment_method = tx_in.payment_method

    await db.flush()
    return tx


@router.delete("/{transaction_id}", status_code=status.HTTP_200_OK)
async def delete_transaction(
    transaction_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Deletes transaction and reverts account balance adjustment."""
    stmt = select(Transaction).where(Transaction.id == transaction_id, Transaction.user_id == current_user.id)
    tx = (await db.execute(stmt)).scalar_one_or_none()
    if not tx:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found.")

    # Revert account balance
    stmt_acc = select(Account).where(Account.id == tx.account_id)
    account = (await db.execute(stmt_acc)).scalar_one_or_none()
    if account:
        if tx.transaction_type == "income":
            account.current_balance -= tx.amount
        elif tx.transaction_type == "expense":
            account.current_balance += tx.amount

    await db.delete(tx)
    await db.flush()
    return {"message": "Transaction deleted successfully."}


@router.get("/export-csv", response_class=StreamingResponse)
async def export_transactions_csv(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Exports user transactions as a downloadable CSV file."""
    stmt = (
        select(Transaction)
        .where(Transaction.user_id == current_user.id)
        .options(selectinload(Transaction.category))
        .order_by(desc(Transaction.transaction_date))
    )
    result = await db.execute(stmt)
    transactions = result.scalars().all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Date", "Type", "Amount", "Payee", "Category", "Payment Method", "Description", "Notes"])

    for t in transactions:
        cat_name = t.category.name if t.category else "Uncategorized"
        writer.writerow([
            t.transaction_date.isoformat(),
            t.transaction_type,
            f"{t.amount:.2f}",
            t.payee_or_merchant,
            cat_name,
            t.payment_method,
            t.description or "",
            t.notes or "",
        ])

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=transactions.csv"},
    )


@router.post("/import-csv", status_code=status.HTTP_200_OK)
async def import_transactions_csv(
    account_id: int = Query(...),
    csv_content: str = Query(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Imports transactions from a raw CSV text content into the specified account."""
    stmt_acc = select(Account).where(Account.id == account_id, Account.user_id == current_user.id)
    account = (await db.execute(stmt_acc)).scalar_one_or_none()
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found.")

    # Fetch default or first available category
    from backend.app.models.category import Category
    stmt_cat = select(Category).where(Category.user_id == current_user.id).limit(1)
    default_cat = (await db.execute(stmt_cat)).scalar_one_or_none()
    default_cat_id = default_cat.id if default_cat else 1

    reader = csv.reader(io.StringIO(csv_content))
    imported_count = 0

    for row_idx, row in enumerate(reader):
        if not row or len(row) < 3:
            continue
        # Skip header row if present
        if row_idx == 0 and any(col.lower() in ("date", "amount", "payee", "type") for col in row):
            continue

        try:
            # Expected format: Date, Type, Amount, Payee, ...
            tx_date_str = row[0].strip()
            tx_type_str = row[1].strip().lower() if len(row) > 1 else "expense"
            if tx_type_str not in ("income", "expense"):
                tx_type_str = "expense"
            tx_amount = abs(float(row[2].replace("$", "").replace("₹", "").replace(",", "").strip()))
            tx_payee = row[3].strip() if len(row) > 3 and row[3].strip() else "Bank Transaction"

            tx_date_obj = date.fromisoformat(tx_date_str)

            tx = Transaction(
                user_id=current_user.id,
                account_id=account.id,
                category_id=default_cat_id,
                amount=tx_amount,
                transaction_type=tx_type_str,
                transaction_date=tx_date_obj,
                payee_or_merchant=tx_payee,
                description="Imported via CSV",
                payment_method="card",
            )
            db.add(tx)

            if tx_type_str == "income":
                account.current_balance += tx_amount
            else:
                account.current_balance -= tx_amount

            imported_count += 1
        except Exception:
            continue

    await db.flush()
    return {"message": f"Successfully imported {imported_count} transactions.", "imported_count": imported_count}
