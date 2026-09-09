from decimal import Decimal
from typing import Dict, List


class RecommendationEngine:
    """
    Deterministic financial hygiene recommendation engine.
    Analyzes cash flows, debt ratios, savings milestones, and emergency buffers to generate
    prioritized, actionable recommendations.
    """

    @classmethod
    def generate_recommendations(
        cls,
        monthly_income: Decimal,
        monthly_expenses: Decimal,
        liquid_savings: Decimal,
        monthly_debt: Decimal,
    ) -> List[Dict]:
        recommendations = []

        # 1. Emergency Fund Rule
        monthly_burn = monthly_expenses if monthly_expenses > 0 else Decimal("1000.00")
        runway = liquid_savings / monthly_burn
        if runway < Decimal("3.0"):
            recommendations.append({
                "category": "emergency_fund",
                "title": "Build Minimum 3-Month Emergency Buffer",
                "summary": (
                    f"Your liquid savings currently provide {runway:.1f} months of living expenses. "
                    "Establish a target emergency fund covering at least 3 to 6 months of non-negotiable living costs."
                ),
                "impact_estimate": f"Protect against unexpected shocks up to ${(monthly_burn * Decimal('3.0')):,.2f}",
                "priority": "urgent" if runway < Decimal("1.0") else "high",
            })

        # 2. Debt-to-Income Optimization Rule
        if monthly_income > 0:
            dti = (monthly_debt / monthly_income) * Decimal("100")
            if dti > Decimal("36.0"):
                recommendations.append({
                    "category": "debt",
                    "title": "Accelerate High-Interest Debt Repayment",
                    "summary": (
                        f"Your monthly debt payments consume {dti:.1f}% of income, exceeding the recommended 36% ceiling. "
                        "Consider utilizing the debt avalanche strategy to reduce high-interest loans."
                    ),
                    "impact_estimate": "Lower debt-to-income ratio below 35% within 12 months",
                    "priority": "high",
                })

        # 3. Savings Rate Rule (50/30/20)
        if monthly_income > 0:
            net_savings = max(Decimal("0.00"), monthly_income - monthly_expenses)
            savings_pct = (net_savings / monthly_income) * Decimal("100")
            if savings_pct < Decimal("20.0"):
                recommendations.append({
                    "category": "budgeting",
                    "title": "Optimize Discretionary Spending to Reach 20% Savings",
                    "summary": (
                        f"Your current savings rate is {savings_pct:.1f}%. Increasing your monthly allocation by "
                        f"${(monthly_income * Decimal('0.05')):,.2f} will significantly compound long-term wealth."
                    ),
                    "impact_estimate": f"+${(monthly_income * Decimal('0.05') * Decimal('12')):,.2f} annual savings increase",
                    "priority": "medium",
                })

        # 4. Investment Diversification Rule
        recommendations.append({
            "category": "investment",
            "title": "Maintain Balanced Asset Allocation",
            "summary": "Review portfolio diversification across equities, fixed income, and cash reserves on a quarterly basis.",
            "impact_estimate": "Mitigate single-asset volatility risks",
            "priority": "low",
        })

        return recommendations
