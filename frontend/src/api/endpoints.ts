import api from './client';
import {
  User,
  Account,
  Transaction,
  Category,
  Budget,
  SavingsGoal,
  Loan,
  InvestmentPortfolio,
  Holding,
  RiskScore,
  Anomaly,
  Notification,
  Recommendation,
  DashboardSummary,
} from '../types';

export const authApi = {
  login: (data: FormData) => api.post('/auth/login', data, { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }),
  register: (data: { email: string; password: string; full_name: string; preferred_currency?: string }) =>
    api.post<User>('/auth/register', data),
  logout: () => api.post('/auth/logout'),
  getProfile: () => api.get<User>('/users/me'),
  updateProfile: (data: Partial<User>) => api.put<User>('/users/me', data),
};

export const accountsApi = {
  list: () => api.get<Account[]>('/accounts/'),
  create: (data: Partial<Account> & { initial_balance?: number }) => api.post<Account>('/accounts/', data),
  get: (id: number) => api.get<Account>(`/accounts/${id}`),
  delete: (id: number) => api.delete(`/accounts/${id}`),
};

export const transactionsApi = {
  list: (params?: Record<string, any>) => api.get<Transaction[]>('/transactions/', { params }),
  create: (data: Partial<Transaction>) => api.post<Transaction>('/transactions/', data),
  update: (id: number, data: Partial<Transaction>) => api.put<Transaction>(`/transactions/${id}`, data),
  delete: (id: number) => api.delete(`/transactions/${id}`),
  importCsv: (accountId: number, csvContent: string) =>
    api.post<{ message: string; imported_count: number }>('/transactions/import-csv', null, {
      params: { account_id: accountId, csv_content: csvContent },
    }),
};

export const categoriesApi = {
  list: () => api.get<Category[]>('/categories/'),
  create: (data: Partial<Category>) => api.post<Category>('/categories/', data),
};

export const budgetsApi = {
  getCurrent: () => api.get<Budget | null>('/budgets/current'),
  create: (data: any) => api.post<Budget>('/budgets/', data),
};

export const savingsApi = {
  list: () => api.get<SavingsGoal[]>('/savings/'),
  create: (data: Partial<SavingsGoal>) => api.post<SavingsGoal>('/savings/', data),
  contribute: (goalId: number, data: { amount: number; contribution_date: string; notes?: string }) =>
    api.post(`/savings/${goalId}/contribute`, data),
};

export const loansApi = {
  list: () => api.get<Loan[]>('/loans/'),
  create: (data: any) => api.post<Loan>('/loans/', data),
  simulatePrepayment: (loanId: number, data: { extra_amount: number; action: string }) =>
    api.post(`/loans/${loanId}/simulate-prepayment`, data),
};

export const investmentsApi = {
  getPortfolio: () => api.get<InvestmentPortfolio>('/investments/portfolio'),
  addHolding: (data: any) => api.post<Holding>('/investments/holdings', data),
  updateValuation: (holdingId: number, data: { current_price: number; valuation_date: string }) =>
    api.put<Holding>(`/investments/holdings/${holdingId}/valuation`, data),
};

export const reportsApi = {
  getDashboardSummary: () => api.get<DashboardSummary>('/reports/dashboard-summary'),
  getCashFlow: (months = 6) => api.get<any[]>('/reports/cash-flow', { params: { months } }),
  getSpendingByCategory: () => api.get<any[]>('/reports/spending-by-category'),
};

export const aiApi = {
  queryAssistant: (query: string) => api.post<any>('/ai/query', { query }),
  getRiskScore: () => api.get<RiskScore>('/risk/score'),
  getAnomalies: () => api.get<Anomaly[]>('/anomalies/'),
  getForecasting: (periods = 3) => api.get<any>('/forecasting/cashflow', { params: { periods } }),
  getRecommendations: () => api.get<Recommendation[]>('/recommendations/'),
};

export const notificationsApi = {
  list: () => api.get<Notification[]>('/notifications/'),
  markRead: (id: number) => api.put<Notification>(`/notifications/${id}/read`),
};

export const adminApi = {
  getTelemetry: () => api.get<any>('/admin/telemetry'),
  listUsers: () => api.get<User[]>('/admin/users'),
  getAuditLogs: () => api.get<any[]>('/audit/logs'),
};
