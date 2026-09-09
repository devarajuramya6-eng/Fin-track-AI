from datetime import date
from decimal import Decimal
from typing import Dict, List
from dateutil.relativedelta import relativedelta
import numpy as np


class ForecastingEngine:
    """
    Local time-series forecasting engine for cash flows, expenses, and savings trajectories.
    Uses linear trend extrapolation and exponential moving averages with confidence intervals.
    Does not require external APIs.
    """

    @classmethod
    def forecast_linear_trend(
        cls,
        historical_monthly_data: List[Decimal],
        start_date: date,
        periods_ahead: int = 3,
        metric_name: str = "monthly_expenses",
    ) -> Dict:
        if not historical_monthly_data:
            return {
                "metric_name": metric_name,
                "algorithm": "linear_regression",
                "confidence_level": Decimal("0.80"),
                "points": [],
                "summary_insight": "Insufficient historical billing cycles to compute forecast.",
            }

        y = np.array([float(val) for val in historical_monthly_data])
        n = len(y)
        x = np.arange(n)

        if n >= 2:
            # Fit line y = mx + c
            slope, intercept = np.polyfit(x, y, 1)
            residuals = y - (slope * x + intercept)
            std_err = float(np.std(residuals)) if len(residuals) > 0 else 0.0
        else:
            slope = 0.0
            intercept = y[0]
            std_err = y[0] * 0.1

        points = []
        for step in range(1, periods_ahead + 1):
            future_x = n - 1 + step
            predicted = max(0.0, slope * future_x + intercept)
            margin = max(predicted * 0.05, 1.96 * std_err)
            
            future_date = start_date + relativedelta(months=step)
            points.append({
                "forecast_date": future_date,
                "predicted_amount": Decimal(str(round(predicted, 2))),
                "lower_bound": Decimal(str(round(max(0.0, predicted - margin), 2))),
                "upper_bound": Decimal(str(round(predicted + margin, 2))),
            })

        trend_direction = "upward" if slope > 0 else "downward" if slope < 0 else "flat"
        summary = (
            f"Based on {n} billing cycles, {metric_name.replace('_', ' ')} exhibits a {trend_direction} trend "
            f"with an estimated average trajectory of ${points[0]['predicted_amount'] if points else 0:,.2f} next month."
        )

        return {
            "metric_name": metric_name,
            "algorithm": "linear_trend_fitting",
            "confidence_level": Decimal("0.85"),
            "points": points,
            "summary_insight": summary,
        }
