from typing import Dict, List, Optional
import numpy as np


class AnomalyResult:
    def __init__(
        self,
        transaction_id: Optional[int],
        anomaly_type: str,
        severity: str,
        detection_method: str,
        score_value: float,
        description: str,
    ):
        self.transaction_id = transaction_id
        self.anomaly_type = anomaly_type
        self.severity = severity
        self.detection_method = detection_method
        self.score_value = score_value
        self.description = description

    def to_dict(self) -> Dict:
        return {
            "transaction_id": self.transaction_id,
            "anomaly_type": self.anomaly_type,
            "severity": self.severity,
            "detection_method": self.detection_method,
            "score_value": round(self.score_value, 2),
            "description": self.description,
        }


class AnomalyDetectionEngine:
    """
    Multi-model anomaly detection engine using purely local algorithms:
    1. Parametric Z-Score Analysis: Flag values exceeding mean + k * std_dev
    2. Non-parametric Interquartile Range (IQR): Robust against heavy-tailed spending
    3. Duplicate Transaction Heuristics: Identical amount & payee within short timeframe
    4. Category Surge Detection: Unusually high cumulative category burn in rolling period
    """

    @classmethod
    def detect_amount_anomalies(
        cls,
        transactions: List[Dict],
        z_threshold: float = 2.5,
        iqr_multiplier: float = 1.5,
    ) -> List[AnomalyResult]:
        anomalies: List[AnomalyResult] = []
        if len(transactions) < 5:
            return anomalies

        amounts = np.array([float(t["amount"]) for t in transactions])
        mean_val = float(np.mean(amounts))
        std_val = float(np.std(amounts))

        q25, q75 = np.percentile(amounts, [25, 75])
        iqr = q75 - q25
        iqr_upper_bound = q75 + (iqr_multiplier * iqr)

        for t in transactions:
            amt = float(t["amount"])
            t_id = t.get("id")
            payee = t.get("payee_or_merchant", "Unknown")

            # 1. Check Z-Score
            if std_val > 0:
                z_score = (amt - mean_val) / std_val
                if z_score >= z_threshold:
                    severity = "high" if z_score > 3.5 else "warning"
                    anomalies.append(
                        AnomalyResult(
                            transaction_id=t_id,
                            anomaly_type="amount_outlier",
                            severity=severity,
                            detection_method="z_score",
                            score_value=float(z_score),
                            description=(
                                f"Unusually large charge of ${amt:,.2f} at '{payee}'. "
                                f"Exceeds historical average (${mean_val:,.2f}) by {z_score:.1f} standard deviations."
                            ),
                        )
                    )
                    continue

            # 2. Check IQR Upper Bound
            if amt > iqr_upper_bound and iqr > 0:
                score_val = (amt - q75) / iqr
                anomalies.append(
                    AnomalyResult(
                        transaction_id=t_id,
                        anomaly_type="amount_outlier",
                        severity="warning",
                        detection_method="iqr",
                        score_value=float(score_val),
                        description=(
                            f"Spending of ${amt:,.2f} at '{payee}' is well above the 75th percentile limit "
                            f"(${iqr_upper_bound:,.2f})."
                        ),
                    )
                )

        return anomalies

    @classmethod
    def detect_duplicate_transactions(cls, transactions: List[Dict]) -> List[AnomalyResult]:
        """Detects possible accidental double-charges (same merchant and identical amount on same day)."""
        anomalies: List[AnomalyResult] = []
        seen = {}

        for t in transactions:
            key = (str(t.get("payee_or_merchant", "")).lower().strip(), str(t.get("amount")), str(t.get("transaction_date")))
            t_id = t.get("id")
            if key in seen:
                prev_id = seen[key]
                anomalies.append(
                    AnomalyResult(
                        transaction_id=t_id,
                        anomaly_type="duplicate",
                        severity="warning",
                        detection_method="rule_heuristic",
                        score_value=1.0,
                        description=(
                            f"Potential duplicate transaction detected: ${t.get('amount')} at "
                            f"'{t.get('payee_or_merchant')}' on {t.get('transaction_date')} (matches transaction #{prev_id})."
                        ),
                    )
                )
            else:
                seen[key] = t_id

        return anomalies
