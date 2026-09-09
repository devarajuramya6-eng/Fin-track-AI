import React from 'react';
import { ResponsiveContainer, PieChart, Pie, Cell, Tooltip } from 'recharts';
import { useAuth } from '../../contexts/AuthContext';
import { useTheme } from '../../contexts/ThemeContext';
import { formatCurrency } from '../../utils/formatters';

interface CategorySpend {
  category: string;
  color: string;
  amount: number;
}

interface SpendingDonutChartProps {
  data: CategorySpend[];
}

export const SpendingDonutChart: React.FC<SpendingDonutChartProps> = ({ data }) => {
  const { user } = useAuth();
  const { theme } = useTheme();
  const currency = user?.preferred_currency || 'USD';
  const isDark = theme === 'dark';

  if (!data || data.length === 0) {
    return (
      <div className="h-64 flex items-center justify-center text-slate-400 dark:text-slate-500 text-sm">
        No expense data recorded this month.
      </div>
    );
  }

  return (
    <div className="w-full h-64 flex items-center">
      <div className="w-1/2 h-full">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              dataKey="amount"
              nameKey="category"
              cx="50%"
              cy="50%"
              innerRadius={55}
              outerRadius={80}
              paddingAngle={4}
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color || '#3b82f6'} />
              ))}
            </Pie>
            <Tooltip
              contentStyle={{
                backgroundColor: isDark ? '#0f172a' : '#ffffff',
                borderColor: isDark ? '#334155' : '#cbd5e1',
                borderRadius: '8px',
                fontSize: '12px',
                color: isDark ? '#f8fafc' : '#0f172a',
              }}
              formatter={(val: any) => [formatCurrency(Number(val), currency), '']}
            />
          </PieChart>
        </ResponsiveContainer>
      </div>

      <div className="w-1/2 pl-4 space-y-2 overflow-y-auto max-h-60">
        {data.map((item, idx) => (
          <div key={idx} className="flex items-center justify-between text-xs">
            <div className="flex items-center gap-2 truncate">
              <span className="w-2.5 h-2.5 rounded-full flex-shrink-0" style={{ backgroundColor: item.color }} />
              <span className="text-slate-700 dark:text-slate-300 truncate">{item.category}</span>
            </div>
            <span className="font-semibold text-slate-900 dark:text-slate-200">{formatCurrency(item.amount, currency)}</span>
          </div>
        ))}
      </div>
    </div>
  );
};
