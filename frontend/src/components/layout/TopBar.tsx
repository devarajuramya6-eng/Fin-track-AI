import React from 'react';
import { Bell, Sparkles, ShieldCheck, Sun, Moon } from 'lucide-react';
import { useAuth } from '../../contexts/AuthContext';
import { useTheme } from '../../contexts/ThemeContext';
import { Link } from 'react-router-dom';

export const TopBar: React.FC = () => {
  const { user } = useAuth();
  const { theme, toggleTheme } = useTheme();

  return (
    <header className="h-16 bg-white/80 dark:bg-slate-900/60 backdrop-blur-md border-b border-slate-200 dark:border-slate-800 px-6 flex items-center justify-between sticky top-0 z-30 transition-colors">
      <div className="flex items-center gap-3">
        <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20">
          <ShieldCheck className="w-3.5 h-3.5" />
          <span>Local Engine Active</span>
        </span>
        <span className="text-xs text-slate-500 font-medium hidden sm:inline">
          100% On-Device AI • No Cloud API Keys Required
        </span>
      </div>

      <div className="flex items-center gap-3">
        <Link
          to="/ai-assistant"
          className="flex items-center gap-2 px-3 py-1.5 text-xs font-medium bg-emerald-500/10 dark:bg-gradient-to-r dark:from-emerald-500/20 dark:to-teal-500/20 text-emerald-700 dark:text-emerald-300 border border-emerald-500/30 rounded-lg hover:bg-emerald-500/20 transition shadow-sm"
        >
          <Sparkles className="w-3.5 h-3.5 text-emerald-500 dark:text-emerald-400" />
          <span>Ask AI Assistant</span>
        </Link>

        {/* Theme Toggle Button (Light / Dark) */}
        <button
          onClick={toggleTheme}
          className="p-2 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg transition"
          title={`Switch to ${theme === 'dark' ? 'Light' : 'Dark'} Mode`}
        >
          {theme === 'dark' ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4 text-slate-600" />}
        </button>

        <Link
          to="/notifications"
          className="relative p-2 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg transition"
          title="Notifications"
        >
          <Bell className="w-4 h-4" />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></span>
        </Link>

        <div className="h-4 w-px bg-slate-200 dark:bg-slate-800"></div>

        <span className="text-xs font-bold px-2.5 py-1 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 rounded-md border border-slate-200 dark:border-slate-700">
          {user?.preferred_currency || 'USD'}
        </span>
      </div>
    </header>
  );
};
