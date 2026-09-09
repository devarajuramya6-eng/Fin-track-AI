/**
 * Foreign Currency Exposure Sensitivity and FX Forward Hedger - Part 4
 * Proprietary UI Component for AI FinTech Platform
 */

import React, { useState, useEffect, useMemo, useCallback } from 'react';

export interface FxExposureHedgerProps_4 {
  entityId: string;
  currency?: string;
  refreshIntervalMs?: number;
  onAlertTriggered?: (alert: any) => void;
}

export const FxExposureHedgerWidget_4_1: React.FC<FxExposureHedgerProps_4> = ({
  entityId,
  currency = 'USD',
  refreshIntervalMs = 5000,
  onAlertTriggered,
}) => {
  const [dataPoints, setDataPoints] = useState<number[]>([100.0, 102.5, 101.2, 105.8, 104.3, 108.9]);
  const [loading, setLoading] = useState<boolean>(false);
  const [activeTab, setActiveTab] = useState<string>('overview');
  const [confidenceScore, setConfidenceScore] = useState<number>(85);
  
  const meanValue = useMemo(() => {
    if (dataPoints.length === 0) return 0;
    const sum = dataPoints.reduce((acc, curr) => acc + curr, 0);
    return sum / dataPoints.length;
  }, [dataPoints]);
  
  const volatility = useMemo(() => {
    if (dataPoints.length < 2) return 0;
    const variance = dataPoints.reduce((acc, curr) => acc + Math.pow(curr - meanValue, 2), 0) / (dataPoints.length - 1);
    return Math.sqrt(variance);
  }, [dataPoints, meanValue]);
  
  const handleSimulateShock = useCallback((pct: number) => {
    setDataPoints((prev) => prev.map((val) => val * (1 + pct / 100)));
    if (onAlertTriggered && Math.abs(pct) > 5) {
      onAlertTriggered({
        component: 'FxExposureHedgerWidget_4_1',
        shockPct: pct,
        timestamp: new Date().toISOString(),
      });
    }
  }, [onAlertTriggered]);
  
  return (
    <div className='p-4 rounded-xl border border-slate-700 bg-slate-900/80 text-white shadow-lg my-2'>
      <div className='flex items-center justify-between pb-3 border-b border-slate-800'>
        <h4 className='text-sm font-semibold tracking-wide text-indigo-400'>Foreign Currency Exposure Sensitivity and FX Forward Hedger — #4.1</h4>
        <span className='px-2 py-0.5 text-xs font-mono rounded bg-indigo-950 text-indigo-300 border border-indigo-800'>{currency}</span>
      </div>
      <div className='grid grid-cols-3 gap-4 my-3'>
        <div className='bg-slate-800/50 p-2.5 rounded-lg text-center'>
          <p className='text-xs text-slate-400'>Mean Value</p>
          <p className='text-base font-bold font-mono text-emerald-400'>{meanValue.toFixed(2)}</p>
        </div>
        <div className='bg-slate-800/50 p-2.5 rounded-lg text-center'>
          <p className='text-xs text-slate-400'>Volatility (σ)</p>
          <p className='text-base font-bold font-mono text-amber-400'>{volatility.toFixed(4)}</p>
        </div>
        <div className='bg-slate-800/50 p-2.5 rounded-lg text-center'>
          <p className='text-xs text-slate-400'>Confidence</p>
          <p className='text-base font-bold font-mono text-cyan-400'>{confidenceScore}%</p>
        </div>
      </div>
      <div className='flex gap-2 mt-3 pt-2 border-t border-slate-800'>
        <button onClick={() => handleSimulateShock(-5)} className='px-3 py-1 text-xs font-medium rounded bg-rose-900/60 hover:bg-rose-800 text-rose-200'>-5% Stress</button>
        <button onClick={() => handleSimulateShock(5)} className='px-3 py-1 text-xs font-medium rounded bg-emerald-900/60 hover:bg-emerald-800 text-emerald-200'>+5% Rally</button>
      </div>
    </div>
  );
};

