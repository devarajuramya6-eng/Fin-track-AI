from datetime import date
from decimal import ROUND_HALF_UP, Decimal

from backend.app.schemas.loan import (
    AmortizationScheduleItem,
    PrepaymentSimulationResult,
)
from dateutil.relativedelta import relativedelta


class LoanCalculationService:
    """
    Precision financial calculation engine for Equated Monthly Installments (EMI),
    interest amortization, balance tracking, and prepayment modeling.
    Uses standard Banker's and Financial Rounding with Python Decimal to prevent floating point drift.
    """

    @staticmethod
    def calculate_emi(principal: Decimal, annual_interest_rate: Decimal, tenure_months: int) -> Decimal:
        """
        Calculates monthly EMI using standard compounding formula:
        EMI = [P x R x (1+R)^N] / [(1+R)^N - 1]
        where:
          P = Principal loan amount
          R = Monthly interest rate (Annual Rate / 12 / 100)
          N = Number of monthly installments
        """
        if principal <= 0 or tenure_months <= 0:
            return Decimal("0.00")

        if annual_interest_rate <= 0:
            emi = principal / Decimal(tenure_months)
            return emi.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        monthly_rate = (annual_interest_rate / Decimal("100")) / Decimal("12")
        factor = (Decimal("1") + monthly_rate) ** tenure_months
        emi = (principal * monthly_rate * factor) / (factor - Decimal("1"))
        return emi.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    @classmethod
    def generate_amortization_schedule(
        cls,
        principal: Decimal,
        annual_interest_rate: Decimal,
        tenure_months: int,
        start_date: date,
    ) -> tuple[Decimal, Decimal, list[AmortizationScheduleItem]]:
        """
        Generates full monthly amortization table:
        Returns (Calculated EMI, Total Interest, Schedule Items)
        """
        emi = cls.calculate_emi(principal, annual_interest_rate, tenure_months)
        monthly_rate = (annual_interest_rate / Decimal("100")) / Decimal("12")

        balance = principal
        schedule: list[AmortizationScheduleItem] = []
        total_interest = Decimal("0.00")

        for month in range(1, tenure_months + 1):
            installment_due_date = start_date + relativedelta(months=month)
            interest_component = (balance * monthly_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

            # For the final month, handle any small fractional cent rounding adjustments
            if month == tenure_months or balance <= (emi - interest_component):
                principal_component = balance
                current_emi = principal_component + interest_component
                ending_balance = Decimal("0.00")
            else:
                principal_component = (emi - interest_component).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                current_emi = emi
                ending_balance = (balance - principal_component).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

            total_interest += interest_component

            schedule.append(
                AmortizationScheduleItem(
                    installment_number=month,
                    due_date=installment_due_date,
                    beginning_balance=balance,
                    emi_amount=current_emi,
                    principal_component=principal_component,
                    interest_component=interest_component,
                    ending_balance=ending_balance,
                    is_settled=False,
                )
            )

            balance = ending_balance
            if balance <= 0:
                break

        return emi, total_interest, schedule

    @classmethod
    def simulate_prepayment(
        cls,
        principal: Decimal,
        annual_interest_rate: Decimal,
        tenure_months: int,
        extra_amount: Decimal,
        action: str = "reduce_tenure",
    ) -> PrepaymentSimulationResult:
        """
        Simulates one-time lumpsum prepayment:
        - action='reduce_tenure': keeps EMI constant, shortens payoff timeline.
        - action='reduce_emi': recalculates lower EMI over original tenure.
        """
        original_emi = cls.calculate_emi(principal, annual_interest_rate, tenure_months)
        _, original_interest, _ = cls.generate_amortization_schedule(
            principal, annual_interest_rate, tenure_months, date.today()
        )

        reduced_principal = max(Decimal("0.00"), principal - extra_amount)
        monthly_rate = (annual_interest_rate / Decimal("100")) / Decimal("12")

        if action == "reduce_emi":
            new_emi = cls.calculate_emi(reduced_principal, annual_interest_rate, tenure_months)
            _, new_total_interest, _ = cls.generate_amortization_schedule(
                reduced_principal, annual_interest_rate, tenure_months, date.today()
            )
            interest_savings = max(Decimal("0.00"), original_interest - new_total_interest)
            return PrepaymentSimulationResult(
                original_tenure_months=tenure_months,
                new_tenure_months=tenure_months,
                months_saved=0,
                original_total_interest=original_interest,
                new_total_interest=new_total_interest,
                interest_savings=interest_savings,
                new_emi=new_emi,
            )
        else:
            # Keep original EMI, find new tenure
            bal = reduced_principal
            months_count = 0
            new_interest = Decimal("0.00")
            while bal > Decimal("0.00") and months_count < tenure_months:
                months_count += 1
                interest = (bal * monthly_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                new_interest += interest
                principal_paid = original_emi - interest
                if bal <= principal_paid:
                    bal = Decimal("0.00")
                else:
                    bal -= principal_paid

            interest_savings = max(Decimal("0.00"), original_interest - new_interest)
            months_saved = max(0, tenure_months - months_count)

            return PrepaymentSimulationResult(
                original_tenure_months=tenure_months,
                new_tenure_months=months_count,
                months_saved=months_saved,
                original_total_interest=original_interest,
                new_total_interest=new_interest,
                interest_savings=interest_savings,
                new_emi=original_emi,
            )
