export interface User {
  id: number;
  email: string;
  full_name: string;
  is_active: boolean;
  is_superuser: boolean;
  preferred_currency: string;
  timezone: string;
  created_at: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

export interface Account {
  id: number;
  user_id: number;
  name: string;
  account_type: 'checking' | 'savings' | 'credit_card' | 'cash' | 'investment' | 'loan' | 'other';
  institution_name?: string;
  account_number_mask?: string;
  currency: string;
  current_balance: number;
  is_active: boolean;
  color: string;
  created_at: string;
}

export interface Category {
  id: number;
  name: string;
  category_type: 'income' | 'expense' | 'transfer';
  icon?: string;
  color?: string;
  parent_id?: number;
  is_system: boolean;
}

export interface Transaction {
  id: number;
  user_id: number;
  account_id: number;
  category_id: number;
  amount: number;
  transaction_type: 'income' | 'expense' | 'transfer';
  transaction_date: string;
  payee_or_merchant: string;
  description?: string;
  notes?: string;
  payment_method: string;
  is_recurring: boolean;
  is_excluded_from_budget: boolean;
  reference_number?: string;
  created_at: string;
  category?: Category;
}

export interface BudgetCategory {
  id: number;
  budget_id: number;
  category_id: number;
  allocated_limit: number;
  alert_threshold_percent: number;
  category?: Category;
  spent_amount?: number;
  remaining_amount?: number;
  percentage_used?: number;
}

export interface Budget {
  id: number;
  user_id: number;
  name: string;
  period_type: string;
  start_date: string;
  end_date: string;
  total_budget_limit: number;
  is_active: boolean;
  created_at: string;
  categories: BudgetCategory[];
  total_spent?: number;
  total_remaining?: number;
}

export interface SavingsContribution {
  id: number;
  goal_id: number;
  amount: number;
  contribution_date: string;
  notes?: string;
  created_at: string;
}

export interface SavingsGoal {
  id: number;
  user_id: number;
  name: string;
  goal_category: string;
  target_amount: number;
  current_amount: number;
  target_date: string;
  is_completed: boolean;
  color: string;
  notes?: string;
  created_at: string;
  progress_percentage?: number;
  required_monthly_savings?: number;
  contributions?: SavingsContribution[];
}

export interface AmortizationScheduleItem {
  installment_number: number;
  due_date: string;
  beginning_balance: number;
  emi_amount: number;
  principal_component: number;
  interest_component: number;
  ending_balance: number;
  is_settled: boolean;
}

export interface Loan {
  id: number;
  user_id: number;
  loan_name: string;
  loan_type: string;
  lender_name: string;
  principal_amount: number;
  annual_interest_rate: number;
  tenure_months: number;
  start_date: string;
  calculated_emi: number;
  total_interest: number;
  total_repayment: number;
  outstanding_balance: number;
  is_active: boolean;
  created_at: string;
  amortization_schedule?: AmortizationScheduleItem[];
}

export interface Holding {
  id: number;
  investment_id: number;
  asset_symbol: string;
  asset_name: string;
  asset_class: string;
  quantity: number;
  average_buy_price: number;
  current_price: number;
  total_invested_value: number;
  current_market_value: number;
  unrealized_profit_loss: number;
  return_percentage: number;
  last_valuation_date: string;
  created_at: string;
}

export interface InvestmentPortfolio {
  id: number;
  user_id: number;
  portfolio_name: string;
  description?: string;
  total_invested_amount: number;
  total_current_value: number;
  total_unrealized_gain_loss: number;
  overall_return_percentage: number;
  holdings: Holding[];
  asset_allocation: Record<string, number>;
}

export interface RiskFactor {
  id: number;
  factor_name: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  impact_points: number;
  description: string;
  mitigation_suggestion: string;
}

export interface RiskScore {
  overall_health_score: number;
  risk_score: number;
  risk_level: string;
  savings_ratio: number;
  debt_to_income_ratio: number;
  emergency_runway_months: number;
  cash_flow_volatility_score: number;
  summary_explanation: string;
  risk_factors: RiskFactor[];
}

export interface Anomaly {
  id: number;
  transaction_id?: number;
  anomaly_type: string;
  severity: string;
  detection_method: string;
  score_value: number;
  description: string;
  is_resolved: boolean;
  created_at: string;
}

export interface Notification {
  id: number;
  user_id: number;
  title: string;
  message: string;
  notification_type: string;
  severity: 'info' | 'warning' | 'success' | 'error';
  link_url?: string;
  is_read: boolean;
  created_at: string;
}

export interface Recommendation {
  id: number;
  category: string;
  title: string;
  summary: string;
  impact_estimate?: string;
  priority: string;
  is_applied: boolean;
}

export interface DashboardSummary {
  total_cash: number;
  total_investments: number;
  total_debt: number;
  net_worth: number;
  month_to_date_income: number;
  month_to_date_expenses: number;
  net_monthly_savings: number;
}