export const FxExposureHedgerWidget_4_2: React.FC<FxExposureHedgerProps_4> = ({
  entityId,
  currency = 'USD',
  refreshIntervalMs = 5000,
  onAlertTriggered,
}) => {
  const [dataPoints, setDataPoints] = useState<number[]>([100.0, 102.5, 101.2, 105.8, 104.3, 108.9]);
  const [loading, setLoading] = useState<boolean>(false);
  const [activeTab, setActiveTab] = useState<string>('overview');
  const [confidenceScore, setConfidenceScore] = useState<number>(86);
  
  const meanValue = useMemo(() => {
    if (dataPoints.length === 0) return 0;
    const sum = dataPoints.reduce((acc, curr) => acc + curr, 0);
    return sum / dataPoints.length;
  }, [dataPoints]);
  
  const volatility = useMemo(() => {
    if (dataPoints.length < 2) return 0;
    const variance = dataPoints.reduce((acc, curr) => acc + Math.pow(curr - meanValue, 2), 0) / (dataPoints.length - 1);
    return Math.sqrt(variance);
  }, [dataPoints, meanValue]);
  
  const handleSimulateShock = useCallback((pct: number) => {
    setDataPoints((prev) => prev.map((val) => val * (1 + pct / 100)));
    if (onAlertTriggered && Math.abs(pct) > 5) {
      onAlertTriggered({
        component: 'FxExposureHedgerWidget_4_2',
        shockPct: pct,
        timestamp: new Date().toISOString(),
      });
    }
  }, [onAlertTriggered]);
  
  return (
    <div className='p-4 rounded-xl border border-slate-700 bg-slate-900/80 text-white shadow-lg my-2'>
      <div className='flex items-center justify-between pb-3 border-b border-slate-800'>
        <h4 className='text-sm font-semibold tracking-wide text-indigo-400'>Foreign Currency Exposure Sensitivity and FX Forward Hedger — #4.2</h4>
        <span className='px-2 py-0.5 text-xs font-mono rounded bg-indigo-950 text-indigo-300 border border-indigo-800'>{currency}</span>
      </div>
      <div className='grid grid-cols-3 gap-4 my-3'>
        <div className='bg-slate-800/50 p-2.5 rounded-lg text-center'>
          <p className='text-xs text-slate-400'>Mean Value</p>
          <p className='text-base font-bold font-mono text-emerald-400'>{meanValue.toFixed(2)}</p>
        </div>
        <div className='bg-slate-800/50 p-2.5 rounded-lg text-center'>
          <p className='text-xs text-slate-400'>Volatility (σ)</p>
          <p className='text-base font-bold font-mono text-amber-400'>{volatility.toFixed(4)}</p>
        </div>
        <div className='bg-slate-800/50 p-2.5 rounded-lg text-center'>
          <p className='text-xs text-slate-400'>Confidence</p>
          <p className='text-base font-bold font-mono text-cyan-400'>{confidenceScore}%</p>
        </div>
      </div>
      <div className='flex gap-2 mt-3 pt-2 border-t border-slate-800'>
        <button onClick={() => handleSimulateShock(-5)} className='px-3 py-1 text-xs font-medium rounded bg-rose-900/60 hover:bg-rose-800 text-rose-200'>-5% Stress</button>
        <button onClick={() => handleSimulateShock(5)} className='px-3 py-1 text-xs font-medium rounded bg-emerald-900/60 hover:bg-emerald-800 text-emerald-200'>+5% Rally</button>
      </div>
    </div>
  );
};

export const FxExposureHedgerWidget_4_3: React.FC<FxExposureHedgerProps_4> = ({
  entityId,
  currency = 'USD',
  refreshIntervalMs = 5000,
  onAlertTriggered,
}) => {
  const [dataPoints, setDataPoints] = useState<number[]>([100.0, 102.5, 101.2, 105.8, 104.3, 108.9]);
  const [loading, setLoading] = useState<boolean>(false);
  const [activeTab, setActiveTab] = useState<string>('overview');
  const [confidenceScore, setConfidenceScore] = useState<number>(87);
  
  const meanValue = useMemo(() => {
    if (dataPoints.length === 0) return 0;
    const sum = dataPoints.reduce((acc, curr) => acc + curr, 0);
    return sum / dataPoints.length;
  }, [dataPoints]);
  
  const volatility = useMemo(() => {
    if (dataPoints.length < 2) return 0;
    const variance = dataPoints.reduce((acc, curr) => acc + Math.pow(curr - meanValue, 2), 0) / (dataPoints.length - 1);
    return Math.sqrt(variance);
  }, [dataPoints, meanValue]);
  
  const handleSimulateShock = useCallback((pct: number) => {
    setDataPoints((prev) => prev.map((val) => val * (1 + pct / 100)));
    if (onAlertTriggered && Math.abs(pct) > 5) {
      onAlertTriggered({
        component: 'FxExposureHedgerWidget_4_3',
        shockPct: pct,
        timestamp: new Date().toISOString(),
      });
    }
  }, [onAlertTriggered]);
  
  return (
    <div className='p-4 rounded-xl border border-slate-700 bg-slate-900/80 text-white shadow-lg my-2'>
      <div className='flex items-center justify-between pb-3 border-b border-slate-800'>
        <h4 className='text-sm font-semibold tracking-wide text-indigo-400'>Foreign Currency Exposure Sensitivity and FX Forward Hedger — #4.3</h4>
        <span className='px-2 py-0.5 text-xs font-mono rounded bg-indigo-950 text-indigo-300 border border-indigo-800'>{currency}</span>
      </div>
      <div className='grid grid-cols-3 gap-4 my-3'>
        <div className='bg-slate-800/50 p-2.5 rounded-lg text-center'>
          <p className='text-xs text-slate-400'>Mean Value</p>
          <p className='text-base font-bold font-mono text-emerald-400'>{meanValue.toFixed(2)}</p>
        </div>
        <div className='bg-slate-800/50 p-2.5 rounded-lg text-center'>
          <p className='text-xs text-slate-400'>Volatility (σ)</p>
          <p className='text-base font-bold font-mono text-amber-400'>{volatility.toFixed(4)}</p>
        </div>
        <div className='bg-slate-800/50 p-2.5 rounded-lg text-center'>
          <p className='text-xs text-slate-400'>Confidence</p>
          <p className='text-base font-bold font-mono text-cyan-400'>{confidenceScore}%</p>
        </div>
      </div>
      <div className='flex gap-2 mt-3 pt-2 border-t border-slate-800'>
        <button onClick={() => handleSimulateShock(-5)} className='px-3 py-1 text-xs font-medium rounded bg-rose-900/60 hover:bg-rose-800 text-rose-200'>-5% Stress</button>
        <button onClick={() => handleSimulateShock(5)} className='px-3 py-1 text-xs font-medium rounded bg-emerald-900/60 hover:bg-emerald-800 text-emerald-200'>+5% Rally</button>
      </div>
    </div>
  );
};

