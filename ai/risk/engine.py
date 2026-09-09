from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, List
import numpy as np


class RiskFactorResult:
    def __init__(self, name: str, severity: str, impact_points: int, description: str, suggestion: str):
        self.factor_name = name
        self.severity = severity
        self.impact_points = impact_points
        self.description = description
        self.mitigation_suggestion = suggestion

    def to_dict(self) -> Dict:
        return {
            "factor_name": self.factor_name,
            "severity": self.severity,
            "impact_points": self.impact_points,
            "description": self.description,
            "mitigation_suggestion": self.mitigation_suggestion,
        }


class RiskScoringEngine:
    """
    Explainable, deterministic financial risk scoring engine.
    Produces a composite 0-100 Risk Score based on 5 quantitative financial pillars:
    1. Debt-to-Income Ratio (DTI) - Max 30 points
    2. Emergency Runway (Months of survival) - Max 25 points
    3. Cash Flow Volatility (Standard deviation) - Max 20 points
    4. Savings Ratio (Savings / Income) - Max 15 points
    5. Loan Burden / Overdue Obligations - Max 10 points

    Risk Classification:
      0 - 24 : Low Risk (Optimal Financial Health)
      25 - 49: Moderate Risk (Stable with room for optimization)
      50 - 74: High Risk (Vulnerable to financial shocks)
      75 - 100: Critical Risk (Urgent restructuring needed)
    """

    @classmethod
    def evaluate_risk(
        cls,
        monthly_income: Decimal,
        monthly_debt_obligations: Decimal,
        liquid_savings: Decimal,
        monthly_expenses: Decimal,
        historical_net_cashflows: List[Decimal],
    ) -> Dict:
        risk_score = 0
        factors: List[RiskFactorResult] = []

        # Pillar 1: Debt-to-Income (DTI)
        if monthly_income > 0:
            dti = (monthly_debt_obligations / monthly_income) * Decimal("100")
        else:
            dti = Decimal("100.00")

        if dti > Decimal("50.0"):
            pts = 30
            risk_score += pts
            factors.append(
                RiskFactorResult(
                    name="Severe Debt-to-Income Ratio",
                    severity="critical",
                    impact_points=pts,
                    description=f"Debt obligations consume {dti:.1f}% of monthly income (>50%).",
                    suggestion="Prioritize debt paydown via avalanche method or explore loan restructuring.",
                )
            )
        elif dti > Decimal("36.0"):
            pts = 18
            risk_score += pts
            factors.append(
                RiskFactorResult(
                    name="Elevated Debt-to-Income Ratio",
                    severity="medium",
                    impact_points=pts,
                    description=f"Debt obligations consume {dti:.1f}% of income (recommended threshold: <36%).",
                    suggestion="Avoid acquiring new consumer debt and accelerate loan prepayments.",
                )
            )
        else:
            factors.append(
                RiskFactorResult(
                    name="Healthy Debt-to-Income Ratio",
                    severity="low",
                    impact_points=0,
                    description=f"Debt obligations are well-managed at {dti:.1f}% of income.",
                    suggestion="Maintain low leverage and keep credit utilization below 30%.",
                )
            )

        # Pillar 2: Emergency Runway (Months of liquid reserves)
        if monthly_expenses > 0:
            runway_months = (liquid_savings / monthly_expenses).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
        else:
            runway_months = Decimal("12.0")

        if runway_months < Decimal("1.0"):
            pts = 25
            risk_score += pts
            factors.append(
                RiskFactorResult(
                    name="Critical Liquidity Deficit",
                    severity="critical",
                    impact_points=pts,
                    description=f"Liquid emergency fund covers only {runway_months} months of basic expenses.",
                    suggestion="Build an immediate 1-month buffer, then expand to 3-6 months.",
                )
            )
        elif runway_months < Decimal("3.0"):
            pts = 14
            risk_score += pts
            factors.append(
                RiskFactorResult(
                    name="Below-Target Emergency Buffer",
                    severity="medium",
                    impact_points=pts,
                    description=f"Emergency fund covers {runway_months} months (recommended: 3 to 6 months).",
                    suggestion="Direct 10-15% of surplus cash flow into a high-yield savings account.",
                )
            )
        else:
            factors.append(
                RiskFactorResult(
                    name="Robust Emergency Reserves",
                    severity="low",
                    impact_points=0,
                    description=f"Healthy emergency runway of {runway_months} months.",
                    suggestion="Keep liquid buffer intact and allocate excess cash to investments.",
                )
            )

        # Pillar 3: Cash Flow Volatility
        volatility_score = Decimal("0.00")
        if len(historical_net_cashflows) >= 3:
            floats = [float(x) for x in historical_net_cashflows]
            std_dev = float(np.std(floats))
            mean_cf = abs(float(np.mean(floats))) if float(np.mean(floats)) != 0 else 1.0
            coef_var = std_dev / mean_cf
            volatility_score = Decimal(str(round(coef_var, 2)))

            if coef_var > 1.5:
                pts = 20
                risk_score += pts
                factors.append(
                    RiskFactorResult(
                        name="High Spending & Cash Flow Volatility",
                        severity="high",
                        impact_points=pts,
                        description="Net monthly cash flow swings unpredictably month-over-month.",
                        suggestion="Audit variable discretionary expenditures and establish fixed category caps.",
                    )
                )
            elif coef_var > 0.8:
                pts = 10
                risk_score += pts
                factors.append(
                    RiskFactorResult(
                        name="Moderate Cash Flow Fluctuations",
                        severity="medium",
                        impact_points=pts,
                        description="Noticeable variation in net cash flow across recent billing cycles.",
                        suggestion="Smooth seasonal expenses by amortizing annual bills into monthly savings.",
                    )
                )

        # Pillar 4: Savings Ratio
        if monthly_income > 0:
            net_savings = max(Decimal("0.00"), monthly_income - monthly_expenses)
            savings_ratio = (net_savings / monthly_income) * Decimal("100")
        else:
            savings_ratio = Decimal("0.00")

        if savings_ratio < Decimal("5.0"):
            pts = 15
            risk_score += pts
            factors.append(
                RiskFactorResult(
                    name="Very Low Savings Rate",
                    severity="high",
                    impact_points=pts,
                    description=f"Savings rate is currently {savings_ratio:.1f}% (benchmark: 20%+).",
                    suggestion="Adopt the 50/30/20 rule: 50% Needs, 30% Wants, 20% Savings.",
                )
            )
        elif savings_ratio < Decimal("15.0"):
            pts = 7
            risk_score += pts
            factors.append(
                RiskFactorResult(
                    name="Modest Savings Rate",
                    severity="medium",
                    impact_points=pts,
                    description=f"Savings rate is {savings_ratio:.1f}%. Target is 20% for long-term compounding.",
                    suggestion="Automate a 2-5% increase in monthly goal contributions.",
                )
            )

        # Clamp composite risk score [0, 100]
        final_risk_score = min(100, max(0, risk_score))
        overall_health_score = 100 - final_risk_score

        if final_risk_score < 25:
            risk_level = "Low"
            summary = "Your financial profile exhibits strong resilience, healthy buffers, and sustainable debt levels."
        elif final_risk_score < 50:
            risk_level = "Moderate"
            summary = "Your finances are stable, but optimizing your savings rate and emergency buffer will significantly improve durability."
        elif final_risk_score < 75:
            risk_level = "High"
            summary = "You have noticeable financial vulnerabilities. Elevated debt service or low reserves make you susceptible to unexpected shocks."
        else:
            risk_level = "Severe"
            summary = "Urgent financial restructuring recommended. Debt obligations and liquidity constraints require immediate action."

        return {
            "overall_health_score": overall_health_score,
            "risk_score": final_risk_score,
            "risk_level": risk_level,
            "savings_ratio": savings_ratio.quantize(Decimal("0.1")),
            "debt_to_income_ratio": dti.quantize(Decimal("0.1")),
            "emergency_runway_months": runway_months,
            "cash_flow_volatility_score": volatility_score,
            "summary_explanation": summary,
            "risk_factors": [f.to_dict() for f in factors],
        }
