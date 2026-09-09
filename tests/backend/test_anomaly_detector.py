from datetime import date
import pytest

from ai.anomaly.detector import AnomalyDetectionEngine


def test_anomaly_detection_amount_outlier():
    # Normal spending around 20-50, with one 1500 charge
    txs = [
        {"id": 1, "amount": 25.0, "payee_or_merchant": "Coffee Shop", "transaction_date": date(2026, 1, 1)},
        {"id": 2, "amount": 30.0, "payee_or_merchant": "Bakery", "transaction_date": date(2026, 1, 2)},
        {"id": 3, "amount": 45.0, "payee_or_merchant": "Grocery", "transaction_date": date(2026, 1, 3)},
        {"id": 4, "amount": 28.0, "payee_or_merchant": "Lunch", "transaction_date": date(2026, 1, 4)},
        {"id": 5, "amount": 35.0, "payee_or_merchant": "Dinner", "transaction_date": date(2026, 1, 5)},
        {"id": 6, "amount": 1500.0, "payee_or_merchant": "Luxury Watch", "transaction_date": date(2026, 1, 6)},
    ]

    anomalies = AnomalyDetectionEngine.detect_amount_anomalies(txs)
    assert len(anomalies) >= 1
    target = next((a for a in anomalies if a.transaction_id == 6), None)
    assert target is not None
    assert target.anomaly_type == "amount_outlier"


def test_anomaly_detection_duplicate():
    txs = [
        {"id": 101, "amount": 99.99, "payee_or_merchant": "Software Sub", "transaction_date": date(2026, 2, 1)},
        {"id": 102, "amount": 99.99, "payee_or_merchant": "Software Sub", "transaction_date": date(2026, 2, 1)},
    ]

    duplicates = AnomalyDetectionEngine.detect_duplicate_transactions(txs)
    assert len(duplicates) == 1
    assert duplicates[0].anomaly_type == "duplicate"
    assert duplicates[0].transaction_id == 102