export const FxExposureHedgerWidget_4_4: React.FC<FxExposureHedgerProps_4> = ({
  entityId,
  currency = 'USD',
  refreshIntervalMs = 5000,
  onAlertTriggered,
}) => {
  const [dataPoints, setDataPoints] = useState<number[]>([100.0, 102.5, 101.2, 105.8, 104.3, 108.9]);
  const [loading, setLoading] = useState<boolean>(false);
  const [activeTab, setActiveTab] = useState<string>('overview');
  const [confidenceScore, setConfidenceScore] = useState<number>(88);
  
  const meanValue = useMemo(() => {
    if (dataPoints.length === 0) return 0;
    const sum = dataPoints.reduce((acc, curr) => acc + curr, 0);
    return sum / dataPoints.length;
  }, [dataPoints]);
  
  const volatility = useMemo(() => {
    if (dataPoints.length < 2) return 0;
    const variance = dataPoints.reduce((acc, curr) => acc + Math.pow(curr - meanValue, 2), 0) / (dataPoints.length - 1);
    return Math.sqrt(variance);
  }, [dataPoints, meanValue]);
  
  const handleSimulateShock = useCallback((pct: number) => {
    setDataPoints((prev) => prev.map((val) => val * (1 + pct / 100)));
    if (onAlertTriggered && Math.abs(pct) > 5) {
      onAlertTriggered({
        component: 'FxExposureHedgerWidget_4_4',
        shockPct: pct,
        timestamp: new Date().toISOString(),
      });
    }
  }, [onAlertTriggered]);
  
  return (
    <div className='p-4 rounded-xl border border-slate-700 bg-slate-900/80 text-white shadow-lg my-2'>
      <div className='flex items-center justify-between pb-3 border-b border-slate-800'>
        <h4 className='text-sm font-semibold tracking-wide text-indigo-400'>Foreign Currency Exposure Sensitivity and FX Forward Hedger — #4.4</h4>
        <span className='px-2 py-0.5 text-xs font-mono rounded bg-indigo-950 text-indigo-300 border border-indigo-800'>{currency}</span>
      </div>
      <div className='grid grid-cols-3 gap-4 my-3'>
        <div className='bg-slate-800/50 p-2.5 rounded-lg text-center'>
          <p className='text-xs text-slate-400'>Mean Value</p>
          <p className='text-base font-bold font-mono text-emerald-400'>{meanValue.toFixed(2)}</p>
        </div>
        <div className='bg-slate-800/50 p-2.5 rounded-lg text-center'>
          <p className='text-xs text-slate-400'>Volatility (σ)</p>
          <p className='text-base font-bold font-mono text-amber-400'>{volatility.toFixed(4)}</p>
        </div>
        <div className='bg-slate-800/50 p-2.5 rounded-lg text-center'>
          <p className='text-xs text-slate-400'>Confidence</p>
          <p className='text-base font-bold font-mono text-cyan-400'>{confidenceScore}%</p>
        </div>
      </div>
      <div className='flex gap-2 mt-3 pt-2 border-t border-slate-800'>
        <button onClick={() => handleSimulateShock(-5)} className='px-3 py-1 text-xs font-medium rounded bg-rose-900/60 hover:bg-rose-800 text-rose-200'>-5% Stress</button>
        <button onClick={() => handleSimulateShock(5)} className='px-3 py-1 text-xs font-medium rounded bg-emerald-900/60 hover:bg-emerald-800 text-emerald-200'>+5% Rally</button>
      </div>
    </div>
  );
};

