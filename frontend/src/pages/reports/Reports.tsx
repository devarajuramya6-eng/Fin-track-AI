import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { reportsApi } from '../../api/endpoints';
import { Card } from '../../components/common/Card';
import { CashFlowChart } from '../../components/charts/CashFlowChart';
import { SpendingDonutChart } from '../../components/charts/SpendingDonutChart';
import { useAuth } from '../../contexts/AuthContext';
import { formatCurrency } from '../../utils/formatters';

export const Reports: React.FC = () => {
  const { user } = useAuth();
  const currency = user?.preferred_currency || 'USD';
  const [months, setMonths] = useState(6);

  const { data: cashFlow } = useQuery({
    queryKey: ['cash-flow-report', months],
    queryFn: () => reportsApi.getCashFlow(months).then((res) => res.data),
  });

  const { data: categorySpend } = useQuery({
    queryKey: ['spending-by-category'],
    queryFn: () => reportsApi.getSpendingByCategory().then((res) => res.data),
  });

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-white">Financial Intelligence Reports</h1>
          <p className="text-xs text-slate-500 dark:text-slate-400">Periodic cash flow statements, category expense distributions, and net trends.</p>
        </div>
        <div className="flex items-center gap-3">
          <select
            value={months}
            onChange={(e) => setMonths(Number(e.target.value))}
            className="bg-slate-50 dark:bg-slate-900 border border-slate-300 dark:border-slate-800 rounded-lg px-3 py-1.5 text-xs text-slate-900 dark:text-slate-100 focus:outline-none focus:border-emerald-500"
          >
            <option value={3}>Last 3 Months</option>
            <option value={6}>Last 6 Months</option>
            <option value={12}>Last 12 Months</option>
          </select>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card title="Cash Flow Statement" subtitle="Inflow vs Outflow Historical Trend">
          <CashFlowChart data={cashFlow || []} />
        </Card>

        <Card title="Expense Category Concentration" subtitle="Distribution of monthly non-investment outflows">
          <SpendingDonutChart data={categorySpend || []} />
        </Card>
      </div>

      {/* Cash Flow Statement Ledger Table */}
      <Card title="Monthly Cash Flow Breakdown" subtitle="Detailed table of historical monthly financial statements">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-200 dark:border-slate-800 text-slate-500 dark:text-slate-400 uppercase tracking-wider font-semibold">
                <th className="pb-3">Period</th>
                <th className="pb-3 text-right">Total Inflow (Income)</th>
                <th className="pb-3 text-right">Total Outflow (Expenses)</th>
                <th className="pb-3 text-right">Net Savings Surplus</th>
                <th className="pb-3 text-right">Savings Rate</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200 dark:divide-slate-800/60">
              {cashFlow?.map((row, idx) => {
                const savingsRate = row.income > 0 ? ((row.net / row.income) * 100).toFixed(1) : '0.0';
                return (
                  <tr key={idx} className="hover:bg-slate-100/50 dark:hover:bg-slate-800/30 transition">
                    <td className="py-3 font-semibold text-slate-800 dark:text-slate-200">{row.period}</td>
                    <td className="py-3 text-right font-bold text-emerald-600 dark:text-emerald-400">{formatCurrency(row.income, currency)}</td>
                    <td className="py-3 text-right font-bold text-rose-600 dark:text-rose-400">{formatCurrency(row.expense, currency)}</td>
                    <td className={`py-3 text-right font-extrabold ${row.net >= 0 ? 'text-emerald-600 dark:text-emerald-400' : 'text-rose-600 dark:text-rose-400'}`}>
                      {formatCurrency(row.net, currency)}
                    </td>
                    <td className="py-3 text-right font-medium text-slate-700 dark:text-slate-300">{savingsRate}%</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
};
