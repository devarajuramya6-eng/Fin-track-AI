import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Plus, AlertTriangle, PieChart } from 'lucide-react';
import { budgetsApi, categoriesApi } from '../../api/endpoints';
import { Card } from '../../components/common/Card';
import { Button } from '../../components/common/Button';
import { Modal } from '../../components/common/Modal';
import { Input } from '../../components/common/Input';
import { Badge } from '../../components/common/Badge';
import { useAuth } from '../../contexts/AuthContext';
import { formatCurrency, getCurrencySymbol } from '../../utils/formatters';

export const Budgets: React.FC = () => {
  const { user } = useAuth();
  const currency = user?.preferred_currency || 'USD';
  const queryClient = useQueryClient();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [budgetName, setBudgetName] = useState('Monthly Operating Budget');
  const [totalLimit, setTotalLimit] = useState('3500');
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const { data: budget } = useQuery({
    queryKey: ['current-budget'],
    queryFn: () => budgetsApi.getCurrent().then((res) => res.data),
  });

  const { data: categories } = useQuery({
    queryKey: ['categories'],
    queryFn: () => categoriesApi.list().then((res) => res.data),
  });

  const createMutation = useMutation({
    mutationFn: (data: any) => budgetsApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['current-budget'] });
      setIsModalOpen(false);
      setErrorMessage(null);
    },
    onError: (err: any) => {
      setErrorMessage(err.response?.data?.detail || 'Failed to create budget. Please try again.');
    },
  });

  const handleCreate = (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage(null);
    const today = new Date();
    const firstDay = new Date(today.getFullYear(), today.getMonth(), 1).toISOString().split('T')[0];
    const lastDay = new Date(today.getFullYear(), today.getMonth() + 1, 0).toISOString().split('T')[0];

    const expenseCategories = (categories || []).filter((c) => c.category_type === 'expense');
    const allocationCount = Math.max(1, Math.min(6, expenseCategories.length));
    const perCatLimit = Math.round(Number(totalLimit) / allocationCount);

    const categoryAllocations = expenseCategories.slice(0, 6).map((c) => ({
      category_id: c.id,
      allocated_limit: perCatLimit,
      alert_threshold_percent: 85,
    }));

    createMutation.mutate({
      name: budgetName,
      period_type: 'monthly',
      start_date: firstDay,
      end_date: lastDay,
      total_budget_limit: Number(totalLimit),
      category_allocations: categoryAllocations,
    });
  };

  const percentUsed = budget && budget.total_budget_limit > 0
    ? Math.min(100, Math.round(((budget.total_spent || 0) / budget.total_budget_limit) * 100))
    : 0;

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-white">Budget Radar & Controls</h1>
          <p className="text-xs text-slate-500 dark:text-slate-400">Set spending caps, monitor threshold alerts, and avoid category overruns.</p>
        </div>
        <Button variant="primary" size="sm" onClick={() => setIsModalOpen(true)}>
          <Plus className="w-4 h-4 mr-1.5" />
          <span>Configure Budget</span>
        </Button>
      </div>

      {budget ? (
        <>
          {/* Overall Budget Progress */}
          <Card className="bg-gradient-to-br from-slate-50 via-white to-slate-100 dark:from-slate-900 dark:via-slate-900 dark:to-slate-950 border-slate-200 dark:border-slate-800">
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
              <div>
                <Badge variant={percentUsed > 90 ? 'danger' : percentUsed > 75 ? 'warning' : 'success'}>
                  {budget.name} ({budget.start_date} to {budget.end_date})
                </Badge>
                <div className="mt-3 flex items-baseline gap-2">
                  <span className="text-3xl font-extrabold text-slate-900 dark:text-white">
                    {formatCurrency(budget.total_spent || 0, currency)}
                  </span>
                  <span className="text-sm text-slate-500 dark:text-slate-400">
                    spent of {formatCurrency(budget.total_budget_limit, currency)} limit
                  </span>
                </div>
              </div>
              <div className="text-left sm:text-right">
                <span className="text-2xl font-bold text-emerald-600 dark:text-emerald-400">
                  {formatCurrency(budget.total_remaining || 0, currency)}
                </span>
                <p className="text-xs text-slate-500 dark:text-slate-400">Remaining Budget Balance</p>
              </div>
            </div>

            {/* Visual Progress Bar */}
            <div className="mt-6">
              <div className="flex justify-between text-xs text-slate-500 dark:text-slate-400 mb-1.5 font-medium">
                <span>Utilization Rate</span>
                <span>{percentUsed}%</span>
              </div>
              <div className="w-full bg-slate-200 dark:bg-slate-950 rounded-full h-3 overflow-hidden border border-slate-300 dark:border-slate-800">
                <div
                  className={`h-full rounded-full transition-all duration-500 ${
                    percentUsed > 90 ? 'bg-rose-500' : percentUsed > 75 ? 'bg-amber-500' : 'bg-emerald-500'
                  }`}
                  style={{ width: `${percentUsed}%` }}
                />
              </div>
            </div>
          </Card>

          {/* Category Envelopes Breakdown */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {budget.categories?.map((bCat) => {
              const catSpent = Number(bCat.spent_amount || 0);
              const catLimit = Number(bCat.allocated_limit);
              const catPercent = Math.min(100, Math.round((catSpent / (catLimit || 1)) * 100));
              const isOver = catSpent > catLimit;

              return (
                <Card key={bCat.id} className="border-slate-200 dark:border-slate-800">
                  <div className="flex items-center justify-between mb-3">
                    <span className="font-semibold text-slate-800 dark:text-slate-200 text-sm">{bCat.category?.name || 'Category'}</span>
                    <Badge variant={isOver ? 'danger' : catPercent > 80 ? 'warning' : 'neutral'}>
                      {catPercent}%
                    </Badge>
                  </div>

                  <div className="flex justify-between items-baseline mb-2">
                    <span className="text-lg font-bold text-slate-900 dark:text-white">{formatCurrency(catSpent, currency)}</span>
                    <span className="text-xs text-slate-500 dark:text-slate-400">of {formatCurrency(catLimit, currency)}</span>
                  </div>

                  <div className="w-full bg-slate-200 dark:bg-slate-950 rounded-full h-2 overflow-hidden border border-slate-300 dark:border-slate-800">
                    <div
                      className={`h-full rounded-full ${
                        isOver ? 'bg-rose-500' : catPercent > 80 ? 'bg-amber-500' : 'bg-emerald-500'
                      }`}
                      style={{ width: `${catPercent}%` }}
                    />
                  </div>

                  {isOver && (
                    <div className="mt-3 flex items-center text-xs text-rose-500 dark:text-rose-400 font-medium">
                      <AlertTriangle className="w-3.5 h-3.5 mr-1 flex-shrink-0" />
                      <span>Exceeded limit by {formatCurrency(catSpent - catLimit, currency)}</span>
                    </div>
                  )}
                </Card>
              );
            })}
          </div>
        </>
      ) : (
        <Card className="text-center py-12">
          <PieChart className="w-12 h-12 text-slate-400 dark:text-slate-600 mx-auto mb-3" />
          <h3 className="text-lg font-semibold text-slate-900 dark:text-white">No Active Budget Found</h3>
          <p className="text-xs text-slate-500 dark:text-slate-400 max-w-sm mx-auto mt-1 leading-relaxed">
            Create your first monthly budget to establish automated spending envelopes and threshold alarms.
          </p>
          <Button variant="primary" size="sm" className="mt-4" onClick={() => setIsModalOpen(true)}>
            Initialize Budget
          </Button>
        </Card>
      )}

      {/* Modal */}
      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Configure Monthly Budget">
        <form onSubmit={handleCreate} className="space-y-4">
          {errorMessage && (
            <div className="p-3 bg-rose-500/10 border border-rose-500/20 text-rose-500 dark:text-rose-400 text-xs rounded-lg">
              {errorMessage}
            </div>
          )}
          <Input
            label="Budget Name"
            type="text"
            required
            value={budgetName}
            onChange={(e) => setBudgetName(e.target.value)}
          />
          <Input
            label={`Total Monthly Spending Limit (${getCurrencySymbol(currency)})`}
            type="number"
            required
            value={totalLimit}
            onChange={(e) => setTotalLimit(e.target.value)}
          />
          <Button type="submit" variant="primary" className="w-full" isLoading={createMutation.isPending}>
            Activate Budget Radar
          </Button>
        </form>
      </Modal>
    </div>
  );
};