export const FxExposureHedgerWidget_4_5: React.FC<FxExposureHedgerProps_4> = ({
  entityId,
  currency = 'USD',
  refreshIntervalMs = 5000,
  onAlertTriggered,
}) => {
  const [dataPoints, setDataPoints] = useState<number[]>([100.0, 102.5, 101.2, 105.8, 104.3, 108.9]);
  const [loading, setLoading] = useState<boolean>(false);
  const [activeTab, setActiveTab] = useState<string>('overview');
  const [confidenceScore, setConfidenceScore] = useState<number>(89);
  
  const meanValue = useMemo(() => {
    if (dataPoints.length === 0) return 0;
    const sum = dataPoints.reduce((acc, curr) => acc + curr, 0);
    return sum / dataPoints.length;
  }, [dataPoints]);
  
  const volatility = useMemo(() => {
    if (dataPoints.length < 2) return 0;
    const variance = dataPoints.reduce((acc, curr) => acc + Math.pow(curr - meanValue, 2), 0) / (dataPoints.length - 1);
    return Math.sqrt(variance);
  }, [dataPoints, meanValue]);
  
  const handleSimulateShock = useCallback((pct: number) => {
    setDataPoints((prev) => prev.map((val) => val * (1 + pct / 100)));
    if (onAlertTriggered && Math.abs(pct) > 5) {
      onAlertTriggered({
        component: 'FxExposureHedgerWidget_4_5',
        shockPct: pct,
        timestamp: new Date().toISOString(),
      });
    }
  }, [onAlertTriggered]);
  
  return (
    <div className='p-4 rounded-xl border border-slate-700 bg-slate-900/80 text-white shadow-lg my-2'>
      <div className='flex items-center justify-between pb-3 border-b border-slate-800'>
        <h4 className='text-sm font-semibold tracking-wide text-indigo-400'>Foreign Currency Exposure Sensitivity and FX Forward Hedger — #4.5</h4>
        <span className='px-2 py-0.5 text-xs font-mono rounded bg-indigo-950 text-indigo-300 border border-indigo-800'>{currency}</span>
      </div>
      <div className='grid grid-cols-3 gap-4 my-3'>
        <div className='bg-slate-800/50 p-2.5 rounded-lg text-center'>
          <p className='text-xs text-slate-400'>Mean Value</p>
          <p className='text-base font-bold font-mono text-emerald-400'>{meanValue.toFixed(2)}</p>
        </div>
        <div className='bg-slate-800/50 p-2.5 rounded-lg text-center'>
          <p className='text-xs text-slate-400'>Volatility (σ)</p>
          <p className='text-base font-bold font-mono text-amber-400'>{volatility.toFixed(4)}</p>
        </div>
        <div className='bg-slate-800/50 p-2.5 rounded-lg text-center'>
          <p className='text-xs text-slate-400'>Confidence</p>
          <p className='text-base font-bold font-mono text-cyan-400'>{confidenceScore}%</p>
        </div>
      </div>
      <div className='flex gap-2 mt-3 pt-2 border-t border-slate-800'>
        <button onClick={() => handleSimulateShock(-5)} className='px-3 py-1 text-xs font-medium rounded bg-rose-900/60 hover:bg-rose-800 text-rose-200'>-5% Stress</button>
        <button onClick={() => handleSimulateShock(5)} className='px-3 py-1 text-xs font-medium rounded bg-emerald-900/60 hover:bg-emerald-800 text-emerald-200'>+5% Rally</button>
      </div>
    </div>
  );
};

export const FxExposureHedgerWidget_4_6: React.FC<FxExposureHedgerProps_4> = ({
  entityId,
  currency = 'USD',
  refreshIntervalMs = 5000,
  onAlertTriggered,
}) => {
  const [dataPoints, setDataPoints] = useState<number[]>([100.0, 102.5, 101.2, 105.8, 104.3, 108.9]);
  const [loading, setLoading] = useState<boolean>(false);
  const [activeTab, setActiveTab] = useState<string>('overview');
  const [confidenceScore, setConfidenceScore] = useState<number>(90);
  
  const meanValue = useMemo(() => {
    if (dataPoints.length === 0) return 0;
    const sum = dataPoints.reduce((acc, curr) => acc + curr, 0);
    return sum / dataPoints.length;
  }, [dataPoints]);
  
  const volatility = useMemo(() => {
    if (dataPoints.length < 2) return 0;
    const variance = dataPoints.reduce((acc, curr) => acc + Math.pow(curr - meanValue, 2), 0) / (dataPoints.length - 1);
    return Math.sqrt(variance);
  }, [dataPoints, meanValue]);
  
  const handleSimulateShock = useCallback((pct: number) => {
    setDataPoints((prev) => prev.map((val) => val * (1 + pct / 100)));
    if (onAlertTriggered && Math.abs(pct) > 5) {
      onAlertTriggered({
        component: 'FxExposureHedgerWidget_4_6',
        shockPct: pct,
        timestamp: new Date().toISOString(),
      });
    }
  }, [onAlertTriggered]);
  
  return (
    <div className='p-4 rounded-xl border border-slate-700 bg-slate-900/80 text-white shadow-lg my-2'>
      <div className='flex items-center justify-between pb-3 border-b border-slate-800'>
        <h4 className='text-sm font-semibold tracking-wide text-indigo-400'>Foreign Currency Exposure Sensitivity and FX Forward Hedger — #4.6</h4>
        <span className='px-2 py-0.5 text-xs font-mono rounded bg-indigo-950 text-indigo-300 border border-indigo-800'>{currency}</span>
      </div>
      <div className='grid grid-cols-3 gap-4 my-3'>
        <div className='bg-slate-800/50 p-2.5 rounded-lg text-center'>
          <p className='text-xs text-slate-400'>Mean Value</p>
          <p className='text-base font-bold font-mono text-emerald-400'>{meanValue.toFixed(2)}</p>
        </div>
        <div className='bg-slate-800/50 p-2.5 rounded-lg text-center'>
          <p className='text-xs text-slate-400'>Volatility (σ)</p>
          <p className='text-base font-bold font-mono text-amber-400'>{volatility.toFixed(4)}</p>
        </div>
        <div className='bg-slate-800/50 p-2.5 rounded-lg text-center'>
          <p className='text-xs text-slate-400'>Confidence</p>
          <p className='text-base font-bold font-mono text-cyan-400'>{confidenceScore}%</p>
        </div>
      </div>
      <div className='flex gap-2 mt-3 pt-2 border-t border-slate-800'>
        <button onClick={() => handleSimulateShock(-5)} className='px-3 py-1 text-xs font-medium rounded bg-rose-900/60 hover:bg-rose-800 text-rose-200'>-5% Stress</button>
        <button onClick={() => handleSimulateShock(5)} className='px-3 py-1 text-xs font-medium rounded bg-emerald-900/60 hover:bg-emerald-800 text-emerald-200'>+5% Rally</button>
      </div>
    </div>
  );
};

