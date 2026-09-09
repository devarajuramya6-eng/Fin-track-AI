from datetime import date
from decimal import Decimal

from ai.assistant.service import FinancialAssistantService
from backend.app.api.deps import get_current_user, get_db
from backend.app.models.loan import Loan
from backend.app.models.transaction import Transaction, TransactionCategory
from backend.app.models.user import User
from backend.app.schemas.analytics import AssistantQueryRequest, AssistantQueryResponse
from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post("/query", response_model=AssistantQueryResponse)
async def query_financial_assistant(
    request: AssistantQueryRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Submits a conversational financial question to the local assistant.
    Analyzes user financial database metrics without any external AI API.
    """
    start_of_month = date.today().replace(day=1)

    # Fetch live user financial context
    stmt_spent = select(func.coalesce(func.sum(Transaction.amount), Decimal("0.00"))).where(
        Transaction.user_id == current_user.id,
        Transaction.transaction_type == "expense",
        Transaction.transaction_date >= start_of_month,
    )
    monthly_spent = (await db.execute(stmt_spent)).scalar_one()

    stmt_inc = select(func.coalesce(func.sum(Transaction.amount), Decimal("0.00"))).where(
        Transaction.user_id == current_user.id,
        Transaction.transaction_type == "income",
        Transaction.transaction_date >= start_of_month,
    )
    monthly_income = (await db.execute(stmt_inc)).scalar_one()
    if monthly_income == 0:
        monthly_income = Decimal("4000.00")  # Default baseline for guidance

    stmt_top_cat = (
        select(TransactionCategory.name, func.sum(Transaction.amount).label("tot"))
        .join(Transaction, Transaction.category_id == TransactionCategory.id)
        .where(
            Transaction.user_id == current_user.id,
            Transaction.transaction_type == "expense",
            Transaction.transaction_date >= start_of_month,
        )
        .group_by(TransactionCategory.name)
        .order_by(func.sum(Transaction.amount).desc())
        .limit(1)
    )
    top_cat_res = (await db.execute(stmt_top_cat)).first()
    top_cat = top_cat_res[0] if top_cat_res else "General Living"
    top_cat_amount = top_cat_res[1] if top_cat_res else Decimal("0.00")

    stmt_emi = select(func.coalesce(func.sum(Loan.calculated_emi), Decimal("0.00"))).where(
        Loan.user_id == current_user.id, Loan.is_active == True
    )
    monthly_emi = (await db.execute(stmt_emi)).scalar_one()

    context = {
        "monthly_spent": monthly_spent,
        "monthly_income": monthly_income,
        "top_category": top_cat,
        "top_category_amount": top_cat_amount,
        "monthly_emi": monthly_emi,
        "risk_score": 28,
        "emergency_months": Decimal("3.2"),
    }

    result = FinancialAssistantService.process_query(query=request.query, user_context=context)
    return result
