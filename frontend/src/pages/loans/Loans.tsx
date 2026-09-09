import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Plus, Sparkles, ShieldCheck } from 'lucide-react';
import { loansApi } from '../../api/endpoints';
import { Card } from '../../components/common/Card';
import { Button } from '../../components/common/Button';
import { Modal } from '../../components/common/Modal';
import { Input } from '../../components/common/Input';
import { Badge } from '../../components/common/Badge';
import { useAuth } from '../../contexts/AuthContext';
import { formatCurrency, getCurrencySymbol } from '../../utils/formatters';

export const Loans: React.FC = () => {
  const { user } = useAuth();
  const currency = user?.preferred_currency || 'USD';
  const queryClient = useQueryClient();
  const [isNewLoanModalOpen, setIsNewLoanModalOpen] = useState(false);
  const [isSimModalOpen, setIsSimModalOpen] = useState(false);
  const [selectedLoan, setSelectedLoan] = useState<any>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  // New Loan Form
  const [loanName, setLoanName] = useState('');
  const [loanType, setLoanType] = useState('personal');
  const [lenderName, setLenderName] = useState('');
  const [principal, setPrincipal] = useState('15000');
  const [rate, setRate] = useState('7.5');
  const [tenure, setTenure] = useState('36');
  const [startDate, setStartDate] = useState(new Date().toISOString().split('T')[0]);

  // Prepayment Form
  const [prepaymentExtra, setPrepaymentExtra] = useState('2000');
  const [simResult, setSimResult] = useState<any>(null);

  const { data: loans } = useQuery({
    queryKey: ['loans'],
    queryFn: () => loansApi.list().then((res) => res.data),
  });

  const createLoanMutation = useMutation({
    mutationFn: (data: any) => loansApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['loans'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard-summary'] });
      setIsNewLoanModalOpen(false);
      setErrorMessage(null);
      setLoanName('');
      setLenderName('');
    },
    onError: (err: any) => {
      setErrorMessage(err.response?.data?.detail || 'Failed to create loan entry.');
    },
  });

  const simMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: any }) =>
      loansApi.simulatePrepayment(id, data),
    onSuccess: (res) => {
      setSimResult(res.data);
    },
  });

  const handleCreateLoan = (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage(null);
    createLoanMutation.mutate({
      loan_name: loanName,
      loan_type: loanType,
      lender_name: lenderName,
      principal_amount: Number(principal),
      annual_interest_rate: Number(rate),
      tenure_months: Number(tenure),
      start_date: startDate,
    });
  };

  const handleSimulate = (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedLoan) return;
    simMutation.mutate({
      id: selectedLoan.id,
      data: {
        extra_amount: Number(prepaymentExtra),
        action: 'reduce_tenure',
      },
    });
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-white">Loan & EMI Portfolio</h1>
          <p className="text-xs text-slate-500 dark:text-slate-400">Precision EMI amortization schedules, remaining balances, and prepayment simulations.</p>
        </div>
        <Button variant="primary" size="sm" onClick={() => setIsNewLoanModalOpen(true)}>
          <Plus className="w-4 h-4 mr-1.5" />
          <span>Add Loan Liability</span>
        </Button>
      </div>

      {/* Loan Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {loans?.map((loan) => (
          <Card key={loan.id} className="border-slate-200 dark:border-slate-800 flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-3">
                <Badge variant="neutral">{loan.loan_type.toUpperCase()}</Badge>
                <span className="text-xs text-slate-500 dark:text-slate-400">{loan.lender_name}</span>
              </div>

              <h3 className="font-bold text-slate-900 dark:text-white text-base">{loan.loan_name}</h3>

              <div className="mt-4 grid grid-cols-2 gap-3 p-3 bg-slate-100 dark:bg-slate-950/60 rounded-xl border border-slate-200 dark:border-slate-800/80">
                <div>
                  <span className="text-xs text-slate-500">Monthly EMI</span>
                  <p className="text-lg font-extrabold text-emerald-600 dark:text-emerald-400">{formatCurrency(Number(loan.calculated_emi), currency)}</p>
                </div>
                <div>
                  <span className="text-xs text-slate-500">Interest Rate</span>
                  <p className="text-lg font-bold text-slate-800 dark:text-slate-200">{Number(loan.annual_interest_rate)}% APR</p>
                </div>
              </div>

              <div className="mt-3 space-y-1.5 text-xs text-slate-500 dark:text-slate-400">
                <div className="flex justify-between">
                  <span>Outstanding Balance:</span>
                  <span className="font-semibold text-slate-800 dark:text-slate-200">{formatCurrency(Number(loan.outstanding_balance), currency)}</span>
                </div>
                <div className="flex justify-between">
                  <span>Total Interest Over Tenure:</span>
                  <span className="font-semibold text-slate-800 dark:text-slate-200">{formatCurrency(Number(loan.total_interest), currency)}</span>
                </div>
                <div className="flex justify-between">
                  <span>Tenure Duration:</span>
                  <span className="font-semibold text-slate-800 dark:text-slate-200">{loan.tenure_months} Months</span>
                </div>
              </div>
            </div>

            <div className="mt-5 pt-4 border-t border-slate-200 dark:border-slate-800 flex gap-2">
              <Button
                variant="secondary"
                size="sm"
                className="w-full text-xs"
                onClick={() => {
                  setSelectedLoan(loan);
                  setSimResult(null);
                  setIsSimModalOpen(true);
                }}
              >
                <Sparkles className="w-3.5 h-3.5 mr-1 text-emerald-600 dark:text-emerald-400" />
                <span>Simulate Prepayment</span>
              </Button>
            </div>
          </Card>
        ))}
      </div>

      {/* New Loan Modal */}
      <Modal isOpen={isNewLoanModalOpen} onClose={() => setIsNewLoanModalOpen(false)} title="Register Loan Liability">
        <form onSubmit={handleCreateLoan} className="space-y-4">
          {errorMessage && (
            <div className="p-3 bg-rose-500/10 border border-rose-500/20 text-rose-500 dark:text-rose-400 text-xs rounded-lg">
              {errorMessage}
            </div>
          )}
          <Input
            label="Loan Nickname"
            type="text"
            required
            value={loanName}
            onChange={(e) => setLoanName(e.target.value)}
            placeholder="e.g. Home Mortgage / Auto Loan"
          />

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-700 dark:text-slate-300 mb-1.5">
                Loan Category
              </label>
              <select
                value={loanType}
                onChange={(e) => setLoanType(e.target.value)}
                className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-900 dark:text-slate-100 focus:outline-none focus:border-emerald-500"
              >
                <option value="personal">Personal Loan</option>
                <option value="home">Home Mortgage</option>
                <option value="auto">Auto Vehicle Loan</option>
                <option value="education">Education Loan</option>
                <option value="custom">Custom Liability</option>
              </select>
            </div>

            <Input
              label="Lender Institution"
              type="text"
              required
              value={lenderName}
              onChange={(e) => setLenderName(e.target.value)}
              placeholder="e.g. Chase, HDFC Bank, SBI"
            />
          </div>

          <div className="grid grid-cols-3 gap-3">
            <Input
              label={`Principal (${getCurrencySymbol(currency)})`}
              type="number"
              required
              value={principal}
              onChange={(e) => setPrincipal(e.target.value)}
            />
            <Input
              label="Rate (% APR)"
              type="number"
              step="0.01"
              required
              value={rate}
              onChange={(e) => setRate(e.target.value)}
            />
            <Input
              label="Tenure (Mos)"
              type="number"
              required
              value={tenure}
              onChange={(e) => setTenure(e.target.value)}
            />
          </div>

          <Input
            label="Start Date"
            type="date"
            required
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
          />

          <Button type="submit" variant="primary" className="w-full mt-2" isLoading={createLoanMutation.isPending}>
            Calculate & Generate Amortization Table
          </Button>
        </form>
      </Modal>

      {/* Prepayment Simulation Modal */}
      <Modal isOpen={isSimModalOpen} onClose={() => setIsSimModalOpen(false)} title={`Prepayment Simulator: ${selectedLoan?.loan_name}`}>
        <form onSubmit={handleSimulate} className="space-y-4">
          <Input
            label={`Lumpsum Extra Prepayment (${getCurrencySymbol(currency)})`}
            type="number"
            required
            value={prepaymentExtra}
            onChange={(e) => setPrepaymentExtra(e.target.value)}
            placeholder="2000"
          />

          <Button type="submit" variant="primary" className="w-full" isLoading={simMutation.isPending}>
            Calculate Interest & Tenure Reduction
          </Button>

          {simResult && (
            <div className="mt-4 p-4 bg-slate-50 dark:bg-slate-950 rounded-xl border border-emerald-500/30 space-y-3">
              <div className="flex items-center gap-2 text-emerald-600 dark:text-emerald-400 font-bold text-sm">
                <ShieldCheck className="w-4 h-4" />
                <span>Simulation Findings</span>
              </div>
              <div className="grid grid-cols-2 gap-3 text-xs">
                <div>
                  <span className="text-slate-500 dark:text-slate-400">Total Interest Saved:</span>
                  <p className="text-base font-extrabold text-emerald-600 dark:text-emerald-400">
                    {formatCurrency(Number(simResult.interest_savings), currency)}
                  </p>
                </div>
                <div>
                  <span className="text-slate-500 dark:text-slate-400">Payoff Timeline Saved:</span>
                  <p className="text-base font-bold text-slate-900 dark:text-white">{simResult.months_saved} Months Earlier</p>
                </div>
              </div>
              <p className="text-xs text-slate-500 dark:text-slate-400">
                Accelerates debt-free date to month <strong>{simResult.new_tenure_months}</strong> of {simResult.original_tenure_months}.
              </p>
            </div>
          )}
        </form>
      </Modal>
    </div>
  );
};
