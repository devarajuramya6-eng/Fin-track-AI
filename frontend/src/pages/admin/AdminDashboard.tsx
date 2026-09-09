import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { Shield } from 'lucide-react';
import { adminApi } from '../../api/endpoints';
import { Card } from '../../components/common/Card';
import { Badge } from '../../components/common/Badge';

export const AdminDashboard: React.FC = () => {
  const { data: telemetry } = useQuery({
    queryKey: ['admin-telemetry'],
    queryFn: () => adminApi.getTelemetry().then((res) => res.data),
  });

  const { data: users } = useQuery({
    queryKey: ['admin-users'],
    queryFn: () => adminApi.listUsers().then((res) => res.data),
  });

  const { data: auditLogs } = useQuery({
    queryKey: ['admin-audit-logs'],
    queryFn: () => adminApi.getAuditLogs().then((res) => res.data),
  });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-white flex items-center gap-2">
          <Shield className="w-7 h-7 text-purple-500 dark:text-purple-400" />
          <span>Platform Administrator Console</span>
        </h1>
        <p className="text-xs text-slate-500 dark:text-slate-400">System health monitoring, database entity metrics, and tamper-evident audit logs.</p>
      </div>

      {/* Telemetry Metrics */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="border-l-4 border-l-purple-500">
          <span className="text-xs text-slate-500 dark:text-slate-400">Total Users</span>
          <p className="text-2xl font-bold text-slate-900 dark:text-white mt-1">{telemetry?.total_users || 0}</p>
        </Card>
        <Card className="border-l-4 border-l-blue-500">
          <span className="text-xs text-slate-500 dark:text-slate-400">Total Accounts</span>
          <p className="text-2xl font-bold text-slate-900 dark:text-white mt-1">{telemetry?.total_accounts || 0}</p>
        </Card>
        <Card className="border-l-4 border-l-emerald-500">
          <span className="text-xs text-slate-500 dark:text-slate-400">Total Transactions</span>
          <p className="text-2xl font-bold text-slate-900 dark:text-white mt-1">{telemetry?.total_transactions || 0}</p>
        </Card>
        <Card className="border-l-4 border-l-teal-500">
          <span className="text-xs text-slate-500 dark:text-slate-400">Total Loans</span>
          <p className="text-2xl font-bold text-slate-900 dark:text-white mt-1">{telemetry?.total_loans || 0}</p>
        </Card>
      </div>

      {/* User Directory */}
      <Card title="Registered User Accounts" subtitle="Local user records and permission tiers">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-200 dark:border-slate-800 text-slate-500 dark:text-slate-400 uppercase tracking-wider font-semibold">
                <th className="pb-3">ID</th>
                <th className="pb-3">Full Name</th>
                <th className="pb-3">Email Address</th>
                <th className="pb-3">Role Status</th>
                <th className="pb-3">Preferred Currency</th>
                <th className="pb-3">Created At</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200 dark:divide-slate-800/60">
              {users?.map((u) => (
                <tr key={u.id} className="hover:bg-slate-100/50 dark:hover:bg-slate-800/30 transition">
                  <td className="py-3 text-slate-400 dark:text-slate-500 font-mono">#{u.id}</td>
                  <td className="py-3 font-medium text-slate-900 dark:text-slate-200">{u.full_name}</td>
                  <td className="py-3 text-slate-700 dark:text-slate-300">{u.email}</td>
                  <td className="py-3">
                    <Badge variant={u.is_superuser ? 'warning' : 'neutral'}>
                      {u.is_superuser ? 'Administrator' : 'Standard User'}
                    </Badge>
                  </td>
                  <td className="py-3 font-semibold text-slate-700 dark:text-slate-300">{u.preferred_currency}</td>
                  <td className="py-3 text-slate-500">{new Date(u.created_at).toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>

      {/* Audit Trail */}
      <Card title="Security & Mutation Audit Logs" subtitle="Tamper-evident activity trail">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-200 dark:border-slate-800 text-slate-500 dark:text-slate-400 uppercase tracking-wider font-semibold">
                <th className="pb-3">Timestamp</th>
                <th className="pb-3">Action</th>
                <th className="pb-3">Entity Type</th>
                <th className="pb-3">Details</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200 dark:divide-slate-800/60">
              {auditLogs?.map((log) => (
                <tr key={log.id} className="hover:bg-slate-100/50 dark:hover:bg-slate-800/30 transition">
                  <td className="py-3 text-slate-400 dark:text-slate-500 font-mono">{new Date(log.created_at).toLocaleString()}</td>
                  <td className="py-3">
                    <Badge variant="neutral">{log.action}</Badge>
                  </td>
                  <td className="py-3 text-slate-700 dark:text-slate-300 font-medium">{log.entity_type}</td>
                  <td className="py-3 text-slate-500 dark:text-slate-400">{log.details || '-'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
};
