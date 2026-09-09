import re
from decimal import Decimal
from typing import Any, Dict, Optional


class FinancialAssistantService:
    """
    Local AI-Style Financial Assistant.
    Operates completely without external commercial AI APIs.
    Combines regex entity extraction, intent classification, and template generation.
    """

    INTENT_PATTERNS = [
        (r"(spend|spent|expense|costs?).*(this month|current month)", "SPENDING_CURRENT_MONTH"),
        (r"(highest|most|largest|top).*(spend|expense|category)", "HIGHEST_EXPENSE_CATEGORY"),
        (r"(how much|can i).*(save|saving)", "SAVINGS_POTENTIAL"),
        (r"(emi|loan|debt|obligations?)", "LOAN_OBLIGATIONS"),
        (r"(risk|health score|financial health)", "RISK_EXPLANATION"),
        (r"(afford|buy|purchase).*\$?([0-9]+)", "AFFORDABILITY_CHECK"),
        (r"(reduce|cut down|trim).*(spending|costs?|expenses?)", "REDUCE_SPENDING_TIPS"),
    ]

    @classmethod
    def detect_intent(cls, query: str) -> str:
        query_clean = query.lower().strip()
        for pattern, intent in cls.INTENT_PATTERNS:
            if re.search(pattern, query_clean):
                return intent
        return "GENERAL_INQUIRY"

    @classmethod
    def process_query(
        cls,
        query: str,
        user_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        intent = cls.detect_intent(query)
        ctx = user_context or {}

        monthly_spent = ctx.get("monthly_spent", Decimal("2450.00"))
        top_category = ctx.get("top_category", "Housing & Rent")
        top_category_amount = ctx.get("top_category_amount", Decimal("1200.00"))
        monthly_income = ctx.get("monthly_income", Decimal("4500.00"))
        monthly_emi = ctx.get("monthly_emi", Decimal("650.00"))
        risk_score = ctx.get("risk_score", 32)
        emergency_months = ctx.get("emergency_months", Decimal("3.5"))

        if intent == "SPENDING_CURRENT_MONTH":
            answer = (
                f"Your total spending for the current month is ${monthly_spent:,.2f}. "
                f"Against your monthly income of ${monthly_income:,.2f}, this represents "
                f"{(monthly_spent / monthly_income * 100):.1f}% of your inflow."
            )
            data = {"monthly_spent": float(monthly_spent), "monthly_income": float(monthly_income)}
            suggestion = "Check the Budgets page to ensure individual categories stay within your targets."

        elif intent == "HIGHEST_EXPENSE_CATEGORY":
            pct = (top_category_amount / monthly_spent * 100) if monthly_spent > 0 else 0
            answer = (
                f"Your highest spending category this month is **{top_category}** totaling "
                f"${top_category_amount:,.2f}, which accounts for {pct:.1f}% of all outflows."
            )
            data = {"top_category": top_category, "amount": float(top_category_amount), "percentage": float(pct)}
            suggestion = f"Consider setting a dedicated budget cap for {top_category} in the Budgets section."

        elif intent == "SAVINGS_POTENTIAL":
            potential_savings = max(Decimal("0.00"), monthly_income - monthly_spent - monthly_emi)
            savings_pct = (potential_savings / monthly_income * 100) if monthly_income > 0 else 0
            answer = (
                f"Based on your income of ${monthly_income:,.2f} and current expenditures, "
                f"your estimated unallocated cash flow is **${potential_savings:,.2f}** ({savings_pct:.1f}%). "
                f"Financial best practice suggests saving at least 20% (${(monthly_income * Decimal('0.20')):,.2f})."
            )
            data = {"potential_savings": float(potential_savings), "target_20_percent": float(monthly_income * Decimal("0.20"))}
            suggestion = "You can route this surplus toward your active Savings Goals or Emergency Fund."

        elif intent == "LOAN_OBLIGATIONS":
            dti = (monthly_emi / monthly_income * 100) if monthly_income > 0 else 0
            answer = (
                f"Your total monthly EMI obligation across all active loans is **${monthly_emi:,.2f}**. "
                f"This consumes {dti:.1f}% of your gross monthly income (healthy benchmark is under 36%)."
            )
            data = {"monthly_emi": float(monthly_emi), "dti_percentage": float(dti)}
            suggestion = "Use the Loan Amortization & Prepayment tool to explore how small extra payments save interest."

        elif intent == "RISK_EXPLANATION":
            answer = (
                f"Your current Financial Risk Score is **{risk_score}/100** (Moderate). "
                f"Your liquid emergency fund covers approximately {emergency_months} months of necessary expenses. "
                f"Maintaining 3–6 months is recommended to protect against income disruption."
            )
            data = {"risk_score": risk_score, "emergency_runway_months": float(emergency_months)}
            suggestion = "Review the Risk Analysis dashboard to inspect detailed breakdown factors."

        elif intent == "AFFORDABILITY_CHECK":
            match = re.search(r"\$?([0-9]+)", query)
            target_amount = Decimal(match.group(1)) if match else Decimal("200")
            surplus = monthly_income - monthly_spent - monthly_emi
            is_affordable = surplus >= target_amount

            if is_affordable:
                answer = (
                    f"A purchase of **${target_amount:,.2f}** appears affordable within your current monthly cash flow. "
                    f"You have a projected monthly buffer of ${surplus:,.2f}."
                )
            else:
                deficit = target_amount - surplus
                answer = (
                    f"A purchase of **${target_amount:,.2f}** would exceed your unallocated monthly surplus by "
                    f"${deficit:,.2f}. Consider spreading this across multiple savings cycles."
                )
            data = {"target_amount": float(target_amount), "projected_surplus": float(surplus), "is_affordable": is_affordable}
            suggestion = "Create a dedicated short-term savings goal for non-essential purchases."

        elif intent == "REDUCE_SPENDING_TIPS":
            answer = (
                "Here are 3 high-impact strategies based on your spending profile:\n"
                "1. **Audit Recurring Subscriptions**: Review monthly auto-debits on credit cards.\n"
                "2. **Implement Category Envelopes**: Put hard weekly caps on Dining and Entertainment.\n"
                "3. **Batch Discretionary Purchases**: Apply a 48-hour cooling-off rule on non-essential buys."
            )
            data = {}
            suggestion = "Set an alert threshold of 80% on discretionary categories in the Budgets section."

        else:
            answer = (
                "I am your local AI Financial Assistant. I can help analyze your spending, check category totals, "
                "calculate savings potential, assess debt burdens, or test if you can afford an upcoming purchase.\n\n"
                "Try asking:\n"
                "- *'How much did I spend this month?'*\n"
                "- *'Where did I spend the most?'*\n"
                "- *'How much can I save?'*\n"
                "- *'What is my financial risk?'*\n"
                "- *'Can I afford a $450 expense?'*"
            )
            data = {}
            suggestion = "Ask any personal finance or budget calculation question above."

        return {
            "detected_intent": intent,
            "answer": answer,
            "calculated_data": data,
            "action_suggestion": suggestion,
            "disclaimer": (
                "Educational estimate only. This platform does not provide regulated financial advice. "
                "Calculations should be independently verified before making major financial commitments."
            ),
        }
