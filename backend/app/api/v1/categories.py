
from backend.app.api.deps import get_current_user, get_db
from backend.app.models.transaction import TransactionCategory
from backend.app.models.user import User
from backend.app.schemas.transaction import CategoryCreate, CategoryRead
from fastapi import APIRouter, Depends, status
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

DEFAULT_CATEGORIES = [
    {"name": "Salary & Income", "category_type": "income", "icon": "Wallet", "color": "#10b981"},
    {"name": "Investments & Dividends", "category_type": "income", "icon": "TrendingUp", "color": "#059669"},
    {"name": "Housing & Rent", "category_type": "expense", "icon": "Home", "color": "#ef4444"},
    {"name": "Groceries & Food", "category_type": "expense", "icon": "ShoppingCart", "color": "#f97316"},
    {"name": "Transportation & Fuel", "category_type": "expense", "icon": "Car", "color": "#eab308"},
    {"name": "Utilities & Bills", "category_type": "expense", "icon": "Zap", "color": "#6366f1"},
    {"name": "Healthcare & Medical", "category_type": "expense", "icon": "Activity", "color": "#ec4899"},
    {"name": "Dining Out & Cafes", "category_type": "expense", "icon": "Coffee", "color": "#8b5cf6"},
    {"name": "Entertainment & Leisure", "category_type": "expense", "icon": "Film", "color": "#a855f7"},
    {"name": "Education & Learning", "category_type": "expense", "icon": "BookOpen", "color": "#06b6d4"},
    {"name": "Shopping & Discretionary", "category_type": "expense", "icon": "ShoppingBag", "color": "#f43f5e"},
    {"name": "Loan EMI & Debt", "category_type": "expense", "icon": "CreditCard", "color": "#dc2626"},
    {"name": "Transfer & Adjustment", "category_type": "transfer", "icon": "Repeat", "color": "#64748b"},
]


@router.get("/", response_model=list[CategoryRead])
async def list_categories(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Lists all available categories (system defaults + custom user categories)."""
    stmt = select(TransactionCategory).where(
        or_(
            TransactionCategory.is_system == True,
            TransactionCategory.user_id == current_user.id,
        )
    )
    result = await db.execute(stmt)
    categories = result.scalars().all()

    # If no system categories exist in database yet, seed them automatically
    if not categories:
        for cat_data in DEFAULT_CATEGORIES:
            cat = TransactionCategory(
                name=cat_data["name"],
                category_type=cat_data["category_type"],
                icon=cat_data["icon"],
                color=cat_data["color"],
                is_system=True,
            )
            db.add(cat)
        await db.flush()
        result = await db.execute(stmt)
        categories = result.scalars().all()

    return categories


@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
async def create_custom_category(
    cat_in: CategoryCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Creates a user-defined custom category."""
    cat = TransactionCategory(
        user_id=current_user.id,
        name=cat_in.name,
        category_type=cat_in.category_type,
        icon=cat_in.icon,
        color=cat_in.color,
        parent_id=cat_in.parent_id,
        is_system=False,
    )
    db.add(cat)
    await db.flush()
    return cat
