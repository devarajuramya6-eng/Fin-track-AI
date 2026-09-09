import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  ReceiptText,
  PieChart,
  Target,
  Landmark,
  TrendingUp,
  FileBarChart2,
  Bot,
  ShieldAlert,
  Bell,
  Settings,
  Shield,
  LogOut,
} from 'lucide-react';
import { useAuth } from '../../contexts/AuthContext';

const NAV_ITEMS = [
  { name: 'Dashboard', path: '/', icon: LayoutDashboard },
  { name: 'Transactions', path: '/transactions', icon: ReceiptText },
  { name: 'Budgets', path: '/budgets', icon: PieChart },
  { name: 'Savings Goals', path: '/savings', icon: Target },
  { name: 'Loans & EMI', path: '/loans', icon: Landmark },
  { name: 'Investments', path: '/investments', icon: TrendingUp },
  { name: 'Reports', path: '/reports', icon: FileBarChart2 },
  { name: 'AI Assistant', path: '/ai-assistant', icon: Bot },
  { name: 'Risk Analysis', path: '/risk', icon: ShieldAlert },
  { name: 'Notifications', path: '/notifications', icon: Bell },
  { name: 'Settings', path: '/settings', icon: Settings },
];

export const Sidebar: React.FC = () => {
  const { user, logout } = useAuth();

  return (
    <aside className="w-64 bg-white dark:bg-slate-900 border-r border-slate-200 dark:border-slate-800 flex flex-col h-screen sticky top-0 transition-colors">
      {/* Brand Header */}
      <div className="p-5 border-b border-slate-200 dark:border-slate-800 flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-500 to-teal-400 flex items-center justify-center font-bold text-slate-950 text-xl shadow-lg shadow-emerald-500/20">
          AF
        </div>
        <div>
          <h1 className="font-bold text-slate-900 dark:text-white text-base leading-tight tracking-tight">AI FinTech</h1>
          <p className="text-xs text-slate-500 dark:text-slate-400 font-medium">Personal Finance & Risk</p>
        </div>
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
        {NAV_ITEMS.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3.5 py-2.5 rounded-lg text-sm font-medium transition-all ${
                  isActive
                    ? 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/30 dark:border-emerald-500/20 shadow-sm font-semibold'
                    : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800/60'
                }`
              }
            >
              <Icon className="w-5 h-5 flex-shrink-0" />
              <span>{item.name}</span>
            </NavLink>
          );
        })}

        {user?.is_superuser && (
          <div className="pt-3 border-t border-slate-200 dark:border-slate-800/80 mt-3">
            <p className="px-3.5 text-xs font-semibold uppercase tracking-wider text-slate-400 dark:text-slate-500 mb-1">Administration</p>
            <NavLink
              to="/admin"
              className={({ isActive }) =>
                `flex items-center gap-3 px-3.5 py-2.5 rounded-lg text-sm font-medium transition-all ${
                  isActive
                    ? 'bg-purple-500/10 text-purple-600 dark:text-purple-400 border border-purple-500/30 dark:border-purple-500/20 font-semibold'
                    : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800/60'
                }`
              }
            >
              <Shield className="w-5 h-5 flex-shrink-0" />
              <span>Admin Console</span>
            </NavLink>
          </div>
        )}
      </nav>

      {/* User Session Footer */}
      <div className="p-4 border-t border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/80 flex items-center justify-between">
        <div className="flex items-center gap-3 overflow-hidden">
          <div className="w-8 h-8 rounded-full bg-emerald-100 dark:bg-slate-700 text-emerald-700 dark:text-white flex items-center justify-center font-bold text-xs uppercase">
            {user?.full_name?.charAt(0) || 'U'}
          </div>
          <div className="overflow-hidden">
            <p className="text-sm font-semibold text-slate-800 dark:text-slate-200 truncate">{user?.full_name || 'Solo User'}</p>
            <p className="text-xs text-slate-500 dark:text-slate-400 truncate">{user?.email || 'user@local'}</p>
          </div>
        </div>
        <button
          onClick={logout}
          title="Sign out"
          className="p-1.5 text-slate-400 hover:text-rose-500 hover:bg-slate-200 dark:hover:bg-slate-800 rounded-lg transition"
        >
          <LogOut className="w-4 h-4" />
        </button>
      </div>
    </aside>
  );
};