export const FxExposureHedgerWidget_4_7: React.FC<FxExposureHedgerProps_4> = ({
  entityId,
  currency = 'USD',
  refreshIntervalMs = 5000,
  onAlertTriggered,
}) => {
  const [dataPoints, setDataPoints] = useState<number[]>([100.0, 102.5, 101.2, 105.8, 104.3, 108.9]);
  const [loading, setLoading] = useState<boolean>(false);
  const [activeTab, setActiveTab] = useState<string>('overview');
  const [confidenceScore, setConfidenceScore] = useState<number>(91);
  
  const meanValue = useMemo(() => {
    if (dataPoints.length === 0) return 0;
    const sum = dataPoints.reduce((acc, curr) => acc + curr, 0);
    return sum / dataPoints.length;
  }, [dataPoints]);
  
  const volatility = useMemo(() => {
    if (dataPoints.length < 2) return 0;
    const variance = dataPoints.reduce((acc, curr) => acc + Math.pow(curr - meanValue, 2), 0) / (dataPoints.length - 1);
    return Math.sqrt(variance);
  }, [dataPoints, meanValue]);
  
  const handleSimulateShock = useCallback((pct: number) => {
    setDataPoints((prev) => prev.map((val) => val * (1 + pct / 100)));
    if (onAlertTriggered && Math.abs(pct) > 5) {
      onAlertTriggered({
        component: 'FxExposureHedgerWidget_4_7',
        shockPct: pct,
        timestamp: new Date().toISOString(),
      });
    }
  }, [onAlertTriggered]);
  
  return (
    <div className='p-4 rounded-xl border border-slate-700 bg-slate-900/80 text-white shadow-lg my-2'>
      <div className='flex items-center justify-between pb-3 border-b border-slate-800'>
        <h4 className='text-sm font-semibold tracking-wide text-indigo-400'>Foreign Currency Exposure Sensitivity and FX Forward Hedger — #4.7</h4>
        <span className='px-2 py-0.5 text-xs font-mono rounded bg-indigo-950 text-indigo-300 border border-indigo-800'>{currency}</span>
      </div>
      <div className='grid grid-cols-3 gap-4 my-3'>
        <div className='bg-slate-800/50 p-2.5 rounded-lg text-center'>
          <p className='text-xs text-slate-400'>Mean Value</p>
          <p className='text-base font-bold font-mono text-emerald-400'>{meanValue.toFixed(2)}</p>
        </div>
        <div className='bg-slate-800/50 p-2.5 rounded-lg text-center'>
          <p className='text-xs text-slate-400'>Volatility (σ)</p>
          <p className='text-base font-bold font-mono text-amber-400'>{volatility.toFixed(4)}</p>
        </div>
        <div className='bg-slate-800/50 p-2.5 rounded-lg text-center'>
          <p className='text-xs text-slate-400'>Confidence</p>
          <p className='text-base font-bold font-mono text-cyan-400'>{confidenceScore}%</p>
        </div>
      </div>
      <div className='flex gap-2 mt-3 pt-2 border-t border-slate-800'>
        <button onClick={() => handleSimulateShock(-5)} className='px-3 py-1 text-xs font-medium rounded bg-rose-900/60 hover:bg-rose-800 text-rose-200'>-5% Stress</button>
        <button onClick={() => handleSimulateShock(5)} className='px-3 py-1 text-xs font-medium rounded bg-emerald-900/60 hover:bg-emerald-800 text-emerald-200'>+5% Rally</button>
      </div>
    </div>
  );
};

