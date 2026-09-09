import React from 'react';
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from 'recharts';
import { useAuth } from '../../contexts/AuthContext';
import { useTheme } from '../../contexts/ThemeContext';
import { formatCurrency, getCurrencySymbol } from '../../utils/formatters';

interface CashFlowDataPoint {
  period: string;
  income: number;
  expense: number;
  net: number;
}

interface CashFlowChartProps {
  data: CashFlowDataPoint[];
}

export const CashFlowChart: React.FC<CashFlowChartProps> = ({ data }) => {
  const { user } = useAuth();
  const { theme } = useTheme();
  const currency = user?.preferred_currency || 'USD';
  const isDark = theme === 'dark';

  return (
    <div className="w-full h-72">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
          <defs>
            <linearGradient id="incomeGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#10b981" stopOpacity={0.4} />
              <stop offset="95%" stopColor="#10b981" stopOpacity={0.0} />
            </linearGradient>
            <linearGradient id="expenseGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#f43f5e" stopOpacity={0.4} />
              <stop offset="95%" stopColor="#f43f5e" stopOpacity={0.0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke={isDark ? '#334155' : '#e2e8f0'} vertical={false} />
          <XAxis dataKey="period" stroke={isDark ? '#94a3b8' : '#64748b'} fontSize={12} tickLine={false} />
          <YAxis
            stroke={isDark ? '#94a3b8' : '#64748b'}
            fontSize={12}
            tickLine={false}
            tickFormatter={(val) => `${getCurrencySymbol(currency)}${val}`}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: isDark ? '#0f172a' : '#ffffff',
              borderColor: isDark ? '#334155' : '#cbd5e1',
              borderRadius: '8px',
              fontSize: '12px',
              color: isDark ? '#f8fafc' : '#0f172a',
            }}
            formatter={(value: any) => [formatCurrency(Number(value), currency), '']}
          />
          <Area
            type="monotone"
            dataKey="income"
            name="Income"
            stroke="#10b981"
            strokeWidth={2}
            fillOpacity={1}
            fill="url(#incomeGrad)"
          />
          <Area
            type="monotone"
            dataKey="expense"
            name="Expense"
            stroke="#f43f5e"
            strokeWidth={2}
            fillOpacity={1}
            fill="url(#expenseGrad)"
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
};
