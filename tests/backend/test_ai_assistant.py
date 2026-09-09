from decimal import Decimal
import pytest

from ai.assistant.service import FinancialAssistantService


def test_assistant_intent_detection():
    assert FinancialAssistantService.detect_intent("How much did I spend this month?") == "SPENDING_CURRENT_MONTH"
    assert FinancialAssistantService.detect_intent("Where is my highest expense category?") == "HIGHEST_EXPENSE_CATEGORY"
    assert FinancialAssistantService.detect_intent("How much can I save?") == "SAVINGS_POTENTIAL"
    assert FinancialAssistantService.detect_intent("What are my total EMI loans?") == "LOAN_OBLIGATIONS"
    assert FinancialAssistantService.detect_intent("Can I afford a $350 purchase?") == "AFFORDABILITY_CHECK"


def test_assistant_processing_with_disclaimer():
    context = {
        "monthly_spent": Decimal("1800.00"),
        "monthly_income": Decimal("5000.00"),
        "monthly_emi": Decimal("400.00"),
    }
    response = FinancialAssistantService.process_query("Can I afford $300?", user_context=context)

    assert response["detected_intent"] == "AFFORDABILITY_CHECK"
    assert "affordable" in response["answer"].lower()
    assert "disclaimer" in response
    assert "not provide regulated financial advice" in response["disclaimer"]