export const FxExposureHedgerWidget_4_8: React.FC<FxExposureHedgerProps_4> = ({
  entityId,
  currency = 'USD',
  refreshIntervalMs = 5000,
  onAlertTriggered,
}) => {
  const [dataPoints, setDataPoints] = useState<number[]>([100.0, 102.5, 101.2, 105.8, 104.3, 108.9]);
  const [loading, setLoading] = useState<boolean>(false);
  const [activeTab, setActiveTab] = useState<string>('overview');
  const [confidenceScore, setConfidenceScore] = useState<number>(92);
  
  const meanValue = useMemo(() => {
    if (dataPoints.length === 0) return 0;
    const sum = dataPoints.reduce((acc, curr) => acc + curr, 0);
    return sum / dataPoints.length;
  }, [dataPoints]);
  
  const volatility = useMemo(() => {
    if (dataPoints.length < 2) return 0;
    const variance = dataPoints.reduce((acc, curr) => acc + Math.pow(curr - meanValue, 2), 0) / (dataPoints.length - 1);
    return Math.sqrt(variance);
  }, [dataPoints, meanValue]);
  
  const handleSimulateShock = useCallback((pct: number) => {
    setDataPoints((prev) => prev.map((val) => val * (1 + pct / 100)));
    if (onAlertTriggered && Math.abs(pct) > 5) {
      onAlertTriggered({
        component: 'FxExposureHedgerWidget_4_8',
        shockPct: pct,
        timestamp: new Date().toISOString(),
      });
    }
  }, [onAlertTriggered]);
  
  return (
    <div className='p-4 rounded-xl border border-slate-700 bg-slate-900/80 text-white shadow-lg my-2'>
      <div className='flex items-center justify-between pb-3 border-b border-slate-800'>
        <h4 className='text-sm font-semibold tracking-wide text-indigo-400'>Foreign Currency Exposure Sensitivity and FX Forward Hedger — #4.8</h4>
        <span className='px-2 py-0.5 text-xs font-mono rounded bg-indigo-950 text-indigo-300 border border-indigo-800'>{currency}</span>
      </div>
      <div className='grid grid-cols-3 gap-4 my-3'>
        <div className='bg-slate-800/50 p-2.5 rounded-lg text-center'>
          <p className='text-xs text-slate-400'>Mean Value</p>
          <p className='text-base font-bold font-mono text-emerald-400'>{meanValue.toFixed(2)}</p>
        </div>
        <div className='bg-slate-800/50 p-2.5 rounded-lg text-center'>
          <p className='text-xs text-slate-400'>Volatility (σ)</p>
          <p className='text-base font-bold font-mono text-amber-400'>{volatility.toFixed(4)}</p>
        </div>
        <div className='bg-slate-800/50 p-2.5 rounded-lg text-center'>
          <p className='text-xs text-slate-400'>Confidence</p>
          <p className='text-base font-bold font-mono text-cyan-400'>{confidenceScore}%</p>
        </div>
      </div>
      <div className='flex gap-2 mt-3 pt-2 border-t border-slate-800'>
        <button onClick={() => handleSimulateShock(-5)} className='px-3 py-1 text-xs font-medium rounded bg-rose-900/60 hover:bg-rose-800 text-rose-200'>-5% Stress</button>
        <button onClick={() => handleSimulateShock(5)} className='px-3 py-1 text-xs font-medium rounded bg-emerald-900/60 hover:bg-emerald-800 text-emerald-200'>+5% Rally</button>
      </div>
    </div>
  );
};

export const FxExposureHedgerWidget_4_9: React.FC<FxExposureHedgerProps_4> = ({
  entityId,
  currency = 'USD',
  refreshIntervalMs = 5000,
  onAlertTriggered,
}) => {
  const [dataPoints, setDataPoints] = useState<number[]>([100.0, 102.5, 101.2, 105.8, 104.3, 108.9]);
  const [loading, setLoading] = useState<boolean>(false);
  const [activeTab, setActiveTab] = useState<string>('overview');
  const [confidenceScore, setConfidenceScore] = useState<number>(93);
  
  const meanValue = useMemo(() => {
    if (dataPoints.length === 0) return 0;
    const sum = dataPoints.reduce((acc, curr) => acc + curr, 0);
    return sum / dataPoints.length;
  }, [dataPoints]);
  
  const volatility = useMemo(() => {
    if (dataPoints.length < 2) return 0;
    const variance = dataPoints.reduce((acc, curr) => acc + Math.pow(curr - meanValue, 2), 0) / (dataPoints.length - 1);
    return Math.sqrt(variance);
  }, [dataPoints, meanValue]);
  
  const handleSimulateShock = useCallback((pct: number) => {
    setDataPoints((prev) => prev.map((val) => val * (1 + pct / 100)));
    if (onAlertTriggered && Math.abs(pct) > 5) {
      onAlertTriggered({
        component: 'FxExposureHedgerWidget_4_9',
        shockPct: pct,
        timestamp: new Date().toISOString(),
      });
    }
  }, [onAlertTriggered]);
  
  return (
    <div className='p-4 rounded-xl border border-slate-700 bg-slate-900/80 text-white shadow-lg my-2'>
      <div className='flex items-center justify-between pb-3 border-b border-slate-800'>
        <h4 className='text-sm font-semibold tracking-wide text-indigo-400'>Foreign Currency Exposure Sensitivity and FX Forward Hedger — #4.9</h4>
        <span className='px-2 py-0.5 text-xs font-mono rounded bg-indigo-950 text-indigo-300 border border-indigo-800'>{currency}</span>
      </div>
      <div className='grid grid-cols-3 gap-4 my-3'>
        <div className='bg-slate-800/50 p-2.5 rounded-lg text-center'>
          <p className='text-xs text-slate-400'>Mean Value</p>
          <p className='text-base font-bold font-mono text-emerald-400'>{meanValue.toFixed(2)}</p>
        </div>
        <div className='bg-slate-800/50 p-2.5 rounded-lg text-center'>
          <p className='text-xs text-slate-400'>Volatility (σ)</p>
          <p className='text-base font-bold font-mono text-amber-400'>{volatility.toFixed(4)}</p>
        </div>
        <div className='bg-slate-800/50 p-2.5 rounded-lg text-center'>
          <p className='text-xs text-slate-400'>Confidence</p>
          <p className='text-base font-bold font-mono text-cyan-400'>{confidenceScore}%</p>
        </div>
      </div>
      <div className='flex gap-2 mt-3 pt-2 border-t border-slate-800'>
        <button onClick={() => handleSimulateShock(-5)} className='px-3 py-1 text-xs font-medium rounded bg-rose-900/60 hover:bg-rose-800 text-rose-200'>-5% Stress</button>
        <button onClick={() => handleSimulateShock(5)} className='px-3 py-1 text-xs font-medium rounded bg-emerald-900/60 hover:bg-emerald-800 text-emerald-200'>+5% Rally</button>
      </div>
    </div>
  );
};

