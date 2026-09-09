from datetime import date, datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, Field


class RiskFactorRead(BaseModel):
    id: int
    factor_name: str
    severity: str
    impact_points: int
    description: str
    mitigation_suggestion: str

    class Config:
        from_attributes = True


class RiskScoreRead(BaseModel):
    overall_health_score: int
    risk_score: int
    risk_level: str
    savings_ratio: Decimal
    debt_to_income_ratio: Decimal
    emergency_runway_months: Decimal
    cash_flow_volatility_score: Decimal
    summary_explanation: str
    risk_factors: list[RiskFactorRead] = []

    class Config:
        from_attributes = True


class AnomalyRead(BaseModel):
    id: int
    transaction_id: int | None = None
    anomaly_type: str
    severity: str
    detection_method: str
    score_value: Decimal
    description: str
    is_resolved: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ForecastDataPoint(BaseModel):
    forecast_date: date
    predicted_amount: Decimal
    lower_bound: Decimal
    upper_bound: Decimal


class ForecastResponse(BaseModel):
    metric_name: str
    algorithm: str
    confidence_level: Decimal
    points: list[ForecastDataPoint] = []
    summary_insight: str


class RecommendationRead(BaseModel):
    id: int
    category: str
    title: str
    summary: str
    impact_estimate: str | None = None
    priority: str
    is_applied: bool

    class Config:
        from_attributes = True


class AssistantQueryRequest(BaseModel):
    query: str = Field(..., min_length=2, max_length=500)


class AssistantQueryResponse(BaseModel):
    detected_intent: str
    answer: str
    calculated_data: dict[str, Any] | None = None
    action_suggestion: str | None = None
    disclaimer: str = (
        "Educational estimate only. This platform does not provide regulated financial advice. "
        "Calculations should be independently verified before making major financial commitments."
    )
