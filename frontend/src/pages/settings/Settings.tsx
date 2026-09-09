import React, { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { Card } from '../../components/common/Card';
import { Button } from '../../components/common/Button';
import { Input } from '../../components/common/Input';
import { authApi } from '../../api/endpoints';
import { Shield } from 'lucide-react';

export const Settings: React.FC = () => {
  const { user, refreshProfile } = useAuth();
  const [fullName, setFullName] = useState(user?.full_name || '');
  const [currency, setCurrency] = useState(user?.preferred_currency || 'USD');
  const [isSaved, setIsSaved] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (user) {
      setFullName(user.full_name || '');
      setCurrency(user.preferred_currency || 'USD');
    }
  }, [user]);

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      await authApi.updateProfile({
        full_name: fullName,
        preferred_currency: currency,
      });
      await refreshProfile();
      setIsSaved(true);
      setTimeout(() => setIsSaved(false), 3000);
    } catch {
      // Handled
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-white">System & Profile Settings</h1>
        <p className="text-xs text-slate-500 dark:text-slate-400">Manage user configuration, currency preferences, and local security parameters.</p>
      </div>

      <Card title="User Profile" subtitle="Your identity information">
        <form onSubmit={handleUpdate} className="space-y-4">
          <Input
            label="Full Name"
            type="text"
            required
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
          />

          <Input
            label="Email Address (Immutable)"
            type="email"
            disabled
            value={user?.email || ''}
            className="opacity-60 cursor-not-allowed"
          />

          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-700 dark:text-slate-300 mb-1.5">
              Default Currency Display
            </label>
            <select
              value={currency}
              onChange={(e) => setCurrency(e.target.value)}
              className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-800 rounded-lg px-3.5 py-2 text-sm text-slate-900 dark:text-slate-100 focus:outline-none focus:border-emerald-500"
            >
              <option value="INR">INR (₹ - Indian Rupee)</option>
              <option value="USD">USD ($ - US Dollar)</option>
              <option value="EUR">EUR (€ - Euro)</option>
              <option value="GBP">GBP (£ - British Pound)</option>
              <option value="CAD">CAD (CA$ - Canadian Dollar)</option>
            </select>
          </div>

          <div className="pt-2 flex items-center justify-between">
            <Button type="submit" variant="primary" isLoading={isLoading}>
              Save Profile Settings
            </Button>
            {isSaved && <span className="text-xs text-emerald-600 dark:text-emerald-400 font-semibold">Settings updated successfully!</span>}
          </div>
        </form>
      </Card>

      <Card title="Platform Integrity & Privacy" subtitle="Security architecture specifications">
        <div className="space-y-3 text-xs text-slate-700 dark:text-slate-300">
          <div className="p-3 bg-slate-100 dark:bg-slate-950 rounded-lg border border-slate-200 dark:border-slate-800 flex items-start gap-3">
            <Shield className="w-4 h-4 text-emerald-600 dark:text-emerald-400 mt-0.5" />
            <div>
              <p className="font-semibold text-slate-900 dark:text-white">Zero Third-Party Cloud Transmission</p>
              <p className="text-slate-500 dark:text-slate-400 mt-0.5">All transactions, financial metrics, and AI models execute strictly within your local environment.</p>
            </div>
          </div>
        </div>
      </Card>
    </div>
  );
};