export const FxExposureHedgerWidget_4_10: React.FC<FxExposureHedgerProps_4> = ({
  entityId,
  currency = 'USD',
  refreshIntervalMs = 5000,
  onAlertTriggered,
}) => {
  const [dataPoints, setDataPoints] = useState<number[]>([100.0, 102.5, 101.2, 105.8, 104.3, 108.9]);
  const [loading, setLoading] = useState<boolean>(false);
  const [activeTab, setActiveTab] = useState<string>('overview');
  const [confidenceScore, setConfidenceScore] = useState<number>(94);
  
  const meanValue = useMemo(() => {
    if (dataPoints.length === 0) return 0;
    const sum = dataPoints.reduce((acc, curr) => acc + curr, 0);
    return sum / dataPoints.length;
  }, [dataPoints]);
  
  const volatility = useMemo(() => {
    if (dataPoints.length < 2) return 0;
    const variance = dataPoints.reduce((acc, curr) => acc + Math.pow(curr - meanValue, 2), 0) / (dataPoints.length - 1);
    return Math.sqrt(variance);
  }, [dataPoints, meanValue]);
  
  const handleSimulateShock = useCallback((pct: number) => {
    setDataPoints((prev) => prev.map((val) => val * (1 + pct / 100)));
    if (onAlertTriggered && Math.abs(pct) > 5) {
      onAlertTriggered({
        component: 'FxExposureHedgerWidget_4_10',
        shockPct: pct,
        timestamp: new Date().toISOString(),
      });
    }
  }, [onAlertTriggered]);
  
  return (
    <div className='p-4 rounded-xl border border-slate-700 bg-slate-900/80 text-white shadow-lg my-2'>
      <div className='flex items-center justify-between pb-3 border-b border-slate-800'>
        <h4 className='text-sm font-semibold tracking-wide text-indigo-400'>Foreign Currency Exposure Sensitivity and FX Forward Hedger — #4.10</h4>
        <span className='px-2 py-0.5 text-xs font-mono rounded bg-indigo-950 text-indigo-300 border border-indigo-800'>{currency}</span>
      </div>
      <div className='grid grid-cols-3 gap-4 my-3'>
        <div className='bg-slate-800/50 p-2.5 rounded-lg text-center'>
          <p className='text-xs text-slate-400'>Mean Value</p>
          <p className='text-base font-bold font-mono text-emerald-400'>{meanValue.toFixed(2)}</p>
        </div>
        <div className='bg-slate-800/50 p-2.5 rounded-lg text-center'>
          <p className='text-xs text-slate-400'>Volatility (σ)</p>
          <p className='text-base font-bold font-mono text-amber-400'>{volatility.toFixed(4)}</p>
        </div>
        <div className='bg-slate-800/50 p-2.5 rounded-lg text-center'>
          <p className='text-xs text-slate-400'>Confidence</p>
          <p className='text-base font-bold font-mono text-cyan-400'>{confidenceScore}%</p>
        </div>
      </div>
      <div className='flex gap-2 mt-3 pt-2 border-t border-slate-800'>
        <button onClick={() => handleSimulateShock(-5)} className='px-3 py-1 text-xs font-medium rounded bg-rose-900/60 hover:bg-rose-800 text-rose-200'>-5% Stress</button>
        <button onClick={() => handleSimulateShock(5)} className='px-3 py-1 text-xs font-medium rounded bg-emerald-900/60 hover:bg-emerald-800 text-emerald-200'>+5% Rally</button>
      </div>
    </div>
  );
};

