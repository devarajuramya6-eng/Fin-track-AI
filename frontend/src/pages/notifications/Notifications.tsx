import React from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Bell, Check, AlertTriangle, Info, CheckCircle2 } from 'lucide-react';
import { notificationsApi } from '../../api/endpoints';
import { Card } from '../../components/common/Card';
import { Button } from '../../components/common/Button';
import { Badge } from '../../components/common/Badge';

export const Notifications: React.FC = () => {
  const queryClient = useQueryClient();

  const { data: notifications } = useQuery({
    queryKey: ['notifications'],
    queryFn: () => notificationsApi.list().then((res) => res.data),
  });

  const markReadMutation = useMutation({
    mutationFn: (id: number) => notificationsApi.markRead(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['notifications'] });
    },
  });

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-white flex items-center gap-2">
          <Bell className="w-7 h-7 text-emerald-500 dark:text-emerald-400" />
          <span>In-App Notification Center</span>
        </h1>
        <p className="text-xs text-slate-500 dark:text-slate-400">System alerts, budget overspending warnings, and milestone celebrations.</p>
      </div>

      <div className="space-y-3">
        {notifications?.map((notif) => (
          <Card
            key={notif.id}
            className={`transition border-slate-200 dark:border-slate-800 ${
              notif.is_read ? 'opacity-75' : 'border-l-4 border-l-emerald-500'
            }`}
          >
            <div className="flex items-start justify-between gap-4">
              <div className="flex items-start gap-3">
                <div className="p-2 rounded-lg bg-slate-100 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 mt-0.5">
                  {notif.severity === 'warning' ? (
                    <AlertTriangle className="w-4 h-4 text-amber-500" />
                  ) : notif.severity === 'success' ? (
                    <CheckCircle2 className="w-4 h-4 text-emerald-500" />
                  ) : (
                    <Info className="w-4 h-4 text-blue-500" />
                  )}
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <h4 className="font-semibold text-slate-900 dark:text-white text-sm">{notif.title}</h4>
                    <Badge variant={notif.severity as any}>{notif.notification_type.replace('_', ' ')}</Badge>
                  </div>
                  <p className="text-xs text-slate-600 dark:text-slate-300 mt-1 leading-relaxed">{notif.message}</p>
                  <span className="text-[10px] text-slate-400 dark:text-slate-500 mt-2 block">{new Date(notif.created_at).toLocaleString()}</span>
                </div>
              </div>

              {!notif.is_read && (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => markReadMutation.mutate(notif.id)}
                  title="Mark as read"
                >
                  <Check className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
                </Button>
              )}
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
