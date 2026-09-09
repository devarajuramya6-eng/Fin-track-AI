import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Plus, DollarSign, Calendar, TrendingUp } from 'lucide-react';
import { savingsApi } from '../../api/endpoints';
import { Card } from '../../components/common/Card';
import { Button } from '../../components/common/Button';
import { Modal } from '../../components/common/Modal';
import { Input } from '../../components/common/Input';
import { Badge } from '../../components/common/Badge';
import { useAuth } from '../../contexts/AuthContext';
import { formatCurrency, getCurrencySymbol } from '../../utils/formatters';

export const Savings: React.FC = () => {
  const { user } = useAuth();
  const currency = user?.preferred_currency || 'USD';
  const queryClient = useQueryClient();
  const [isGoalModalOpen, setIsGoalModalOpen] = useState(false);
  const [isContribModalOpen, setIsContribModalOpen] = useState(false);
  const [selectedGoalId, setSelectedGoalId] = useState<number | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  // New Goal Form
  const [name, setName] = useState('');
  const [goalCategory, setGoalCategory] = useState('emergency_fund');
  const [targetAmount, setTargetAmount] = useState('');
  const [currentAmount, setCurrentAmount] = useState('0');
  const [targetDate, setTargetDate] = useState(
    new Date(new Date().setFullYear(new Date().getFullYear() + 1)).toISOString().split('T')[0]
  );

  // Contribution Form
  const [contribAmount, setContribAmount] = useState('');
  const [contribNotes, setContribNotes] = useState('');

  const { data: goals } = useQuery({
    queryKey: ['savings-goals'],
    queryFn: () => savingsApi.list().then((res) => res.data),
  });

  const createGoalMutation = useMutation({
    mutationFn: (data: any) => savingsApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['savings-goals'] });
      setIsGoalModalOpen(false);
      setErrorMessage(null);
      setName('');
      setTargetAmount('');
      setCurrentAmount('0');
    },
    onError: (err: any) => {
      setErrorMessage(err.response?.data?.detail || 'Failed to create savings goal. Please try again.');
    },
  });

  const contributeMutation = useMutation({
    mutationFn: ({ goalId, data }: { goalId: number; data: any }) =>
      savingsApi.contribute(goalId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['savings-goals'] });
      setIsContribModalOpen(false);
      setContribAmount('');
      setErrorMessage(null);
    },
    onError: (err: any) => {
      setErrorMessage(err.response?.data?.detail || 'Failed to record contribution.');
    },
  });

  const handleCreateGoal = (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage(null);
    createGoalMutation.mutate({
      name,
      goal_category: goalCategory,
      target_amount: Number(targetAmount),
      current_amount: Number(currentAmount),
      target_date: targetDate,
    });
  };

  const handleContribute = (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedGoalId || !contribAmount) return;
    setErrorMessage(null);
    contributeMutation.mutate({
      goalId: selectedGoalId,
      data: {
        amount: Number(contribAmount),
        contribution_date: new Date().toISOString().split('T')[0],
        notes: contribNotes || undefined,
      },
    });
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-white">Savings Milestones</h1>
          <p className="text-xs text-slate-500 dark:text-slate-400">Target funds, required monthly contributions, and time-to-goal projections.</p>
        </div>
        <Button variant="primary" size="sm" onClick={() => setIsGoalModalOpen(true)}>
          <Plus className="w-4 h-4 mr-1.5" />
          <span>New Savings Goal</span>
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {goals?.map((goal) => {
          const progress = Math.min(100, Math.round((Number(goal.current_amount) / (Number(goal.target_amount) || 1)) * 100));

          return (
            <Card key={goal.id} className="border-slate-200 dark:border-slate-800 flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between mb-3">
                  <Badge variant={goal.is_completed ? 'success' : 'neutral'}>
                    {goal.goal_category.replace('_', ' ').toUpperCase()}
                  </Badge>
                  <span className="text-xs text-slate-500 dark:text-slate-400 flex items-center">
                    <Calendar className="w-3.5 h-3.5 mr-1" />
                    {goal.target_date}
                  </span>
                </div>

                <h3 className="font-bold text-slate-900 dark:text-white text-base">{goal.name}</h3>

                <div className="mt-4 flex justify-between items-baseline">
                  <span className="text-2xl font-extrabold text-emerald-600 dark:text-emerald-400">
                    {formatCurrency(Number(goal.current_amount), currency)}
                  </span>
                  <span className="text-xs text-slate-500 dark:text-slate-400">
                    of {formatCurrency(Number(goal.target_amount), currency)} target
                  </span>
                </div>

                {/* Progress bar */}
                <div className="mt-3">
                  <div className="w-full bg-slate-200 dark:bg-slate-950 rounded-full h-2.5 overflow-hidden border border-slate-300 dark:border-slate-800">
                    <div
                      className="h-full rounded-full bg-emerald-500 transition-all duration-500"
                      style={{ width: `${progress}%` }}
                    />
                  </div>
                  <div className="mt-1 flex justify-between text-xs text-slate-500 dark:text-slate-400">
                    <span>{progress}% Achieved</span>
                    <span>Remaining: {formatCurrency(Math.max(0, Number(goal.target_amount) - Number(goal.current_amount)), currency)}</span>
                  </div>
                </div>

                {/* Monthly projection formula */}
                {!goal.is_completed && (
                  <div className="mt-4 p-3 bg-slate-100 dark:bg-slate-950/60 rounded-lg border border-slate-200 dark:border-slate-800/80 text-xs text-slate-700 dark:text-slate-300">
                    <div className="flex items-center gap-1.5 text-emerald-600 dark:text-emerald-400 font-semibold mb-1">
                      <TrendingUp className="w-3.5 h-3.5" />
                      <span>Required Monthly Savings</span>
                    </div>
                    <p className="text-slate-500 dark:text-slate-400">
                      Deposit <strong className="text-slate-900 dark:text-slate-100">{formatCurrency(Number(goal.required_monthly_savings || 0), currency)}/mo</strong> to hit target by milestone date.
                    </p>
                  </div>
                )}
              </div>

              <div className="mt-5 pt-4 border-t border-slate-200 dark:border-slate-800 flex items-center justify-between">
                <Button
                  variant="secondary"
                  size="sm"
                  className="w-full"
                  onClick={() => {
                    setSelectedGoalId(goal.id);
                    setIsContribModalOpen(true);
                  }}
                >
                  <DollarSign className="w-4 h-4 mr-1 text-emerald-600 dark:text-emerald-400" />
                  <span>Log Contribution</span>
                </Button>
              </div>
            </Card>
          );
        })}
      </div>

      {/* New Goal Modal */}
      <Modal isOpen={isGoalModalOpen} onClose={() => setIsGoalModalOpen(false)} title="Create New Savings Goal">
        <form onSubmit={handleCreateGoal} className="space-y-4">
          {errorMessage && (
            <div className="p-3 bg-rose-500/10 border border-rose-500/20 text-rose-500 dark:text-rose-400 text-xs rounded-lg">
              {errorMessage}
            </div>
          )}
          <Input
            label="Goal Name"
            type="text"
            required
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="e.g. 6-Month Emergency Runway"
          />

          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-700 dark:text-slate-300 mb-1.5">
              Goal Category
            </label>
            <select
              value={goalCategory}
              onChange={(e) => setGoalCategory(e.target.value)}
              className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-900 dark:text-slate-100 focus:outline-none focus:border-emerald-500"
            >
              <option value="emergency_fund">Emergency Fund</option>
              <option value="house">House Downpayment</option>
              <option value="vehicle">Vehicle Purchase</option>
              <option value="travel">Vacation & Travel</option>
              <option value="education">Education & Learning</option>
              <option value="retirement">Retirement Growth</option>
              <option value="custom">Custom Goal</option>
            </select>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <Input
              label={`Target Amount (${getCurrencySymbol(currency)})`}
              type="number"
              required
              value={targetAmount}
              onChange={(e) => setTargetAmount(e.target.value)}
              placeholder="10000"
            />
            <Input
              label={`Starting Balance (${getCurrencySymbol(currency)})`}
              type="number"
              value={currentAmount}
              onChange={(e) => setCurrentAmount(e.target.value)}
              placeholder="0"
            />
          </div>

          <Input
            label="Target Completion Date"
            type="date"
            required
            value={targetDate}
            onChange={(e) => setTargetDate(e.target.value)}
          />

          <Button type="submit" variant="primary" className="w-full mt-2" isLoading={createGoalMutation.isPending}>
            Establish Savings Milestone
          </Button>
        </form>
      </Modal>

      {/* Contribution Modal */}
      <Modal isOpen={isContribModalOpen} onClose={() => setIsContribModalOpen(false)} title="Log Goal Deposit">
        <form onSubmit={handleContribute} className="space-y-4">
          {errorMessage && (
            <div className="p-3 bg-rose-500/10 border border-rose-500/20 text-rose-500 dark:text-rose-400 text-xs rounded-lg">
              {errorMessage}
            </div>
          )}
          <Input
            label={`Contribution Amount (${getCurrencySymbol(currency)})`}
            type="number"
            step="0.01"
            required
            value={contribAmount}
            onChange={(e) => setContribAmount(e.target.value)}
            placeholder="250.00"
          />
          <Input
            label="Deposit Notes"
            type="text"
            value={contribNotes}
            onChange={(e) => setContribNotes(e.target.value)}
            placeholder="e.g. Monthly transfer from checking"
          />
          <Button type="submit" variant="primary" className="w-full" isLoading={contributeMutation.isPending}>
            Record Deposit
          </Button>
        </form>
      </Modal>
    </div>
  );
};
