
from datetime import UTC

from ai.anomaly.detector import AnomalyDetectionEngine
from backend.app.api.deps import get_current_user, get_db
from backend.app.models.transaction import Transaction
from backend.app.models.user import User
from backend.app.schemas.analytics import AnomalyRead
from fastapi import APIRouter, Depends
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/", response_model=list[AnomalyRead])
async def list_detected_anomalies(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Executes local statistical anomaly detection (Z-score, IQR, Duplicate check)
    over recent transactions.
    """
    stmt = (
        select(Transaction)
        .where(Transaction.user_id == current_user.id)
        .order_by(desc(Transaction.transaction_date))
        .limit(100)
    )
    result = await db.execute(stmt)
    txs = result.scalars().all()

    tx_dicts = [
        {
            "id": t.id,
            "amount": float(t.amount),
            "payee_or_merchant": t.payee_or_merchant,
            "transaction_date": t.transaction_date,
        }
        for t in txs
    ]

    # 1. Amount anomalies via Z-Score & IQR
    amt_anomalies = AnomalyDetectionEngine.detect_amount_anomalies(tx_dicts)
    # 2. Duplicate anomalies
    dup_anomalies = AnomalyDetectionEngine.detect_duplicate_transactions(tx_dicts)

    all_anomalies = amt_anomalies + dup_anomalies

    from datetime import datetime
    now = datetime.now(UTC)

    anomalies_out = []
    for idx, a in enumerate(all_anomalies, start=1):
        anomalies_out.append(
            AnomalyRead(
                id=idx,
                transaction_id=a.transaction_id,
                anomaly_type=a.anomaly_type,
                severity=a.severity,
                detection_method=a.detection_method,
                score_value=a.score_value,
                description=a.description,
                is_resolved=False,
                created_at=now,
            )
        )

    return anomalies_out
