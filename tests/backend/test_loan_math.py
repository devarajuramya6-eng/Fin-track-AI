from datetime import date
from decimal import Decimal
import pytest

from backend.app.services.loan_service import LoanCalculationService


def test_emi_standard_calculation():
    # Principal: $10,000, 12% APR, 12 Months
    # Monthly rate: 1%
    # EMI = [10000 * 0.01 * (1.01^12)] / [(1.01^12) - 1] = 888.49
    principal = Decimal("10000.00")
    rate = Decimal("12.0")
    tenure = 12

    emi = LoanCalculationService.calculate_emi(principal, rate, tenure)
    assert emi == Decimal("888.49")


def test_emi_zero_interest():
    principal = Decimal("12000.00")
    rate = Decimal("0.0")
    tenure = 12

    emi = LoanCalculationService.calculate_emi(principal, rate, tenure)
    assert emi == Decimal("1000.00")


def test_amortization_schedule_completeness():
    principal = Decimal("5000.00")
    rate = Decimal("10.0")
    tenure = 6
    start = date(2026, 1, 1)

    emi, total_interest, schedule = LoanCalculationService.generate_amortization_schedule(
        principal, rate, tenure, start
    )

    assert len(schedule) == 6
    assert schedule[-1].ending_balance == Decimal("0.00")
    total_principal_paid = sum(item.principal_component for item in schedule)
    assert total_principal_paid == principal
    assert total_interest > Decimal("0.00")


def test_prepayment_simulation_reduce_tenure():
    principal = Decimal("20000.00")
    rate = Decimal("8.0")
    tenure = 60
    prepayment = Decimal("5000.00")

    result = LoanCalculationService.simulate_prepayment(
        principal, rate, tenure, prepayment, action="reduce_tenure"
    )

    assert result.months_saved > 0
    assert result.new_tenure_months < tenure
    assert result.interest_savings > Decimal("0.00")
