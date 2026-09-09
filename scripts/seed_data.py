#!/usr/bin/env python3
"""
Realistic Demo Data Generator for AI FinTech Platform.
Generates fictional accounts, categories, transactions, budgets, savings goals,
loans, investments, notifications, and risk audit logs for local developer testing.
"""

import sys
import random
from pathlib import Path
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal

# Add root directory to sys.path
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

from backend.app.db.session import sync_engine, SyncSessionLocal
from backend.app.db.base import Base
from backend.app.core.security import get_password_hash
from backend.app.models import (
    User,
    Role,
    Permission,
    UserRole,
    Account,
    TransactionCategory,
    Transaction,
    Budget,
    BudgetCategory,
    SavingsGoal,
    SavingsContribution,
    Loan,
    LoanAmortization,
    Investment,
    InvestmentHolding,
    InvestmentTransaction,
    Notification,
    NotificationPreference,
    FinancialScore,
    RiskFactor,
    Anomaly,
    AuditLog,
)
from backend.app.services.loan_service import LoanCalculationService
from backend.app.api.v1.categories import DEFAULT_CATEGORIES


def seed_database():
    print("=" * 70)
    print(" AI FinTech Platform — Seeding Realistic Demo Data")
    print("=" * 70)

    # Ensure tables exist
    Base.metadata.create_all(bind=sync_engine)
    session = SyncSessionLocal()

    try:
        # 1. Create Roles
        admin_role = session.query(Role).filter_by(name="admin").first()
        if not admin_role:
            admin_role = Role(name="admin", description="Full system administrative privileges")
            user_role = Role(name="user", description="Standard fintech account holder")
            session.add_all([admin_role, user_role])
            session.flush()

        # 2. Create Demo User
        demo_email = "demo.user@fintech.local"
        demo_user = session.query(User).filter_by(email=demo_email).first()
        if not demo_user:
            demo_user = User(
                email=demo_email,
                hashed_password=get_password_hash("DemoPassword123!"),
                full_name="Alex Mercer",
                preferred_currency="USD",
                timezone="America/New_York",
                is_active=True,
                is_superuser=True,
            )
            session.add(demo_user)
            session.flush()

            session.add(UserRole(user_id=demo_user.id, role_id=admin_role.id))
            session.add(NotificationPreference(user_id=demo_user.id))
            session.flush()
            print(f"[+] Created Demo Superuser: {demo_email}")

        # 3. Create Categories
        categories = {}
        for cat_data in DEFAULT_CATEGORIES:
            cat = session.query(TransactionCategory).filter_by(name=cat_data["name"]).first()
            if not cat:
                cat = TransactionCategory(
                    name=cat_data["name"],
                    category_type=cat_data["category_type"],
                    icon=cat_data["icon"],
                    color=cat_data["color"],
                    is_system=True,
                )
                session.add(cat)
                session.flush()
            categories[cat.name] = cat
        print(f"[+] Seeded {len(categories)} transaction categories.")

        # 4. Create Accounts
        accounts = {}
        acc_defs = [
            ("Primary Checking", "checking", "Chase Bank", "1042", Decimal("6450.00"), "#3b82f6"),
            ("High-Yield Savings", "savings", "Marcus by Goldman", "8821", Decimal("28500.00"), "#10b981"),
            ("Sapphire Credit Card", "credit_card", "Chase", "4491", Decimal("1240.00"), "#f43f5e"),
            ("Physical Cash Vault", "cash", "Cash Reserve", None, Decimal("400.00"), "#f59e0b"),
        ]
        for name, a_type, inst, mask, bal, col in acc_defs:
            acc = session.query(Account).filter_by(user_id=demo_user.id, name=name).first()
            if not acc:
                acc = Account(
                    user_id=demo_user.id,
                    name=name,
                    account_type=a_type,
                    institution_name=inst,
                    account_number_mask=mask,
                    currency="USD",
                    current_balance=bal,
                    color=col,
                    is_active=True,
                )
                session.add(acc)
                session.flush()
            accounts[name] = acc
        print(f"[+] Seeded {len(accounts)} financial accounts.")

        # 5. Create Realistic Transactions over past 90 days
        tx_count = session.query(Transaction).filter_by(user_id=demo_user.id).count()
        if tx_count < 10:
            today = date.today()
            sample_merchants = [
                ("Whole Foods Market", "Groceries & Food", Decimal("124.50"), "expense", "card"),
                ("Trader Joe's", "Groceries & Food", Decimal("86.20"), "expense", "card"),
                ("Metro Transit Pass", "Transportation & Fuel", Decimal("120.00"), "expense", "card"),
                ("Shell Gas Station", "Transportation & Fuel", Decimal("48.00"), "expense", "card"),
                ("City Electric Utility", "Utilities & Bills", Decimal("145.00"), "expense", "bank_transfer"),
                ("High-Speed Fiber Internet", "Utilities & Bills", Decimal("80.00"), "expense", "card"),
                ("Blue Bottle Coffee", "Dining Out & Cafes", Decimal("14.50"), "expense", "card"),
                ("The Italian Kitchen", "Dining Out & Cafes", Decimal("68.00"), "expense", "card"),
                ("StreamFlix & Music Sub", "Entertainment & Leisure", Decimal("29.99"), "expense", "card"),
                ("Tech Employer Payroll", "Salary & Income", Decimal("4250.00"), "income", "bank_transfer"),
                ("Quarterly Stock Dividend", "Investments & Dividends", Decimal("310.00"), "income", "bank_transfer"),
            ]

            created_txs = 0
            for day_offset in range(90, -1, -3):
                tx_date = today - timedelta(days=day_offset)
                # Bi-weekly salary
                if day_offset % 14 == 0:
                    t_inc = Transaction(
                        user_id=demo_user.id,
                        account_id=accounts["Primary Checking"].id,
                        category_id=categories["Salary & Income"].id,
                        amount=Decimal("4250.00"),
                        transaction_type="income",
                        transaction_date=tx_date,
                        payee_or_merchant="Tech Employer Payroll",
                        payment_method="bank_transfer",
                    )
                    session.add(t_inc)
                    created_txs += 1

                # Pick random expense
                m_name, c_name, amt, t_type, p_method = random.choice(sample_merchants)
                if t_type == "expense":
                    t_exp = Transaction(
                        user_id=demo_user.id,
                        account_id=accounts["Primary Checking"].id,
                        category_id=categories[c_name].id,
                        amount=amt + Decimal(str(random.randint(0, 20))),
                        transaction_type="expense",
                        transaction_date=tx_date,
                        payee_or_merchant=m_name,
                        payment_method=p_method,
                    )
                    session.add(t_exp)
                    created_txs += 1

            session.flush()
            print(f"[+] Generated {created_txs} realistic historical transactions.")

        # 6. Create Monthly Budget
        first_day = date.today().replace(day=1)
        last_day = (first_day + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        budget = session.query(Budget).filter_by(user_id=demo_user.id).first()
        if not budget:
            budget = Budget(
                user_id=demo_user.id,
                name="Monthly Operating Radar",
                period_type="monthly",
                start_date=first_day,
                end_date=last_day,
                total_budget_limit=Decimal("3800.00"),
                is_active=True,
            )
            session.add(budget)
            session.flush()

            budget_cats = [
                ("Housing & Rent", Decimal("1400.00")),
                ("Groceries & Food", Decimal("600.00")),
                ("Transportation & Fuel", Decimal("350.00")),
                ("Utilities & Bills", Decimal("300.00")),
                ("Dining Out & Cafes", Decimal("350.00")),
                ("Entertainment & Leisure", Decimal("200.00")),
            ]
            for cat_name, limit in budget_cats:
                if cat_name in categories:
                    session.add(
                        BudgetCategory(
                            budget_id=budget.id,
                            category_id=categories[cat_name].id,
                            allocated_limit=limit,
                            alert_threshold_percent=85,
                        )
                    )
            session.flush()
            print("[+] Seeded active monthly budget and category limits.")

        # 7. Create Savings Goals
        goal = session.query(SavingsGoal).filter_by(user_id=demo_user.id).first()
        if not goal:
            g1 = SavingsGoal(
                user_id=demo_user.id,
                name="6-Month Emergency Fund",
                goal_category="emergency_fund",
                target_amount=Decimal("30000.00"),
                current_amount=Decimal("28500.00"),
                target_date=date.today() + timedelta(days=90),
                color="#10b981",
            )
            g2 = SavingsGoal(
                user_id=demo_user.id,
                name="House Downpayment Fund",
                goal_category="house",
                target_amount=Decimal("80000.00"),
                current_amount=Decimal("35000.00"),
                target_date=date.today() + timedelta(days=500),
                color="#3b82f6",
            )
            session.add_all([g1, g2])
            session.flush()
            print("[+] Seeded savings milestone goals.")

        # 8. Create Loan & Amortization
        loan = session.query(Loan).filter_by(user_id=demo_user.id).first()
        if not loan:
            principal = Decimal("25000.00")
            rate = Decimal("6.5")
            tenure = 48
            start = date.today() - timedelta(days=180)
            emi, total_interest, schedule = LoanCalculationService.generate_amortization_schedule(
                principal, rate, tenure, start
            )
            loan = Loan(
                user_id=demo_user.id,
                loan_name="Vehicle Purchase Loan",
                loan_type="auto",
                lender_name="Credit Union Auto Finance",
                principal_amount=principal,
                annual_interest_rate=rate,
                tenure_months=tenure,
                start_date=start,
                calculated_emi=emi,
                total_interest=total_interest,
                total_repayment=principal + total_interest,
                outstanding_balance=Decimal("21800.00"),
                is_active=True,
            )
            session.add(loan)
            session.flush()

            for item in schedule[:12]:
                session.add(
                    LoanAmortization(
                        loan_id=loan.id,
                        installment_number=item.installment_number,
                        due_date=item.due_date,
                        beginning_balance=item.beginning_balance,
                        emi_amount=item.emi_amount,
                        principal_component=item.principal_component,
                        interest_component=item.interest_component,
                        ending_balance=item.ending_balance,
                        is_settled=item.installment_number <= 6,
                    )
                )
            session.flush()
            print("[+] Seeded auto loan with calculated amortization schedule.")

        # 9. Create Investment Portfolio & Holdings
        portfolio = session.query(Investment).filter_by(user_id=demo_user.id).first()
        if not portfolio:
            portfolio = Investment(
                user_id=demo_user.id,
                portfolio_name="Core Long-Term Wealth Portfolio",
                description="Diversified index funds and equities.",
            )
            session.add(portfolio)
            session.flush()

            holdings_def = [
                ("VTI", "Vanguard Total Stock Market ETF", "etf", Decimal("50"), Decimal("210.00"), Decimal("265.00")),
                ("VXUS", "Vanguard Total International Stock ETF", "etf", Decimal("80"), Decimal("55.00"), Decimal("64.00")),
                ("BND", "Vanguard Total Bond Market ETF", "bond", Decimal("60"), Decimal("72.00"), Decimal("76.50")),
                ("GLD", "SPDR Gold Shares", "gold", Decimal("15"), Decimal("180.00"), Decimal("220.00")),
                ("AAPL", "Apple Inc.", "stock", Decimal("25"), Decimal("165.00"), Decimal("215.00")),
            ]

            for sym, h_name, a_cls, qty, buy_p, curr_p in holdings_def:
                inv_val = (qty * buy_p).quantize(Decimal("0.01"))
                mkt_val = (qty * curr_p).quantize(Decimal("0.01"))
                pnl = mkt_val - inv_val
                ret_pct = ((pnl / inv_val) * Decimal("100")).quantize(Decimal("0.01"))
                h = InvestmentHolding(
                    investment_id=portfolio.id,
                    asset_symbol=sym,
                    asset_name=h_name,
                    asset_class=a_cls,
                    quantity=qty,
                    average_buy_price=buy_p,
                    current_price=curr_p,
                    total_invested_value=inv_val,
                    current_market_value=mkt_val,
                    unrealized_profit_loss=pnl,
                    return_percentage=ret_pct,
                    last_valuation_date=date.today(),
                )
                session.add(h)
            session.flush()
            print("[+] Seeded diversified investment portfolio with manual valuations.")

        # 10. Audit Log Initial Checkpoint
        session.add(
            AuditLog(
                user_id=demo_user.id,
                action="SYSTEM_SEED_INITIALIZED",
                entity_type="System",
                details="Realistic demo database initialized successfully.",
            )
        )

        session.commit()
        print("=" * 70)
        print("[SUCCESS] All demo data generated and committed cleanly!")
        print("=" * 70)

    except Exception as e:
        session.rollback()
        print(f"[ERROR] Database seeding failed: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    seed_database()
