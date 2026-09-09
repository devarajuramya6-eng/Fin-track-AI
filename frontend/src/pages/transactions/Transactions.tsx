import React, { useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  Plus,
  Search,
  Download,
  Upload,
  Trash2,
} from 'lucide-react';
import { transactionsApi, accountsApi, categoriesApi } from '../../api/endpoints';
import { Card } from '../../components/common/Card';
import { Button } from '../../components/common/Button';
import { Input } from '../../components/common/Input';
import { Modal } from '../../components/common/Modal';
import { useAuth } from '../../contexts/AuthContext';
import { formatCurrency, getCurrencySymbol } from '../../utils/formatters';

export const Transactions: React.FC = () => {
  const { user } = useAuth();
  const currency = user?.preferred_currency || 'USD';
  const queryClient = useQueryClient();
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedType, setSelectedType] = useState<string>('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isAccountModalOpen, setIsAccountModalOpen] = useState(false);
  const [isImportModalOpen, setIsImportModalOpen] = useState(false);
  const [csvText, setCsvText] = useState('');
  const [importMessage, setImportMessage] = useState<string | null>(null);

  // Form State
  const [accountId, setAccountId] = useState<number | ''>('');
  const [categoryId, setCategoryId] = useState<number | ''>('');
  const [amount, setAmount] = useState('');
  const [txType, setTxType] = useState<'expense' | 'income'>('expense');
  const [txDate, setTxDate] = useState(new Date().toISOString().split('T')[0]);
  const [payee, setPayee] = useState('');
  const [description, setDescription] = useState('');
  const [paymentMethod, setPaymentMethod] = useState('card');

  // Quick Account Create State
  const [newAccountName, setNewAccountName] = useState('Checking Account');
  const [newAccountType, setNewAccountType] = useState('checking');
  const [newAccountBalance, setNewAccountBalance] = useState('1000.00');

  // Queries
  const { data: transactions, isLoading } = useQuery({
    queryKey: ['transactions', searchTerm, selectedType],
    queryFn: () =>
      transactionsApi
        .list({
          search: searchTerm || undefined,
          transaction_type: selectedType || undefined,
        })
        .then((res) => res.data),
  });

  const { data: accounts } = useQuery({
    queryKey: ['accounts'],
    queryFn: () => accountsApi.list().then((res) => res.data),
  });

  const { data: categories } = useQuery({
    queryKey: ['categories'],
    queryFn: () => categoriesApi.list().then((res) => res.data),
  });

  // Auto-select first account if available
  useEffect(() => {
    if (accounts && accounts.length > 0 && !accountId) {
      setAccountId(accounts[0].id);
    }
  }, [accounts, accountId]);

  // Auto-select first category matching current txType
  useEffect(() => {
    if (categories && categories.length > 0) {
      const validCategories = categories.filter((c) => c.category_type === txType || c.category_type === 'transfer');
      if (validCategories.length > 0 && (!categoryId || !validCategories.some((c) => c.id === categoryId))) {
        setCategoryId(validCategories[0].id);
      }
    }
  }, [categories, txType, categoryId]);

  // Create Transaction Mutation
  const createMutation = useMutation({
    mutationFn: (newTx: any) => transactionsApi.create(newTx),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['transactions'] });
      queryClient.invalidateQueries({ queryKey: ['accounts'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard-summary'] });
      queryClient.invalidateQueries({ queryKey: ['cash-flow'] });
      queryClient.invalidateQueries({ queryKey: ['spending-by-category'] });
      setIsModalOpen(false);
      resetForm();
    },
  });

  // Quick Account Mutation
  const createAccountMutation = useMutation({
    mutationFn: (newAcc: any) => accountsApi.create(newAcc),
    onSuccess: (res) => {
      queryClient.invalidateQueries({ queryKey: ['accounts'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard-summary'] });
      setAccountId(res.data.id);
      setIsAccountModalOpen(false);
    },
  });

  // Import CSV Mutation
  const importCsvMutation = useMutation({
    mutationFn: () => transactionsApi.importCsv(Number(accountId), csvText),
    onSuccess: (res) => {
      queryClient.invalidateQueries({ queryKey: ['transactions'] });
      queryClient.invalidateQueries({ queryKey: ['accounts'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard-summary'] });
      queryClient.invalidateQueries({ queryKey: ['cash-flow'] });
      setImportMessage(res.data.message);
      setTimeout(() => {
        setIsImportModalOpen(false);
        setImportMessage(null);
        setCsvText('');
      }, 1500);
    },
  });

  // Delete Mutation
  const deleteMutation = useMutation({
    mutationFn: (id: number) => transactionsApi.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['transactions'] });
      queryClient.invalidateQueries({ queryKey: ['accounts'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard-summary'] });
    },
  });

  const resetForm = () => {
    setAmount('');
    setPayee('');
    setDescription('');
  };

  const handleCreate = (e: React.FormEvent) => {
    e.preventDefault();
    if (!accountId || !categoryId || !amount || !payee) return;

    createMutation.mutate({
      account_id: Number(accountId),
      category_id: Number(categoryId),
      amount: Number(amount),
      transaction_type: txType,
      transaction_date: txDate,
      payee_or_merchant: payee,
      description: description || undefined,
      payment_method: paymentMethod,
    });
  };

  const handleCreateAccount = (e: React.FormEvent) => {
    e.preventDefault();
    createAccountMutation.mutate({
      name: newAccountName,
      account_type: newAccountType,
      current_balance: Number(newAccountBalance) || 0,
      currency: currency,
    });
  };

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        setCsvText(event.target?.result as string || '');
      };
      reader.readAsText(file);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-white">Transaction Ledger</h1>
          <p className="text-xs text-slate-500 dark:text-slate-400">Manage income, expense postings, and account reconciliations.</p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="secondary" size="sm" onClick={() => setIsAccountModalOpen(true)}>
            <Plus className="w-4 h-4 mr-1.5" />
            <span>+ Add Account</span>
          </Button>
          <Button variant="secondary" size="sm" onClick={() => setIsImportModalOpen(true)}>
            <Upload className="w-4 h-4 mr-1.5" />
            <span>Import CSV</span>
          </Button>
          <a href="/api/v1/transactions/export-csv" target="_blank" rel="noreferrer">
            <Button variant="secondary" size="sm">
              <Download className="w-4 h-4 mr-1.5" />
              <span>Export CSV</span>
            </Button>
          </a>
          <Button variant="primary" size="sm" onClick={() => setIsModalOpen(true)}>
            <Plus className="w-4 h-4 mr-1.5" />
            <span>New Transaction</span>
          </Button>
        </div>
      </div>

      {/* Filter Bar */}
      <Card className="p-4">
        <div className="flex flex-col sm:flex-row items-center gap-3">
          <div className="relative flex-1 w-full">
            <Search className="w-4 h-4 absolute left-3 top-2.5 text-slate-400 dark:text-slate-500" />
            <input
              type="text"
              placeholder="Search merchant, description, or notes..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-800 rounded-lg pl-9 pr-3.5 py-1.5 text-sm text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:border-emerald-500"
            />
          </div>

          <div className="flex items-center gap-2 w-full sm:w-auto">
            <select
              value={selectedType}
              onChange={(e) => setSelectedType(e.target.value)}
              className="bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-800 rounded-lg px-3 py-1.5 text-sm text-slate-900 dark:text-slate-100 focus:outline-none focus:border-emerald-500"
            >
              <option value="">All Types</option>
              <option value="expense">Expenses Only</option>
              <option value="income">Income Only</option>
            </select>
          </div>
        </div>
      </Card>

      {/* Transaction Table */}
      <Card>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-200 dark:border-slate-800 text-slate-500 dark:text-slate-400 uppercase tracking-wider font-semibold">
                <th className="pb-3">Date</th>
                <th className="pb-3">Merchant / Payee</th>
                <th className="pb-3">Category</th>
                <th className="pb-3">Payment Method</th>
                <th className="pb-3 text-right">Amount</th>
                <th className="pb-3 text-center">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200 dark:divide-slate-800/60">
              {isLoading ? (
                <tr>
                  <td colSpan={6} className="py-8 text-center text-slate-500">
                    Loading transactions...
                  </td>
                </tr>
              ) : transactions && transactions.length > 0 ? (
                transactions.map((tx) => (
                  <tr key={tx.id} className="hover:bg-slate-100/50 dark:hover:bg-slate-800/30 transition">
                    <td className="py-3.5 text-slate-500 dark:text-slate-400 font-mono">{tx.transaction_date}</td>
                    <td className="py-3.5 font-medium text-slate-800 dark:text-slate-200">{tx.payee_or_merchant}</td>
                    <td className="py-3.5">
                      <span className="px-2.5 py-1 rounded-full bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300 font-medium">
                        {tx.category?.name || 'General'}
                      </span>
                    </td>
                    <td className="py-3.5 capitalize text-slate-500 dark:text-slate-400">{tx.payment_method.replace('_', ' ')}</td>
                    <td className={`py-3.5 text-right font-bold text-sm ${tx.transaction_type === 'income' ? 'text-emerald-600 dark:text-emerald-400' : 'text-slate-900 dark:text-slate-100'}`}>
                      {tx.transaction_type === 'income' ? '+' : '-'}{formatCurrency(Number(tx.amount), currency)}
                    </td>
                    <td className="py-3.5 text-center">
                      <button
                        onClick={() => deleteMutation.mutate(tx.id)}
                        className="p-1 text-slate-400 hover:text-rose-500 transition rounded"
                        title="Delete transaction"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={6} className="py-8 text-center text-slate-500">
                    No transactions recorded matching your filter.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </Card>

      {/* New Transaction Modal */}
      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Record New Transaction">
        <form onSubmit={handleCreate} className="space-y-4">
          <div className="grid grid-cols-2 gap-3">
            <button
              type="button"
              onClick={() => setTxType('expense')}
              className={`py-2 rounded-lg text-xs font-semibold border transition ${
                txType === 'expense'
                  ? 'bg-rose-500/10 border-rose-500 text-rose-500 dark:text-rose-400'
                  : 'bg-slate-100 dark:bg-slate-950 border-slate-300 dark:border-slate-800 text-slate-600 dark:text-slate-400'
              }`}
            >
              Expense Outflow
            </button>
            <button
              type="button"
              onClick={() => setTxType('income')}
              className={`py-2 rounded-lg text-xs font-semibold border transition ${
                txType === 'income'
                  ? 'bg-emerald-500/10 border-emerald-500 text-emerald-600 dark:text-emerald-400'
                  : 'bg-slate-100 dark:bg-slate-950 border-slate-300 dark:border-slate-800 text-slate-600 dark:text-slate-400'
              }`}
            >
              Income Inflow
            </button>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <div className="flex items-center justify-between mb-1.5">
                <label className="block text-xs font-semibold uppercase tracking-wider text-slate-700 dark:text-slate-300">
                  Account
                </label>
                <button
                  type="button"
                  onClick={() => setIsAccountModalOpen(true)}
                  className="text-[11px] text-emerald-600 dark:text-emerald-400 hover:underline"
                >
                  + New
                </button>
              </div>
              <select
                required
                value={accountId}
                onChange={(e) => setAccountId(Number(e.target.value))}
                className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-900 dark:text-slate-100 focus:outline-none focus:border-emerald-500"
              >
                <option value="">Select Account</option>
                {accounts?.map((acc) => (
                  <option key={acc.id} value={acc.id}>
                    {acc.name} ({formatCurrency(Number(acc.current_balance), currency)})
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-700 dark:text-slate-300 mb-1.5">
                Category
              </label>
              <select
                required
                value={categoryId}
                onChange={(e) => setCategoryId(Number(e.target.value))}
                className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-900 dark:text-slate-100 focus:outline-none focus:border-emerald-500"
              >
                <option value="">Select Category</option>
                {categories
                  ?.filter((c) => c.category_type === txType || c.category_type === 'transfer')
                  .map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.name}
                    </option>
                  ))}
              </select>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <Input
              label={`Amount (${getCurrencySymbol(currency)})`}
              type="number"
              step="0.01"
              required
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              placeholder="0.00"
            />
            <Input
              label="Transaction Date"
              type="date"
              required
              value={txDate}
              onChange={(e) => setTxDate(e.target.value)}
            />
          </div>

          <Input
            label="Payee / Merchant"
            type="text"
            required
            value={payee}
            onChange={(e) => setPayee(e.target.value)}
            placeholder="e.g. Amazon, Whole Foods, Employer"
          />

          <Input
            label="Notes (Optional)"
            type="text"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Additional details or reference notes"
          />

          <Button type="submit" variant="primary" className="w-full mt-2" isLoading={createMutation.isPending}>
            Record Transaction
          </Button>
        </form>
      </Modal>

      {/* Quick Account Modal */}
      <Modal isOpen={isAccountModalOpen} onClose={() => setIsAccountModalOpen(false)} title="Create New Financial Account">
        <form onSubmit={handleCreateAccount} className="space-y-4">
          <Input
            label="Account Name"
            type="text"
            required
            value={newAccountName}
            onChange={(e) => setNewAccountName(e.target.value)}
            placeholder="e.g. HDFC Salary Account, SBI Savings"
          />
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-700 dark:text-slate-300 mb-1.5">
              Account Type
            </label>
            <select
              value={newAccountType}
              onChange={(e) => setNewAccountType(e.target.value)}
              className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-900 dark:text-slate-100 focus:outline-none focus:border-emerald-500"
            >
              <option value="checking">Checking / Current Account</option>
              <option value="savings">Savings Account</option>
              <option value="credit_card">Credit Card</option>
              <option value="investment">Brokerage / Investment</option>
              <option value="loan">Loan Liability Account</option>
            </select>
          </div>
          <Input
            label={`Initial Balance (${getCurrencySymbol(currency)})`}
            type="number"
            step="0.01"
            required
            value={newAccountBalance}
            onChange={(e) => setNewAccountBalance(e.target.value)}
            placeholder="0.00"
          />
          <Button type="submit" variant="primary" className="w-full mt-2" isLoading={createAccountMutation.isPending}>
            Create Account
          </Button>
        </form>
      </Modal>

      {/* CSV Import Modal */}
      <Modal isOpen={isImportModalOpen} onClose={() => setIsImportModalOpen(false)} title="Import Bank Statement (CSV)">
        <div className="space-y-4">
          {importMessage && (
            <div className="p-3 bg-emerald-500/10 border border-emerald-500/20 text-emerald-600 dark:text-emerald-400 text-xs rounded-lg font-medium">
              {importMessage}
            </div>
          )}
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-700 dark:text-slate-300 mb-1.5">
              Target Account
            </label>
            <select
              required
              value={accountId}
              onChange={(e) => setAccountId(Number(e.target.value))}
              className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-900 dark:text-slate-100 focus:outline-none focus:border-emerald-500"
            >
              <option value="">Select Account</option>
              {accounts?.map((acc) => (
                <option key={acc.id} value={acc.id}>
                  {acc.name} ({formatCurrency(Number(acc.current_balance), currency)})
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-700 dark:text-slate-300 mb-1.5">
              Choose CSV File
            </label>
            <input
              type="file"
              accept=".csv,text/csv"
              onChange={handleFileUpload}
              className="w-full text-xs text-slate-600 dark:text-slate-400 file:mr-3 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-slate-200 dark:file:bg-slate-800 file:text-slate-800 dark:file:text-slate-200 hover:file:bg-slate-300 dark:hover:file:bg-slate-700 cursor-pointer"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-700 dark:text-slate-300 mb-1.5">
              Or Paste CSV Data (Format: Date, Type, Amount, Payee)
            </label>
            <textarea
              rows={5}
              value={csvText}
              onChange={(e) => setCsvText(e.target.value)}
              placeholder={`2026-09-01,expense,45.50,Grocery Store\n2026-09-02,income,3500.00,Salary Deposit`}
              className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-800 rounded-lg p-3 text-xs font-mono text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:border-emerald-500"
            />
          </div>

          <Button
            type="button"
            variant="primary"
            className="w-full"
            isLoading={importCsvMutation.isPending}
            disabled={!accountId || !csvText.trim()}
            onClick={() => importCsvMutation.mutate()}
          >
            Import Transactions
          </Button>
        </div>
      </Modal>
    </div>
  );
};
