import React from 'react';
import { useQuery } from '@tanstack/react-query';
import {
  Wallet,
  TrendingUp,
  CreditCard,
  PiggyBank,
  ShieldAlert,
  ArrowUpRight,
  ArrowDownRight,
  Sparkles,
  PlusCircle,
} from 'lucide-react';
import { reportsApi, transactionsApi, aiApi } from '../../api/endpoints';
import { Card } from '../../components/common/Card';
import { Button } from '../../components/common/Button';
import { Badge } from '../../components/common/Badge';
import { Skeleton } from '../../components/common/Skeleton';
import { CashFlowChart } from '../../components/charts/CashFlowChart';
import { SpendingDonutChart } from '../../components/charts/SpendingDonutChart';
import { Link } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { formatCurrency } from '../../utils/formatters';

export const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const currency = user?.preferred_currency || 'USD';

  const { data: summary, isLoading: isSummaryLoading } = useQuery({
    queryKey: ['dashboard-summary'],
    queryFn: () => reportsApi.getDashboardSummary().then((res) => res.data),
  });

  const { data: cashFlow, isLoading: isCashFlowLoading } = useQuery({
    queryKey: ['cash-flow'],
    queryFn: () => reportsApi.getCashFlow(6).then((res) => res.data),
  });

  const { data: categorySpend } = useQuery({
    queryKey: ['spending-by-category'],
    queryFn: () => reportsApi.getSpendingByCategory().then((res) => res.data),
  });

  const { data: recentTxs } = useQuery({
    queryKey: ['recent-transactions'],
    queryFn: () => transactionsApi.list({ limit: 5 }).then((res) => res.data),
  });

  const { data: riskScore } = useQuery({
    queryKey: ['risk-score'],
    queryFn: () => aiApi.getRiskScore().then((res) => res.data),
  });

  const { data: recommendations } = useQuery({
    queryKey: ['recommendations'],
    queryFn: () => aiApi.getRecommendations().then((res) => res.data),
  });

  return (
    <div className="space-y-6">
      {/* Top Banner & Quick Action */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-white">Financial Command Center</h1>
          <p className="text-xs text-slate-500 dark:text-slate-400">Live consolidated overview of assets, liabilities, and local AI intelligence.</p>
        </div>
        <div className="flex items-center gap-3">
          <Link to="/transactions">
            <Button variant="primary" size="sm">
              <PlusCircle className="w-4 h-4 mr-1.5" />
              <span>Add Transaction</span>
            </Button>
          </Link>
        </div>
      </div>

      {/* KPI Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Net Worth */}
        <Card className="border-l-4 border-l-emerald-500">
          <div className="flex items-center justify-between text-xs text-slate-500 dark:text-slate-400 mb-1">
            <span>Net Worth</span>
            <Wallet className="w-4 h-4 text-emerald-500 dark:text-emerald-400" />
          </div>
          {isSummaryLoading ? (
            <Skeleton className="h-8 w-32 mt-1" />
          ) : (
            <div className="text-2xl font-bold text-slate-900 dark:text-white tracking-tight">
              {formatCurrency(summary?.net_worth ?? 0, currency)}
            </div>
          )}
          <div className="mt-2 flex items-center text-xs text-emerald-600 dark:text-emerald-400 font-medium">
            <ArrowUpRight className="w-3.5 h-3.5 mr-0.5" />
            <span>Liquid Cash + Portfolio - Debt</span>
          </div>
        </Card>

        {/* Liquid Cash */}
        <Card className="border-l-4 border-l-blue-500">
          <div className="flex items-center justify-between text-xs text-slate-500 dark:text-slate-400 mb-1">
            <span>Liquid Bank Balances</span>
            <PiggyBank className="w-4 h-4 text-blue-500 dark:text-blue-400" />
          </div>
          {isSummaryLoading ? (
            <Skeleton className="h-8 w-32 mt-1" />
          ) : (
            <div className="text-2xl font-bold text-slate-900 dark:text-white tracking-tight">
              {formatCurrency(summary?.total_cash ?? 0, currency)}
            </div>
          )}
          <div className="mt-2 text-xs text-slate-500 dark:text-slate-400">
            Across checking & savings accounts
          </div>
        </Card>

        {/* Investments */}
        <Card className="border-l-4 border-l-purple-500">
          <div className="flex items-center justify-between text-xs text-slate-500 dark:text-slate-400 mb-1">
            <span>Invested Assets</span>
            <TrendingUp className="w-4 h-4 text-purple-500 dark:text-purple-400" />
          </div>
          {isSummaryLoading ? (
            <Skeleton className="h-8 w-32 mt-1" />
          ) : (
            <div className="text-2xl font-bold text-slate-900 dark:text-white tracking-tight">
              {formatCurrency(summary?.total_investments ?? 0, currency)}
            </div>
          )}
          <div className="mt-2 text-xs text-slate-500 dark:text-slate-400">
            Manual portfolio market valuation
          </div>
        </Card>

        {/* Outstanding Liabilities */}
        <Card className="border-l-4 border-l-rose-500">
          <div className="flex items-center justify-between text-xs text-slate-500 dark:text-slate-400 mb-1">
            <span>Loan Liabilities</span>
            <CreditCard className="w-4 h-4 text-rose-500 dark:text-rose-400" />
          </div>
          {isSummaryLoading ? (
            <Skeleton className="h-8 w-32 mt-1" />
          ) : (
            <div className="text-2xl font-bold text-slate-900 dark:text-white tracking-tight">
              {formatCurrency(summary?.total_debt ?? 0, currency)}
            </div>
          )}
          <div className="mt-2 flex items-center text-xs text-rose-600 dark:text-rose-400 font-medium">
            <ArrowDownRight className="w-3.5 h-3.5 mr-0.5" />
            <span>Active loan obligations</span>
          </div>
        </Card>
      </div>

      {/* Main Charts & Risk Engine Split */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Cash Flow Statement Chart */}
        <div className="lg:col-span-2">
          <Card title="Cash Flow Dynamics" subtitle="Income vs Expense Trajectory over past 6 billing periods">
            {isCashFlowLoading ? <Skeleton className="h-72 w-full" /> : <CashFlowChart data={cashFlow || []} />}
          </Card>
        </div>

        {/* AI Financial Health & Risk Gauge */}
        <div>
          <Card
            title="Financial Risk Radar"
            subtitle="Calculated on-device by Explainable AI"
            action={
              <Link to="/risk">
                <Button variant="ghost" size="sm" className="text-xs text-emerald-600 dark:text-emerald-400">
                  Full Audit
                </Button>
              </Link>
            }
          >
            <div className="flex flex-col items-center justify-center p-4 bg-slate-100 dark:bg-slate-950/60 rounded-xl border border-slate-200 dark:border-slate-800">
              <div className="relative flex items-center justify-center">
                <div className="w-28 h-28 rounded-full border-4 border-slate-300 dark:border-slate-800 flex items-center justify-center">
                  <div className="text-center">
                    <span className="text-3xl font-extrabold text-emerald-600 dark:text-emerald-400">
                      {riskScore?.overall_health_score || 78}
                    </span>
                    <span className="text-slate-400 dark:text-slate-500 text-xs block font-bold">/ 100</span>
                  </div>
                </div>
              </div>
              <div className="mt-4 text-center">
                <Badge variant={riskScore?.risk_level === 'Low' ? 'success' : 'warning'}>
                  {riskScore?.risk_level || 'Low'} Risk Rating
                </Badge>
                <p className="text-xs text-slate-600 dark:text-slate-400 mt-2 leading-relaxed">
                  {riskScore?.summary_explanation || 'Your financial health indicates solid liquidity buffers and manageable obligations.'}
                </p>
              </div>
            </div>

            <div className="mt-4 space-y-2 text-xs">
              <div className="flex justify-between py-1 border-b border-slate-200 dark:border-slate-800/60">
                <span className="text-slate-500 dark:text-slate-400">Debt-to-Income (DTI):</span>
                <span className="font-semibold text-slate-800 dark:text-slate-200">{riskScore?.debt_to_income_ratio || '12.5'}%</span>
              </div>
              <div className="flex justify-between py-1 border-b border-slate-200 dark:border-slate-800/60">
                <span className="text-slate-500 dark:text-slate-400">Emergency Buffer:</span>
                <span className="font-semibold text-slate-800 dark:text-slate-200">{riskScore?.emergency_runway_months || '4.2'} Months</span>
              </div>
            </div>
          </Card>
        </div>
      </div>

      {/* Spending Breakdown & Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Category Breakdown Donut */}
        <div>
          <Card title="Monthly Category Allocation" subtitle="Current billing cycle expenditures">
            <SpendingDonutChart data={categorySpend || []} />
          </Card>
        </div>

        {/* Recent Transactions Ledger */}
        <div className="lg:col-span-2">
          <Card
            title="Recent Ledger Activity"
            subtitle="Latest transactions recorded across all accounts"
            action={
              <Link to="/transactions" className="text-xs text-emerald-600 dark:text-emerald-400 hover:underline">
                View All Ledger Entries
              </Link>
            }
          >
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead>
                  <tr className="border-b border-slate-200 dark:border-slate-800 text-slate-500 dark:text-slate-400 uppercase tracking-wider font-semibold">
                    <th className="pb-3">Date</th>
                    <th className="pb-3">Merchant / Payee</th>
                    <th className="pb-3">Category</th>
                    <th className="pb-3 text-right">Amount</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-200 dark:divide-slate-800/60">
                  {recentTxs && recentTxs.length > 0 ? (
                    recentTxs.map((tx) => (
                      <tr key={tx.id} className="hover:bg-slate-100/50 dark:hover:bg-slate-800/30 transition">
                        <td className="py-3 text-slate-500 dark:text-slate-400">{tx.transaction_date}</td>
                        <td className="py-3 font-medium text-slate-800 dark:text-slate-200">{tx.payee_or_merchant}</td>
                        <td className="py-3">
                          <span className="px-2 py-0.5 rounded-full bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300 font-medium">
                            {tx.category?.name || 'General'}
                          </span>
                        </td>
                        <td className={`py-3 text-right font-bold ${tx.transaction_type === 'income' ? 'text-emerald-600 dark:text-emerald-400' : 'text-slate-900 dark:text-slate-100'}`}>
                          {tx.transaction_type === 'income' ? '+' : '-'}{formatCurrency(Number(tx.amount), currency)}
                        </td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan={4} className="py-6 text-center text-slate-500">
                        No transactions found. Click "Add Transaction" to record your first entry.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </Card>
        </div>
      </div>

      {/* AI Prescriptive Recommendations Banner */}
      {recommendations && recommendations.length > 0 && (
        <Card className="bg-gradient-to-r from-slate-900 via-slate-900 to-emerald-950/30 border-emerald-500/20">
          <div className="flex items-start gap-4">
            <div className="p-2.5 bg-emerald-500/10 text-emerald-400 rounded-xl border border-emerald-500/20 mt-1">
              <Sparkles className="w-5 h-5" />
            </div>
            <div className="flex-1">
              <div className="flex items-center gap-2">
                <h3 className="font-semibold text-white text-sm">AI Financial Copilot Insight</h3>
                <Badge variant="success">Local Intelligence</Badge>
              </div>
              <p className="font-medium text-slate-200 text-sm mt-1">{recommendations[0].title}</p>
              <p className="text-xs text-slate-400 mt-1 leading-relaxed">{recommendations[0].summary}</p>
            </div>
            <Link to="/ai-assistant">
              <Button variant="secondary" size="sm" className="whitespace-nowrap">
                Chat with Copilot
              </Button>
            </Link>
          </div>
        </Card>
      )}
    </div>
  );
};
