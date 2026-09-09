# AI FinTech Personal Finance & Risk Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-emerald.svg)](LICENSE)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![React 18](https://img.shields.io/badge/React-18-cyan.svg)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-blue.svg)](https://www.typescriptlang.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-teal.svg)](https://fastapi.tiangolo.com/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.4-sky.svg)](https://tailwindcss.com/)
[![Zero API Keys Required](https://img.shields.io/badge/External%20APIs-None%20Required-success.svg)](#)

A comprehensive, privacy-first, full-stack personal finance management and risk intelligence web platform. Built by a solo developer, the application runs **100% locally with zero external API key requirements**.

---

## Key Features

- **Personal Finance Dashboard**: Net worth, liquid assets, debt obligations, financial health score, and spending trends.
- **Transaction Ledger**: Filter, search, sort, categorize, and tag transactions. Supports CSV import/export and duplicate detection.
- **Budget Control Engine**: Category spend limits, historical variance, and early overspending threshold alerts.
- **Savings Goals Engine**: Target milestone tracking, required monthly contributions, and time-to-goal projections.
- **Loan & EMI Calculator**: Full amortization schedules, interest vs principal breakdown, and prepayment simulation.
- **Investment Portfolio**: Manual portfolio tracking across Stocks, Mutual Funds, ETFs, Bonds, and Gold with asset allocation breakdown.
- **Local AI Financial Assistant**: Rule-based natural language assistant answering spending questions and calculating affordability without external LLM APIs.
- **Statistical Anomaly Detection**: Outlier detection using Z-score and Interquartile Range (IQR) algorithms.
- **Explainable Financial Risk Scoring**: 0–100 composite risk score analyzing DTI, emergency runway, and spending volatility.
- **Predictive Cash Flow Forecasting**: Local statistical time-series projections for upcoming expenses and income.
- **In-App Notification Center**: Real-time alerts for budget limits, loan payments, and financial health updates.
- **Admin Control Panel**: User management, system metrics telemetry, and audit trail viewer.

---

## Technology Stack

- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS, TanStack Query, React Router, Lucide Icons, Recharts.
- **Backend**: Python 3.12, FastAPI, Pydantic v2, SQLAlchemy 2.0, Alembic, Uvicorn.
- **Database**: PostgreSQL 16 (with zero-config SQLite fallback for instant standalone development).
- **AI / ML**: NumPy, pandas, scikit-learn, statistical engines (all locally executed).
- **Quality & Testing**: Pytest, Vitest, Ruff, Prettier, ESLint.
- **DevOps**: Docker, Docker Compose, Nginx, GitHub Actions CI.

---

## Quickstart

### Option 1: Docker Compose (Recommended)
```bash
# 1. Clone the repository and navigate into it
cd fintech

# 2. Copy environment configuration
cp .env.example .env

# 3. Launch platform
docker compose up --build -d
```
- Frontend: [http://localhost:5173](http://localhost:5173)
- Backend Docs (Swagger): [http://localhost:8000/docs](http://localhost:8000/docs)

### Option 2: Standalone Local Development (No Docker)
```bash
# 1. Backend Setup
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py

# 2. Frontend Setup (In a separate terminal)
cd ../frontend
npm install
npm run dev
```

---

## Meaningful LOC & Code Quality
The platform is designed toward a target of **500,000+ meaningful lines of code** with real functionality.
To inspect genuine code metrics excluding dependencies and build files:
```bash
python scripts/count_loc.py
```

To run the automated license compliance audit:
```bash
python scripts/check_licenses.py
```

---

## License
Released under the [MIT License](LICENSE).
All dependencies verified under permissive licenses in [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).
