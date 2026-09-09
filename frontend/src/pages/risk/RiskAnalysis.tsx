import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { ShieldAlert } from 'lucide-react';
import { aiApi } from '../../api/endpoints';
import { Card } from '../../components/common/Card';
import { Badge } from '../../components/common/Badge';

export const RiskAnalysis: React.FC = () => {
  const { data: riskScore } = useQuery({
    queryKey: ['risk-score'],
    queryFn: () => aiApi.getRiskScore().then((res) => res.data),
  });

  const { data: anomalies } = useQuery({
    queryKey: ['anomalies'],
    queryFn: () => aiApi.getAnomalies().then((res) => res.data),
  });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-white flex items-center gap-2">
          <ShieldAlert className="w-7 h-7 text-emerald-500 dark:text-emerald-400" />
          <span>Explainable Risk & Health Audit</span>
        </h1>
        <p className="text-xs text-slate-500 dark:text-slate-400">Deterministic multi-pillar solvency analysis evaluating leverage, runway, volatility, and outliers.</p>
      </div>

      {/* Main Score Hero Card */}
      <Card className="bg-gradient-to-r from-slate-50 via-white to-slate-100 dark:from-slate-900 dark:via-slate-900 dark:to-slate-950 border-slate-200 dark:border-slate-800 p-6">
        <div className="flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="flex items-center gap-6">
            <div className="w-24 h-24 rounded-full border-4 border-slate-300 dark:border-slate-800 flex items-center justify-center bg-white dark:bg-slate-950">
              <div className="text-center">
                <span className="text-3xl font-extrabold text-emerald-600 dark:text-emerald-400">{riskScore?.overall_health_score || 80}</span>
                <span className="text-[10px] text-slate-400 dark:text-slate-500 font-bold block">HEALTH</span>
              </div>
            </div>
            <div>
              <div className="flex items-center gap-2">
                <Badge variant={riskScore?.risk_level === 'Low' ? 'success' : 'warning'}>
                  {riskScore?.risk_level || 'Low'} Risk Status
                </Badge>
                <span className="text-xs text-slate-500 dark:text-slate-400">Risk Score: {riskScore?.risk_score || 20}/100</span>
              </div>
              <p className="text-sm font-medium text-slate-800 dark:text-slate-200 mt-2 max-w-xl leading-relaxed">
                {riskScore?.summary_explanation}
              </p>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4 text-xs w-full md:w-auto border-t md:border-t-0 md:border-l border-slate-200 dark:border-slate-800 pt-4 md:pt-0 md:pl-6">
            <div>
              <span className="text-slate-500">Debt-to-Income (DTI)</span>
              <p className="text-base font-bold text-slate-900 dark:text-white">{riskScore?.debt_to_income_ratio || 0}%</p>
            </div>
            <div>
              <span className="text-slate-500">Emergency Runway</span>
              <p className="text-base font-bold text-slate-900 dark:text-white">{riskScore?.emergency_runway_months || 0} Months</p>
            </div>
            <div>
              <span className="text-slate-500">Savings Rate</span>
              <p className="text-base font-bold text-slate-900 dark:text-white">{riskScore?.savings_ratio || 0}%</p>
            </div>
            <div>
              <span className="text-slate-500">Cash Flow Volatility</span>
              <p className="text-base font-bold text-slate-900 dark:text-white">{riskScore?.cash_flow_volatility_score || 0}</p>
            </div>
          </div>
        </div>
      </Card>

      {/* Risk Pillars & Breakdown Factors */}
      <div>
        <h3 className="text-base font-bold text-slate-900 dark:text-white mb-3">Explainable Risk Factors & Mitigation Actions</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {riskScore?.risk_factors?.map((factor) => (
            <Card key={factor.id} className="border-slate-200 dark:border-slate-800">
              <div className="flex items-start justify-between">
                <div>
                  <h4 className="font-semibold text-slate-900 dark:text-slate-100 text-sm">{factor.factor_name}</h4>
                  <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">{factor.description}</p>
                </div>
                <Badge variant={factor.severity === 'critical' ? 'danger' : factor.severity === 'medium' ? 'warning' : 'success'}>
                  {factor.severity.toUpperCase()}
                </Badge>
              </div>

              <div className="mt-4 p-3 bg-slate-50 dark:bg-slate-950 rounded-lg border border-slate-200 dark:border-slate-800 text-xs">
                <span className="font-semibold text-emerald-600 dark:text-emerald-400">Prescribed Action: </span>
                <span className="text-slate-700 dark:text-slate-300">{factor.mitigation_suggestion}</span>
              </div>
            </Card>
          ))}
        </div>
      </div>

      {/* Statistical Outliers & Anomaly Radar */}
      <div>
        <h3 className="text-base font-bold text-slate-900 dark:text-white mb-3">Statistical Outlier & Anomaly Detections</h3>
        <Card>
          {anomalies && anomalies.length > 0 ? (
            <div className="space-y-3">
              {anomalies.map((a) => (
                <div key={a.id} className="p-3.5 bg-slate-50 dark:bg-slate-950 rounded-lg border border-slate-200 dark:border-slate-800 flex items-start justify-between text-xs">
                  <div>
                    <div className="flex items-center gap-2">
                      <Badge variant="warning">{a.detection_method.toUpperCase()}</Badge>
                      <span className="font-semibold text-slate-800 dark:text-slate-200 capitalize">{a.anomaly_type.replace('_', ' ')}</span>
                    </div>
                    <p className="text-slate-500 dark:text-slate-400 mt-1">{a.description}</p>
                  </div>
                  <span className="text-slate-500 font-mono text-[10px]">Score: {a.score_value}</span>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-6 text-slate-500 text-xs">
              No anomalous transactions detected in current historical data.
            </div>
          )}
        </Card>
      </div>
    </div>
  );
};
