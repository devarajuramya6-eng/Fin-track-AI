from decimal import Decimal
import pytest

from ai.risk.engine import RiskScoringEngine


def test_risk_scoring_healthy_profile():
    result = RiskScoringEngine.evaluate_risk(
        monthly_income=Decimal("8000.00"),
        monthly_debt_obligations=Decimal("800.00"),  # 10% DTI
        liquid_savings=Decimal("40000.00"),           # ~13 months runway
        monthly_expenses=Decimal("3000.00"),
        historical_net_cashflows=[Decimal("4500.00"), Decimal("5000.00"), Decimal("4800.00")],
    )

    assert result["risk_score"] < 25
    assert result["risk_level"] == "Low"
    assert result["overall_health_score"] > 75
    assert result["emergency_runway_months"] >= Decimal("6.0")


def test_risk_scoring_critical_profile():
    result = RiskScoringEngine.evaluate_risk(
        monthly_income=Decimal("3000.00"),
        monthly_debt_obligations=Decimal("2000.00"),  # 66.7% DTI
        liquid_savings=Decimal("500.00"),              # 0.2 month runway
        monthly_expenses=Decimal("2800.00"),
        historical_net_cashflows=[Decimal("-500.00"), Decimal("100.00"), Decimal("-800.00")],
    )

    assert result["risk_score"] >= 50
    assert result["risk_level"] in ["High", "Severe"]
    assert any(f["severity"] == "critical" for f in result["risk_factors"])
