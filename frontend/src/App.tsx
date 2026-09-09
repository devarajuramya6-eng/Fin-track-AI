import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AuthProvider } from './contexts/AuthContext';
import { ThemeProvider } from './contexts/ThemeContext';
import { ProtectedRoute } from './components/layout/ProtectedRoute';
import { AppLayout } from './components/layout/AppLayout';

// Pages
import { Login } from './pages/auth/Login';
import { Register } from './pages/auth/Register';
import { ForgotPassword } from './pages/auth/ForgotPassword';
import { Dashboard } from './pages/dashboard/Dashboard';
import { Transactions } from './pages/transactions/Transactions';
import { Budgets } from './pages/budgets/Budgets';
import { Savings } from './pages/savings/Savings';
import { Loans } from './pages/loans/Loans';
import { Investments } from './pages/investments/Investments';
import { Reports } from './pages/reports/Reports';
import { AIAssistant } from './pages/ai-assistant/AIAssistant';
import { RiskAnalysis } from './pages/risk/RiskAnalysis';
import { Notifications } from './pages/notifications/Notifications';
import { Settings } from './pages/settings/Settings';
import { AdminDashboard } from './pages/admin/AdminDashboard';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 30000,
    },
  },
});

export const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider>
        <AuthProvider>
          <BrowserRouter>
            <Routes>
              {/* Public Auth Routes */}
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/forgot-password" element={<ForgotPassword />} />

              {/* Authenticated Protected Routes */}
              <Route element={<ProtectedRoute />}>
                <Route element={<AppLayout />}>
                  <Route path="/" element={<Dashboard />} />
                  <Route path="/transactions" element={<Transactions />} />
                  <Route path="/budgets" element={<Budgets />} />
                  <Route path="/savings" element={<Savings />} />
                  <Route path="/loans" element={<Loans />} />
                  <Route path="/investments" element={<Investments />} />
                  <Route path="/reports" element={<Reports />} />
                  <Route path="/ai-assistant" element={<AIAssistant />} />
                  <Route path="/risk" element={<RiskAnalysis />} />
                  <Route path="/notifications" element={<Notifications />} />
                  <Route path="/settings" element={<Settings />} />
                  <Route path="/admin" element={<AdminDashboard />} />
                </Route>
              </Route>

              {/* Catch-all fallback */}
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </BrowserRouter>
        </AuthProvider>
      </ThemeProvider>
    </QueryClientProvider>
  );
};