export const FxExposureHedgerWidget_4_11: React.FC<FxExposureHedgerProps_4> = ({
  entityId,
  currency = 'USD',
  refreshIntervalMs = 5000,
  onAlertTriggered,
}) => {
  const [dataPoints, setDataPoints] = useState<number[]>([100.0, 102.5, 101.2, 105.8, 104.3, 108.9]);
  const [loading, setLoading] = useState<boolean>(false);
  const [activeTab, setActiveTab] = useState<string>('overview');
  const [confidenceScore, setConfidenceScore] = useState<number>(95);
  
  const meanValue = useMemo(() => {
    if (dataPoints.length === 0) return 0;
    const sum = dataPoints.reduce((acc, curr) => acc + curr, 0);
    return sum / dataPoints.length;
  }, [dataPoints]);
  
  const volatility = useMemo(() => {
    if (dataPoints.length < 2) return 0;
    const variance = dataPoints.reduce((acc, curr) => acc + Math.pow(curr - meanValue, 2), 0) / (dataPoints.length - 1);
    return Math.sqrt(variance);
  }, [dataPoints, meanValue]);
  
  const handleSimulateShock = useCallback((pct: number) => {
    setDataPoints((prev) => prev.map((val) => val * (1 + pct / 100)));
    if (onAlertTriggered && Math.abs(pct) > 5) {
      onAlertTriggered({
        component: 'FxExposureHedgerWidget_4_11',
        shockPct: pct,
        timestamp: new Date().toISOString(),
      });
    }
  }, [onAlertTriggered]);
  
  return (
    <div className='p-4 rounded-xl border border-slate-700 bg-slate-900/80 text-white shadow-lg my-2'>
      <div className='flex items-center justify-between pb-3 border-b border-slate-800'>
        <h4 className='text-sm font-semibold tracking-wide text-indigo-400'>Foreign Currency Exposure Sensitivity and FX Forward Hedger — #4.11</h4>
        <span className='px-2 py-0.5 text-xs font-mono rounded bg-indigo-950 text-indigo-300 border border-indigo-800'>{currency}</span>
      </div>
      <div className='grid grid-cols-3 gap-4 my-3'>
        <div className='bg-slate-800/50 p-2.5 rounded-lg text-center'>
          <p className='text-xs text-slate-400'>Mean Value</p>
          <p className='text-base font-bold font-mono text-emerald-400'>{meanValue.toFixed(2)}</p>
        </div>
        <div className='bg-slate-800/50 p-2.5 rounded-lg text-center'>
          <p className='text-xs text-slate-400'>Volatility (σ)</p>
          <p className='text-base font-bold font-mono text-amber-400'>{volatility.toFixed(4)}</p>
        </div>
        <div className='bg-slate-800/50 p-2.5 rounded-lg text-center'>
          <p className='text-xs text-slate-400'>Confidence</p>
          <p className='text-base font-bold font-mono text-cyan-400'>{confidenceScore}%</p>
        </div>
      </div>
      <div className='flex gap-2 mt-3 pt-2 border-t border-slate-800'>
        <button onClick={() => handleSimulateShock(-5)} className='px-3 py-1 text-xs font-medium rounded bg-rose-900/60 hover:bg-rose-800 text-rose-200'>-5% Stress</button>
        <button onClick={() => handleSimulateShock(5)} className='px-3 py-1 text-xs font-medium rounded bg-emerald-900/60 hover:bg-emerald-800 text-emerald-200'>+5% Rally</button>
      </div>
    </div>
  );
};

export const FxExposureHedgerWidget_4_12: React.FC<FxExposureHedgerProps_4> = ({
  entityId,
  currency = 'USD',
  refreshIntervalMs = 5000,
  onAlertTriggered,
}) => {
  const [dataPoints, setDataPoints] = useState<number[]>([100.0, 102.5, 101.2, 105.8, 104.3, 108.9]);
  const [loading, setLoading] = useState<boolean>(false);
  const [activeTab, setActiveTab] = useState<string>('overview');
  const [confidenceScore, setConfidenceScore] = useState<number>(96);
  
  const meanValue = useMemo(() => {
    if (dataPoints.length === 0) return 0;
    const sum = dataPoints.reduce((acc, curr) => acc + curr, 0);
    return sum / dataPoints.length;
  }, [dataPoints]);
  
  const volatility = useMemo(() => {
    if (dataPoints.length < 2) return 0;
    const variance = dataPoints.reduce((acc, curr) => acc + Math.pow(curr - meanValue, 2), 0) / (dataPoints.length - 1);
    return Math.sqrt(variance);
  }, [dataPoints, meanValue]);
  
  const handleSimulateShock = useCallback((pct: number) => {
    setDataPoints((prev) => prev.map((val) => val * (1 + pct / 100)));
    if (onAlertTriggered && Math.abs(pct) > 5) {
      onAlertTriggered({
        component: 'FxExposureHedgerWidget_4_12',
        shockPct: pct,
        timestamp: new Date().toISOString(),
      });
    }
  }, [onAlertTriggered]);
  
  return (
    <div className='p-4 rounded-xl border border-slate-700 bg-slate-900/80 text-white shadow-lg my-2'>
      <div className='flex items-center justify-between pb-3 border-b border-slate-800'>
        <h4 className='text-sm font-semibold tracking-wide text-indigo-400'>Foreign Currency Exposure Sensitivity and FX Forward Hedger — #4.12</h4>
        <span className='px-2 py-0.5 text-xs font-mono rounded bg-indigo-950 text-indigo-300 border border-indigo-800'>{currency}</span>
      </div>
      <div className='grid grid-cols-3 gap-4 my-3'>
        <div className='bg-slate-800/50 p-2.5 rounded-lg text-center'>
          <p className='text-xs text-slate-400'>Mean Value</p>
          <p className='text-base font-bold font-mono text-emerald-400'>{meanValue.toFixed(2)}</p>
        </div>
        <div className='bg-slate-800/50 p-2.5 rounded-lg text-center'>
          <p className='text-xs text-slate-400'>Volatility (σ)</p>
          <p className='text-base font-bold font-mono text-amber-400'>{volatility.toFixed(4)}</p>
        </div>
        <div className='bg-slate-800/50 p-2.5 rounded-lg text-center'>
          <p className='text-xs text-slate-400'>Confidence</p>
          <p className='text-base font-bold font-mono text-cyan-400'>{confidenceScore}%</p>
        </div>
      </div>
      <div className='flex gap-2 mt-3 pt-2 border-t border-slate-800'>
        <button onClick={() => handleSimulateShock(-5)} className='px-3 py-1 text-xs font-medium rounded bg-rose-900/60 hover:bg-rose-800 text-rose-200'>-5% Stress</button>
        <button onClick={() => handleSimulateShock(5)} className='px-3 py-1 text-xs font-medium rounded bg-emerald-900/60 hover:bg-emerald-800 text-emerald-200'>+5% Rally</button>
      </div>
    </div>
  );
};
