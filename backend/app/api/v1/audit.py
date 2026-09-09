
from backend.app.api.deps import get_current_user, get_db
from backend.app.models.audit import AuditLog
from backend.app.models.user import User
from backend.app.schemas.audit import AuditLogRead
from fastapi import APIRouter, Depends
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/logs", response_model=list[AuditLogRead])
async def list_audit_logs(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Retrieves immutable audit trail for security compliance."""
    stmt = select(AuditLog).order_by(desc(AuditLog.created_at)).limit(100)
    result = await db.execute(stmt)
    return result.scalars().all()
