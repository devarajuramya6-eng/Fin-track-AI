import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Plus, RefreshCw } from 'lucide-react';
import { investmentsApi } from '../../api/endpoints';
import { Card } from '../../components/common/Card';
import { Button } from '../../components/common/Button';
import { Modal } from '../../components/common/Modal';
import { Input } from '../../components/common/Input';
import { useAuth } from '../../contexts/AuthContext';
import { formatCurrency, getCurrencySymbol } from '../../utils/formatters';

export const Investments: React.FC = () => {
  const { user } = useAuth();
  const currency = user?.preferred_currency || 'USD';
  const queryClient = useQueryClient();
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const [isValModalOpen, setIsValModalOpen] = useState(false);
  const [selectedHolding, setSelectedHolding] = useState<any>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  // New Holding Form
  const [symbol, setSymbol] = useState('VTI');
  const [name, setName] = useState('Vanguard Total Stock ETF');
  const [assetClass, setAssetClass] = useState('etf');
  const [qty, setQty] = useState('10');
  const [buyPrice, setBuyPrice] = useState('220');
  const [currPrice, setCurrPrice] = useState('250');
  const [newValPrice, setNewValPrice] = useState('');

  const { data: portfolio } = useQuery({
    queryKey: ['investments-portfolio'],
    queryFn: () => investmentsApi.getPortfolio().then((res) => res.data),
  });

  const addHoldingMutation = useMutation({
    mutationFn: (data: any) => investmentsApi.addHolding(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['investments-portfolio'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard-summary'] });
      setIsAddModalOpen(false);
      setErrorMessage(null);
    },
    onError: (err: any) => {
      setErrorMessage(err.response?.data?.detail || 'Failed to add asset holding.');
    },
  });

  const updateValuationMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: any }) =>
      investmentsApi.updateValuation(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['investments-portfolio'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard-summary'] });
      setIsValModalOpen(false);
    },
  });

  const handleAddHolding = (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage(null);
    addHoldingMutation.mutate({
      asset_symbol: symbol,
      asset_name: name,
      asset_class: assetClass,
      quantity: Number(qty),
      buy_price: Number(buyPrice),
      current_price: Number(currPrice),
      purchase_date: new Date().toISOString().split('T')[0],
    });
  };

  const handleUpdateVal = (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedHolding || !newValPrice) return;
    updateValuationMutation.mutate({
      id: selectedHolding.id,
      data: {
        current_price: Number(newValPrice),
        valuation_date: new Date().toISOString().split('T')[0],
      },
    });
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-white">Investment Portfolio</h1>
          <p className="text-xs text-slate-500 dark:text-slate-400">Manual asset valuation tracker across Equities, Mutual Funds, ETFs, Bonds, and Gold.</p>
        </div>
        <Button variant="primary" size="sm" onClick={() => setIsAddModalOpen(true)}>
          <Plus className="w-4 h-4 mr-1.5" />
          <span>Add Asset Holding</span>
        </Button>
      </div>

      {/* Portfolio Metrics */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="border-l-4 border-l-purple-500">
          <span className="text-xs text-slate-500 dark:text-slate-400">Total Portfolio Value</span>
          <p className="text-2xl font-bold text-slate-900 dark:text-white mt-1">
            {formatCurrency(Number(portfolio?.total_current_value || 0), currency)}
          </p>
        </Card>
        <Card className="border-l-4 border-l-blue-500">
          <span className="text-xs text-slate-500 dark:text-slate-400">Total Cost Basis</span>
          <p className="text-2xl font-bold text-slate-900 dark:text-white mt-1">
            {formatCurrency(Number(portfolio?.total_invested_amount || 0), currency)}
          </p>
        </Card>
        <Card className="border-l-4 border-l-emerald-500">
          <span className="text-xs text-slate-500 dark:text-slate-400">Unrealized Gain / Loss</span>
          <p className={`text-2xl font-bold mt-1 ${Number(portfolio?.total_unrealized_gain_loss || 0) >= 0 ? 'text-emerald-600 dark:text-emerald-400' : 'text-rose-600 dark:text-rose-400'}`}>
            {Number(portfolio?.total_unrealized_gain_loss || 0) >= 0 ? '+' : ''}{formatCurrency(Number(portfolio?.total_unrealized_gain_loss || 0), currency)}
          </p>
        </Card>
        <Card className="border-l-4 border-l-teal-500">
          <span className="text-xs text-slate-500 dark:text-slate-400">Overall Portfolio Return</span>
          <p className="text-2xl font-bold text-teal-600 dark:text-teal-400 mt-1">
            +{Number(portfolio?.overall_return_percentage || 0).toFixed(2)}%
          </p>
        </Card>
      </div>

      {/* Holdings Table */}
      <Card title="Holdings Ledger" subtitle="Manually maintained asset holdings without commercial market APIs">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-200 dark:border-slate-800 text-slate-500 dark:text-slate-400 uppercase tracking-wider font-semibold">
                <th className="pb-3">Symbol & Name</th>
                <th className="pb-3">Asset Class</th>
                <th className="pb-3">Quantity</th>
                <th className="pb-3">Avg Buy Price</th>
                <th className="pb-3">Current Price</th>
                <th className="pb-3 text-right">Market Value</th>
                <th className="pb-3 text-right">P&L (%)</th>
                <th className="pb-3 text-center">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200 dark:divide-slate-800/60">
              {portfolio?.holdings?.map((h) => (
                <tr key={h.id} className="hover:bg-slate-100/50 dark:hover:bg-slate-800/30 transition">
                  <td className="py-3.5">
                    <span className="font-bold text-slate-900 dark:text-slate-100">{h.asset_symbol}</span>
                    <span className="block text-slate-500 dark:text-slate-400 text-xs">{h.asset_name}</span>
                  </td>
                  <td className="py-3.5 capitalize text-slate-700 dark:text-slate-300">{h.asset_class.replace('_', ' ')}</td>
                  <td className="py-3.5 text-slate-800 dark:text-slate-200 font-mono">{Number(h.quantity).toFixed(2)}</td>
                  <td className="py-3.5 text-slate-700 dark:text-slate-300">{formatCurrency(Number(h.average_buy_price), currency)}</td>
                  <td className="py-3.5 text-slate-900 dark:text-slate-200 font-bold">{formatCurrency(Number(h.current_price), currency)}</td>
                  <td className="py-3.5 text-right font-bold text-slate-900 dark:text-white">
                    {formatCurrency(Number(h.current_market_value), currency)}
                  </td>
                  <td className="py-3.5 text-right text-emerald-600 dark:text-emerald-400 font-semibold">
                    +{Number(h.return_percentage).toFixed(1)}%
                  </td>
                  <td className="py-3.5 text-center">
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => {
                        setSelectedHolding(h);
                        setNewValPrice(String(h.current_price));
                        setIsValModalOpen(true);
                      }}
                    >
                      <RefreshCw className="w-3.5 h-3.5 mr-1 text-slate-500 dark:text-slate-400" />
                      <span>Update Price</span>
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>

      {/* Add Asset Modal */}
      <Modal isOpen={isAddModalOpen} onClose={() => setIsAddModalOpen(false)} title="Add Asset Holding">
        <form onSubmit={handleAddHolding} className="space-y-4">
          {errorMessage && (
            <div className="p-3 bg-rose-500/10 border border-rose-500/20 text-rose-500 dark:text-rose-400 text-xs rounded-lg">
              {errorMessage}
            </div>
          )}
          <div className="grid grid-cols-2 gap-3">
            <Input
              label="Asset Symbol"
              type="text"
              required
              value={symbol}
              onChange={(e) => setSymbol(e.target.value)}
              placeholder="e.g. AAPL, VTI, INFY, RELIANCE"
            />
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-700 dark:text-slate-300 mb-1.5">
                Asset Class
              </label>
              <select
                value={assetClass}
                onChange={(e) => setAssetClass(e.target.value)}
                className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-900 dark:text-slate-100 focus:outline-none focus:border-emerald-500"
              >
                <option value="stock">Individual Stock</option>
                <option value="etf">Exchange Traded Fund (ETF)</option>
                <option value="mutual_fund">Mutual Fund</option>
                <option value="bond">Fixed Income / Bond</option>
                <option value="gold">Gold & Commodities</option>
                <option value="fixed_deposit">Fixed Deposit</option>
              </select>
            </div>
          </div>

          <Input
            label="Asset Full Name"
            type="text"
            required
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="e.g. Vanguard Total Stock Market"
          />

          <div className="grid grid-cols-3 gap-3">
            <Input
              label="Units / Shares"
              type="number"
              step="0.01"
              required
              value={qty}
              onChange={(e) => setQty(e.target.value)}
            />
            <Input
              label={`Buy Price (${getCurrencySymbol(currency)})`}
              type="number"
              step="0.01"
              required
              value={buyPrice}
              onChange={(e) => setBuyPrice(e.target.value)}
            />
            <Input
              label={`Current Value (${getCurrencySymbol(currency)})`}
              type="number"
              step="0.01"
              required
              value={currPrice}
              onChange={(e) => setCurrPrice(e.target.value)}
            />
          </div>

          <Button type="submit" variant="primary" className="w-full mt-2" isLoading={addHoldingMutation.isPending}>
            Add Holding to Portfolio
          </Button>
        </form>
      </Modal>

      {/* Update Valuation Modal */}
      <Modal isOpen={isValModalOpen} onClose={() => setIsValModalOpen(false)} title={`Update Price: ${selectedHolding?.asset_symbol}`}>
        <form onSubmit={handleUpdateVal} className="space-y-4">
          <Input
            label={`New Current Market Price (${getCurrencySymbol(currency)})`}
            type="number"
            step="0.01"
            required
            value={newValPrice}
            onChange={(e) => setNewValPrice(e.target.value)}
          />
          <Button type="submit" variant="primary" className="w-full" isLoading={updateValuationMutation.isPending}>
            Save Valuation Checkpoint
          </Button>
        </form>
      </Modal>
    </div>
  );
};
