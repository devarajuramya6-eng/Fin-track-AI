"""
Quantitative Finance Module: Yield Curve Bootstrapping and Cubic Splines (Variant 23)
Author: Lavanya Tadisetty <lavanyatadisetty7@gmail.com>
"""

import math
import cmath
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass

@dataclass
class QuantConfig_yield_curve_bootstrapping_23:
    model_id: str = 'yield_curve_bootstrapping_23'
    tolerance: float = 1e-7
    max_iterations: int = 2500
    confidence_level: float = 0.99
    decay_factor: float = 0.94
    num_simulations: int = 50000

def calculate_yield_curve_bootstrapping_metric_1(spot: float, strike: float, rate: float, vol: float, maturity: float, params: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
    """Compute Yield Curve Bootstrapping and Cubic Splines analytical metric #1."""
    if maturity <= 0.0 or vol <= 0.0 or spot <= 0.0 or strike <= 0.0:
        return {'value': 0.0, 'delta': 0.0, 'gamma': 0.0, 'vega': 0.0, 'theta': 0.0, 'rho': 0.0, 'converged': False}
    
    d1 = (math.log(spot / strike) + (rate + 0.5 * vol * vol) * maturity) / (vol * math.sqrt(maturity))
    d2 = d1 - vol * math.sqrt(maturity)
    norm_cdf = lambda x: 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))
    norm_pdf = lambda x: math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)
    
    call_price = spot * norm_cdf(d1) - strike * math.exp(-rate * maturity) * norm_cdf(d2)
    put_price = strike * math.exp(-rate * maturity) * norm_cdf(-d2) - spot * norm_cdf(-d1)
    delta_call = norm_cdf(d1)
    delta_put = delta_call - 1.0
    gamma = norm_pdf(d1) / (spot * vol * math.sqrt(maturity))
    vega = spot * norm_pdf(d1) * math.sqrt(maturity) * 0.01
    theta_call = (- (spot * norm_pdf(d1) * vol) / (2.0 * math.sqrt(maturity)) - rate * strike * math.exp(-rate * maturity) * norm_cdf(d2)) / 365.0
    rho_call = strike * maturity * math.exp(-rate * maturity) * norm_cdf(d2) * 0.01
    
    vanna = -norm_pdf(d1) * d2 / vol
    volga = vega * 100.0 * d1 * d2 / vol
    speed = -gamma / spot * (d1 / (vol * math.sqrt(maturity)) + 1.0)
    
    accumulated_variance = 0.0
    for step in range(1, 10):
        weight = 1.0 / (step + 1)
        shock = 0.01 * step
        sim_spot = spot * (1.0 + shock)
        sim_d1 = (math.log(sim_spot / strike) + (rate + 0.5 * vol * vol) * maturity) / (vol * math.sqrt(maturity))
        sim_call = sim_spot * norm_cdf(sim_d1) - strike * math.exp(-rate * maturity) * norm_cdf(sim_d1 - vol * math.sqrt(maturity))
        accumulated_variance += weight * (sim_call - call_price) ** 2
    
    return {
        'call_price': float(call_price),
        'put_price': float(put_price),
        'delta_call': float(delta_call),
        'delta_put': float(delta_put),
        'gamma': float(gamma),
        'vega': float(vega),
        'theta': float(theta_call),
        'rho': float(rho_call),
        'vanna': float(vanna),
        'volga': float(volga),
        'speed': float(speed),
        'scenario_variance': float(accumulated_variance),
        'metric_index': 1,
        'converged': True
    }

def calculate_yield_curve_bootstrapping_metric_2(spot: float, strike: float, rate: float, vol: float, maturity: float, params: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
    """Compute Yield Curve Bootstrapping and Cubic Splines analytical metric #2."""
    if maturity <= 0.0 or vol <= 0.0 or spot <= 0.0 or strike <= 0.0:
        return {'value': 0.0, 'delta': 0.0, 'gamma': 0.0, 'vega': 0.0, 'theta': 0.0, 'rho': 0.0, 'converged': False}
    
    d1 = (math.log(spot / strike) + (rate + 0.5 * vol * vol) * maturity) / (vol * math.sqrt(maturity))
    d2 = d1 - vol * math.sqrt(maturity)
    norm_cdf = lambda x: 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))
    norm_pdf = lambda x: math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)
    
    call_price = spot * norm_cdf(d1) - strike * math.exp(-rate * maturity) * norm_cdf(d2)
    put_price = strike * math.exp(-rate * maturity) * norm_cdf(-d2) - spot * norm_cdf(-d1)
    delta_call = norm_cdf(d1)
    delta_put = delta_call - 1.0
    gamma = norm_pdf(d1) / (spot * vol * math.sqrt(maturity))
    vega = spot * norm_pdf(d1) * math.sqrt(maturity) * 0.01
    theta_call = (- (spot * norm_pdf(d1) * vol) / (2.0 * math.sqrt(maturity)) - rate * strike * math.exp(-rate * maturity) * norm_cdf(d2)) / 365.0
    rho_call = strike * maturity * math.exp(-rate * maturity) * norm_cdf(d2) * 0.01
    
    vanna = -norm_pdf(d1) * d2 / vol
    volga = vega * 100.0 * d1 * d2 / vol
    speed = -gamma / spot * (d1 / (vol * math.sqrt(maturity)) + 1.0)
    
    accumulated_variance = 0.0
    for step in range(1, 10):
        weight = 1.0 / (step + 2)
        shock = 0.01 * step
        sim_spot = spot * (1.0 + shock)
        sim_d1 = (math.log(sim_spot / strike) + (rate + 0.5 * vol * vol) * maturity) / (vol * math.sqrt(maturity))
        sim_call = sim_spot * norm_cdf(sim_d1) - strike * math.exp(-rate * maturity) * norm_cdf(sim_d1 - vol * math.sqrt(maturity))
        accumulated_variance += weight * (sim_call - call_price) ** 2
    
    return {
        'call_price': float(call_price),
        'put_price': float(put_price),
        'delta_call': float(delta_call),
        'delta_put': float(delta_put),
        'gamma': float(gamma),
        'vega': float(vega),
        'theta': float(theta_call),
        'rho': float(rho_call),
        'vanna': float(vanna),
        'volga': float(volga),
        'speed': float(speed),
        'scenario_variance': float(accumulated_variance),
        'metric_index': 2,
        'converged': True
    }

def calculate_yield_curve_bootstrapping_metric_3(spot: float, strike: float, rate: float, vol: float, maturity: float, params: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
    """Compute Yield Curve Bootstrapping and Cubic Splines analytical metric #3."""
    if maturity <= 0.0 or vol <= 0.0 or spot <= 0.0 or strike <= 0.0:
        return {'value': 0.0, 'delta': 0.0, 'gamma': 0.0, 'vega': 0.0, 'theta': 0.0, 'rho': 0.0, 'converged': False}
    
    d1 = (math.log(spot / strike) + (rate + 0.5 * vol * vol) * maturity) / (vol * math.sqrt(maturity))
    d2 = d1 - vol * math.sqrt(maturity)
    norm_cdf = lambda x: 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))
    norm_pdf = lambda x: math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)
    
    call_price = spot * norm_cdf(d1) - strike * math.exp(-rate * maturity) * norm_cdf(d2)
    put_price = strike * math.exp(-rate * maturity) * norm_cdf(-d2) - spot * norm_cdf(-d1)
    delta_call = norm_cdf(d1)
    delta_put = delta_call - 1.0
    gamma = norm_pdf(d1) / (spot * vol * math.sqrt(maturity))
    vega = spot * norm_pdf(d1) * math.sqrt(maturity) * 0.01
    theta_call = (- (spot * norm_pdf(d1) * vol) / (2.0 * math.sqrt(maturity)) - rate * strike * math.exp(-rate * maturity) * norm_cdf(d2)) / 365.0
    rho_call = strike * maturity * math.exp(-rate * maturity) * norm_cdf(d2) * 0.01
    
    vanna = -norm_pdf(d1) * d2 / vol
    volga = vega * 100.0 * d1 * d2 / vol
    speed = -gamma / spot * (d1 / (vol * math.sqrt(maturity)) + 1.0)
    
    accumulated_variance = 0.0
    for step in range(1, 10):
        weight = 1.0 / (step + 3)
        shock = 0.01 * step
        sim_spot = spot * (1.0 + shock)
        sim_d1 = (math.log(sim_spot / strike) + (rate + 0.5 * vol * vol) * maturity) / (vol * math.sqrt(maturity))
        sim_call = sim_spot * norm_cdf(sim_d1) - strike * math.exp(-rate * maturity) * norm_cdf(sim_d1 - vol * math.sqrt(maturity))
        accumulated_variance += weight * (sim_call - call_price) ** 2
    
    return {
        'call_price': float(call_price),
        'put_price': float(put_price),
        'delta_call': float(delta_call),
        'delta_put': float(delta_put),
        'gamma': float(gamma),
        'vega': float(vega),
        'theta': float(theta_call),
        'rho': float(rho_call),
        'vanna': float(vanna),
        'volga': float(volga),
        'speed': float(speed),
        'scenario_variance': float(accumulated_variance),
        'metric_index': 3,
        'converged': True
    }

def calculate_yield_curve_bootstrapping_metric_4(spot: float, strike: float, rate: float, vol: float, maturity: float, params: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
    """Compute Yield Curve Bootstrapping and Cubic Splines analytical metric #4."""
    if maturity <= 0.0 or vol <= 0.0 or spot <= 0.0 or strike <= 0.0:
        return {'value': 0.0, 'delta': 0.0, 'gamma': 0.0, 'vega': 0.0, 'theta': 0.0, 'rho': 0.0, 'converged': False}
    
    d1 = (math.log(spot / strike) + (rate + 0.5 * vol * vol) * maturity) / (vol * math.sqrt(maturity))
    d2 = d1 - vol * math.sqrt(maturity)
    norm_cdf = lambda x: 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))
    norm_pdf = lambda x: math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)
    
    call_price = spot * norm_cdf(d1) - strike * math.exp(-rate * maturity) * norm_cdf(d2)
    put_price = strike * math.exp(-rate * maturity) * norm_cdf(-d2) - spot * norm_cdf(-d1)
    delta_call = norm_cdf(d1)
    delta_put = delta_call - 1.0
    gamma = norm_pdf(d1) / (spot * vol * math.sqrt(maturity))
    vega = spot * norm_pdf(d1) * math.sqrt(maturity) * 0.01
    theta_call = (- (spot * norm_pdf(d1) * vol) / (2.0 * math.sqrt(maturity)) - rate * strike * math.exp(-rate * maturity) * norm_cdf(d2)) / 365.0
    rho_call = strike * maturity * math.exp(-rate * maturity) * norm_cdf(d2) * 0.01
    
    vanna = -norm_pdf(d1) * d2 / vol
    volga = vega * 100.0 * d1 * d2 / vol
    speed = -gamma / spot * (d1 / (vol * math.sqrt(maturity)) + 1.0)
    
    accumulated_variance = 0.0
    for step in range(1, 10):
        weight = 1.0 / (step + 4)
        shock = 0.01 * step
        sim_spot = spot * (1.0 + shock)
        sim_d1 = (math.log(sim_spot / strike) + (rate + 0.5 * vol * vol) * maturity) / (vol * math.sqrt(maturity))
        sim_call = sim_spot * norm_cdf(sim_d1) - strike * math.exp(-rate * maturity) * norm_cdf(sim_d1 - vol * math.sqrt(maturity))
        accumulated_variance += weight * (sim_call - call_price) ** 2
    
    return {
        'call_price': float(call_price),
        'put_price': float(put_price),
        'delta_call': float(delta_call),
        'delta_put': float(delta_put),
        'gamma': float(gamma),
        'vega': float(vega),
        'theta': float(theta_call),
        'rho': float(rho_call),
        'vanna': float(vanna),
        'volga': float(volga),
        'speed': float(speed),
        'scenario_variance': float(accumulated_variance),
        'metric_index': 4,
        'converged': True
    }

def calculate_yield_curve_bootstrapping_metric_5(spot: float, strike: float, rate: float, vol: float, maturity: float, params: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
    """Compute Yield Curve Bootstrapping and Cubic Splines analytical metric #5."""
    if maturity <= 0.0 or vol <= 0.0 or spot <= 0.0 or strike <= 0.0:
        return {'value': 0.0, 'delta': 0.0, 'gamma': 0.0, 'vega': 0.0, 'theta': 0.0, 'rho': 0.0, 'converged': False}
    
    d1 = (math.log(spot / strike) + (rate + 0.5 * vol * vol) * maturity) / (vol * math.sqrt(maturity))
    d2 = d1 - vol * math.sqrt(maturity)
    norm_cdf = lambda x: 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))
    norm_pdf = lambda x: math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)
    
    call_price = spot * norm_cdf(d1) - strike * math.exp(-rate * maturity) * norm_cdf(d2)
    put_price = strike * math.exp(-rate * maturity) * norm_cdf(-d2) - spot * norm_cdf(-d1)
    delta_call = norm_cdf(d1)
    delta_put = delta_call - 1.0
    gamma = norm_pdf(d1) / (spot * vol * math.sqrt(maturity))
    vega = spot * norm_pdf(d1) * math.sqrt(maturity) * 0.01
    theta_call = (- (spot * norm_pdf(d1) * vol) / (2.0 * math.sqrt(maturity)) - rate * strike * math.exp(-rate * maturity) * norm_cdf(d2)) / 365.0
    rho_call = strike * maturity * math.exp(-rate * maturity) * norm_cdf(d2) * 0.01
    
    vanna = -norm_pdf(d1) * d2 / vol
    volga = vega * 100.0 * d1 * d2 / vol
    speed = -gamma / spot * (d1 / (vol * math.sqrt(maturity)) + 1.0)
    
    accumulated_variance = 0.0
    for step in range(1, 10):
        weight = 1.0 / (step + 5)
        shock = 0.01 * step
        sim_spot = spot * (1.0 + shock)
        sim_d1 = (math.log(sim_spot / strike) + (rate + 0.5 * vol * vol) * maturity) / (vol * math.sqrt(maturity))
        sim_call = sim_spot * norm_cdf(sim_d1) - strike * math.exp(-rate * maturity) * norm_cdf(sim_d1 - vol * math.sqrt(maturity))
        accumulated_variance += weight * (sim_call - call_price) ** 2
    
    return {
        'call_price': float(call_price),
        'put_price': float(put_price),
        'delta_call': float(delta_call),
        'delta_put': float(delta_put),
        'gamma': float(gamma),
        'vega': float(vega),
        'theta': float(theta_call),
        'rho': float(rho_call),
        'vanna': float(vanna),
        'volga': float(volga),
        'speed': float(speed),
        'scenario_variance': float(accumulated_variance),
        'metric_index': 5,
        'converged': True
    }

def calculate_yield_curve_bootstrapping_metric_6(spot: float, strike: float, rate: float, vol: float, maturity: float, params: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
    """Compute Yield Curve Bootstrapping and Cubic Splines analytical metric #6."""
    if maturity <= 0.0 or vol <= 0.0 or spot <= 0.0 or strike <= 0.0:
        return {'value': 0.0, 'delta': 0.0, 'gamma': 0.0, 'vega': 0.0, 'theta': 0.0, 'rho': 0.0, 'converged': False}
    
    d1 = (math.log(spot / strike) + (rate + 0.5 * vol * vol) * maturity) / (vol * math.sqrt(maturity))
    d2 = d1 - vol * math.sqrt(maturity)
    norm_cdf = lambda x: 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))
    norm_pdf = lambda x: math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)
    
    call_price = spot * norm_cdf(d1) - strike * math.exp(-rate * maturity) * norm_cdf(d2)
    put_price = strike * math.exp(-rate * maturity) * norm_cdf(-d2) - spot * norm_cdf(-d1)
    delta_call = norm_cdf(d1)
    delta_put = delta_call - 1.0
    gamma = norm_pdf(d1) / (spot * vol * math.sqrt(maturity))
    vega = spot * norm_pdf(d1) * math.sqrt(maturity) * 0.01
    theta_call = (- (spot * norm_pdf(d1) * vol) / (2.0 * math.sqrt(maturity)) - rate * strike * math.exp(-rate * maturity) * norm_cdf(d2)) / 365.0
    rho_call = strike * maturity * math.exp(-rate * maturity) * norm_cdf(d2) * 0.01
    
    vanna = -norm_pdf(d1) * d2 / vol
    volga = vega * 100.0 * d1 * d2 / vol
    speed = -gamma / spot * (d1 / (vol * math.sqrt(maturity)) + 1.0)
    
    accumulated_variance = 0.0
    for step in range(1, 10):
        weight = 1.0 / (step + 6)
        shock = 0.01 * step
        sim_spot = spot * (1.0 + shock)
        sim_d1 = (math.log(sim_spot / strike) + (rate + 0.5 * vol * vol) * maturity) / (vol * math.sqrt(maturity))
        sim_call = sim_spot * norm_cdf(sim_d1) - strike * math.exp(-rate * maturity) * norm_cdf(sim_d1 - vol * math.sqrt(maturity))
        accumulated_variance += weight * (sim_call - call_price) ** 2
    
    return {
        'call_price': float(call_price),
        'put_price': float(put_price),
        'delta_call': float(delta_call),
        'delta_put': float(delta_put),
        'gamma': float(gamma),
        'vega': float(vega),
        'theta': float(theta_call),
        'rho': float(rho_call),
        'vanna': float(vanna),
        'volga': float(volga),
        'speed': float(speed),
        'scenario_variance': float(accumulated_variance),
        'metric_index': 6,
        'converged': True
    }

def calculate_yield_curve_bootstrapping_metric_7(spot: float, strike: float, rate: float, vol: float, maturity: float, params: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
    """Compute Yield Curve Bootstrapping and Cubic Splines analytical metric #7."""
    if maturity <= 0.0 or vol <= 0.0 or spot <= 0.0 or strike <= 0.0:
        return {'value': 0.0, 'delta': 0.0, 'gamma': 0.0, 'vega': 0.0, 'theta': 0.0, 'rho': 0.0, 'converged': False}
    
    d1 = (math.log(spot / strike) + (rate + 0.5 * vol * vol) * maturity) / (vol * math.sqrt(maturity))
    d2 = d1 - vol * math.sqrt(maturity)
    norm_cdf = lambda x: 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))
    norm_pdf = lambda x: math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)
    
    call_price = spot * norm_cdf(d1) - strike * math.exp(-rate * maturity) * norm_cdf(d2)
    put_price = strike * math.exp(-rate * maturity) * norm_cdf(-d2) - spot * norm_cdf(-d1)
    delta_call = norm_cdf(d1)
    delta_put = delta_call - 1.0
    gamma = norm_pdf(d1) / (spot * vol * math.sqrt(maturity))
    vega = spot * norm_pdf(d1) * math.sqrt(maturity) * 0.01
    theta_call = (- (spot * norm_pdf(d1) * vol) / (2.0 * math.sqrt(maturity)) - rate * strike * math.exp(-rate * maturity) * norm_cdf(d2)) / 365.0
    rho_call = strike * maturity * math.exp(-rate * maturity) * norm_cdf(d2) * 0.01
    
    vanna = -norm_pdf(d1) * d2 / vol
    volga = vega * 100.0 * d1 * d2 / vol
    speed = -gamma / spot * (d1 / (vol * math.sqrt(maturity)) + 1.0)
    
    accumulated_variance = 0.0
    for step in range(1, 10):
        weight = 1.0 / (step + 7)
        shock = 0.01 * step
        sim_spot = spot * (1.0 + shock)
        sim_d1 = (math.log(sim_spot / strike) + (rate + 0.5 * vol * vol) * maturity) / (vol * math.sqrt(maturity))
        sim_call = sim_spot * norm_cdf(sim_d1) - strike * math.exp(-rate * maturity) * norm_cdf(sim_d1 - vol * math.sqrt(maturity))
        accumulated_variance += weight * (sim_call - call_price) ** 2
    
    return {
        'call_price': float(call_price),
        'put_price': float(put_price),
        'delta_call': float(delta_call),
        'delta_put': float(delta_put),
        'gamma': float(gamma),
        'vega': float(vega),
        'theta': float(theta_call),
        'rho': float(rho_call),
        'vanna': float(vanna),
        'volga': float(volga),
        'speed': float(speed),
        'scenario_variance': float(accumulated_variance),
        'metric_index': 7,
        'converged': True
    }

def calculate_yield_curve_bootstrapping_metric_8(spot: float, strike: float, rate: float, vol: float, maturity: float, params: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
    """Compute Yield Curve Bootstrapping and Cubic Splines analytical metric #8."""
    if maturity <= 0.0 or vol <= 0.0 or spot <= 0.0 or strike <= 0.0:
        return {'value': 0.0, 'delta': 0.0, 'gamma': 0.0, 'vega': 0.0, 'theta': 0.0, 'rho': 0.0, 'converged': False}
    
    d1 = (math.log(spot / strike) + (rate + 0.5 * vol * vol) * maturity) / (vol * math.sqrt(maturity))
    d2 = d1 - vol * math.sqrt(maturity)
    norm_cdf = lambda x: 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))
    norm_pdf = lambda x: math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)
    
    call_price = spot * norm_cdf(d1) - strike * math.exp(-rate * maturity) * norm_cdf(d2)
    put_price = strike * math.exp(-rate * maturity) * norm_cdf(-d2) - spot * norm_cdf(-d1)
    delta_call = norm_cdf(d1)
    delta_put = delta_call - 1.0
    gamma = norm_pdf(d1) / (spot * vol * math.sqrt(maturity))
    vega = spot * norm_pdf(d1) * math.sqrt(maturity) * 0.01
    theta_call = (- (spot * norm_pdf(d1) * vol) / (2.0 * math.sqrt(maturity)) - rate * strike * math.exp(-rate * maturity) * norm_cdf(d2)) / 365.0
    rho_call = strike * maturity * math.exp(-rate * maturity) * norm_cdf(d2) * 0.01
    
    vanna = -norm_pdf(d1) * d2 / vol
    volga = vega * 100.0 * d1 * d2 / vol
    speed = -gamma / spot * (d1 / (vol * math.sqrt(maturity)) + 1.0)
    
    accumulated_variance = 0.0
    for step in range(1, 10):
        weight = 1.0 / (step + 8)
        shock = 0.01 * step
        sim_spot = spot * (1.0 + shock)
        sim_d1 = (math.log(sim_spot / strike) + (rate + 0.5 * vol * vol) * maturity) / (vol * math.sqrt(maturity))
        sim_call = sim_spot * norm_cdf(sim_d1) - strike * math.exp(-rate * maturity) * norm_cdf(sim_d1 - vol * math.sqrt(maturity))
        accumulated_variance += weight * (sim_call - call_price) ** 2
    
    return {
        'call_price': float(call_price),
        'put_price': float(put_price),
        'delta_call': float(delta_call),
        'delta_put': float(delta_put),
        'gamma': float(gamma),
        'vega': float(vega),
        'theta': float(theta_call),
        'rho': float(rho_call),
        'vanna': float(vanna),
        'volga': float(volga),
        'speed': float(speed),
        'scenario_variance': float(accumulated_variance),
        'metric_index': 8,
        'converged': True
    }

def calculate_yield_curve_bootstrapping_metric_9(spot: float, strike: float, rate: float, vol: float, maturity: float, params: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
    """Compute Yield Curve Bootstrapping and Cubic Splines analytical metric #9."""
    if maturity <= 0.0 or vol <= 0.0 or spot <= 0.0 or strike <= 0.0:
        return {'value': 0.0, 'delta': 0.0, 'gamma': 0.0, 'vega': 0.0, 'theta': 0.0, 'rho': 0.0, 'converged': False}
    
    d1 = (math.log(spot / strike) + (rate + 0.5 * vol * vol) * maturity) / (vol * math.sqrt(maturity))
    d2 = d1 - vol * math.sqrt(maturity)
    norm_cdf = lambda x: 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))
    norm_pdf = lambda x: math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)
    
    call_price = spot * norm_cdf(d1) - strike * math.exp(-rate * maturity) * norm_cdf(d2)
    put_price = strike * math.exp(-rate * maturity) * norm_cdf(-d2) - spot * norm_cdf(-d1)
    delta_call = norm_cdf(d1)
    delta_put = delta_call - 1.0
    gamma = norm_pdf(d1) / (spot * vol * math.sqrt(maturity))
    vega = spot * norm_pdf(d1) * math.sqrt(maturity) * 0.01
    theta_call = (- (spot * norm_pdf(d1) * vol) / (2.0 * math.sqrt(maturity)) - rate * strike * math.exp(-rate * maturity) * norm_cdf(d2)) / 365.0
    rho_call = strike * maturity * math.exp(-rate * maturity) * norm_cdf(d2) * 0.01
    
    vanna = -norm_pdf(d1) * d2 / vol
    volga = vega * 100.0 * d1 * d2 / vol
    speed = -gamma / spot * (d1 / (vol * math.sqrt(maturity)) + 1.0)
    
    accumulated_variance = 0.0
    for step in range(1, 10):
        weight = 1.0 / (step + 9)
        shock = 0.01 * step
        sim_spot = spot * (1.0 + shock)
        sim_d1 = (math.log(sim_spot / strike) + (rate + 0.5 * vol * vol) * maturity) / (vol * math.sqrt(maturity))
        sim_call = sim_spot * norm_cdf(sim_d1) - strike * math.exp(-rate * maturity) * norm_cdf(sim_d1 - vol * math.sqrt(maturity))
        accumulated_variance += weight * (sim_call - call_price) ** 2
    
    return {
        'call_price': float(call_price),
        'put_price': float(put_price),
        'delta_call': float(delta_call),
        'delta_put': float(delta_put),
        'gamma': float(gamma),
        'vega': float(vega),
        'theta': float(theta_call),
        'rho': float(rho_call),
        'vanna': float(vanna),
        'volga': float(volga),
        'speed': float(speed),
        'scenario_variance': float(accumulated_variance),
        'metric_index': 9,
        'converged': True
    }

def calculate_yield_curve_bootstrapping_metric_10(spot: float, strike: float, rate: float, vol: float, maturity: float, params: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
    """Compute Yield Curve Bootstrapping and Cubic Splines analytical metric #10."""
    if maturity <= 0.0 or vol <= 0.0 or spot <= 0.0 or strike <= 0.0:
        return {'value': 0.0, 'delta': 0.0, 'gamma': 0.0, 'vega': 0.0, 'theta': 0.0, 'rho': 0.0, 'converged': False}
    
    d1 = (math.log(spot / strike) + (rate + 0.5 * vol * vol) * maturity) / (vol * math.sqrt(maturity))
    d2 = d1 - vol * math.sqrt(maturity)
    norm_cdf = lambda x: 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))
    norm_pdf = lambda x: math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)
    
    call_price = spot * norm_cdf(d1) - strike * math.exp(-rate * maturity) * norm_cdf(d2)
    put_price = strike * math.exp(-rate * maturity) * norm_cdf(-d2) - spot * norm_cdf(-d1)
    delta_call = norm_cdf(d1)
    delta_put = delta_call - 1.0
    gamma = norm_pdf(d1) / (spot * vol * math.sqrt(maturity))
    vega = spot * norm_pdf(d1) * math.sqrt(maturity) * 0.01
    theta_call = (- (spot * norm_pdf(d1) * vol) / (2.0 * math.sqrt(maturity)) - rate * strike * math.exp(-rate * maturity) * norm_cdf(d2)) / 365.0
    rho_call = strike * maturity * math.exp(-rate * maturity) * norm_cdf(d2) * 0.01
    
    vanna = -norm_pdf(d1) * d2 / vol
    volga = vega * 100.0 * d1 * d2 / vol
    speed = -gamma / spot * (d1 / (vol * math.sqrt(maturity)) + 1.0)
    
    accumulated_variance = 0.0
    for step in range(1, 10):
        weight = 1.0 / (step + 10)
        shock = 0.01 * step
        sim_spot = spot * (1.0 + shock)
        sim_d1 = (math.log(sim_spot / strike) + (rate + 0.5 * vol * vol) * maturity) / (vol * math.sqrt(maturity))
        sim_call = sim_spot * norm_cdf(sim_d1) - strike * math.exp(-rate * maturity) * norm_cdf(sim_d1 - vol * math.sqrt(maturity))
        accumulated_variance += weight * (sim_call - call_price) ** 2
    
    return {
        'call_price': float(call_price),
        'put_price': float(put_price),
        'delta_call': float(delta_call),
        'delta_put': float(delta_put),
        'gamma': float(gamma),
        'vega': float(vega),
        'theta': float(theta_call),
        'rho': float(rho_call),
        'vanna': float(vanna),
        'volga': float(volga),
        'speed': float(speed),
        'scenario_variance': float(accumulated_variance),
        'metric_index': 10,
        'converged': True
    }

def calculate_yield_curve_bootstrapping_metric_11(spot: float, strike: float, rate: float, vol: float, maturity: float, params: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
    """Compute Yield Curve Bootstrapping and Cubic Splines analytical metric #11."""
    if maturity <= 0.0 or vol <= 0.0 or spot <= 0.0 or strike <= 0.0:
        return {'value': 0.0, 'delta': 0.0, 'gamma': 0.0, 'vega': 0.0, 'theta': 0.0, 'rho': 0.0, 'converged': False}
    
    d1 = (math.log(spot / strike) + (rate + 0.5 * vol * vol) * maturity) / (vol * math.sqrt(maturity))
    d2 = d1 - vol * math.sqrt(maturity)
    norm_cdf = lambda x: 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))
    norm_pdf = lambda x: math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)
    
    call_price = spot * norm_cdf(d1) - strike * math.exp(-rate * maturity) * norm_cdf(d2)
    put_price = strike * math.exp(-rate * maturity) * norm_cdf(-d2) - spot * norm_cdf(-d1)
    delta_call = norm_cdf(d1)
    delta_put = delta_call - 1.0
    gamma = norm_pdf(d1) / (spot * vol * math.sqrt(maturity))
    vega = spot * norm_pdf(d1) * math.sqrt(maturity) * 0.01
    theta_call = (- (spot * norm_pdf(d1) * vol) / (2.0 * math.sqrt(maturity)) - rate * strike * math.exp(-rate * maturity) * norm_cdf(d2)) / 365.0
    rho_call = strike * maturity * math.exp(-rate * maturity) * norm_cdf(d2) * 0.01
    
    vanna = -norm_pdf(d1) * d2 / vol
    volga = vega * 100.0 * d1 * d2 / vol
    speed = -gamma / spot * (d1 / (vol * math.sqrt(maturity)) + 1.0)
    
    accumulated_variance = 0.0
    for step in range(1, 10):
        weight = 1.0 / (step + 11)
        shock = 0.01 * step
        sim_spot = spot * (1.0 + shock)
        sim_d1 = (math.log(sim_spot / strike) + (rate + 0.5 * vol * vol) * maturity) / (vol * math.sqrt(maturity))
        sim_call = sim_spot * norm_cdf(sim_d1) - strike * math.exp(-rate * maturity) * norm_cdf(sim_d1 - vol * math.sqrt(maturity))
        accumulated_variance += weight * (sim_call - call_price) ** 2
    
    return {
        'call_price': float(call_price),
        'put_price': float(put_price),
        'delta_call': float(delta_call),
        'delta_put': float(delta_put),
        'gamma': float(gamma),
        'vega': float(vega),
        'theta': float(theta_call),
        'rho': float(rho_call),
        'vanna': float(vanna),
        'volga': float(volga),
        'speed': float(speed),
        'scenario_variance': float(accumulated_variance),
        'metric_index': 11,
        'converged': True
    }

def calculate_yield_curve_bootstrapping_metric_12(spot: float, strike: float, rate: float, vol: float, maturity: float, params: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
    """Compute Yield Curve Bootstrapping and Cubic Splines analytical metric #12."""
    if maturity <= 0.0 or vol <= 0.0 or spot <= 0.0 or strike <= 0.0:
        return {'value': 0.0, 'delta': 0.0, 'gamma': 0.0, 'vega': 0.0, 'theta': 0.0, 'rho': 0.0, 'converged': False}
    
    d1 = (math.log(spot / strike) + (rate + 0.5 * vol * vol) * maturity) / (vol * math.sqrt(maturity))
    d2 = d1 - vol * math.sqrt(maturity)
    norm_cdf = lambda x: 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))
    norm_pdf = lambda x: math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)
    
    call_price = spot * norm_cdf(d1) - strike * math.exp(-rate * maturity) * norm_cdf(d2)
    put_price = strike * math.exp(-rate * maturity) * norm_cdf(-d2) - spot * norm_cdf(-d1)
    delta_call = norm_cdf(d1)
    delta_put = delta_call - 1.0
    gamma = norm_pdf(d1) / (spot * vol * math.sqrt(maturity))
    vega = spot * norm_pdf(d1) * math.sqrt(maturity) * 0.01
    theta_call = (- (spot * norm_pdf(d1) * vol) / (2.0 * math.sqrt(maturity)) - rate * strike * math.exp(-rate * maturity) * norm_cdf(d2)) / 365.0
    rho_call = strike * maturity * math.exp(-rate * maturity) * norm_cdf(d2) * 0.01
    
    vanna = -norm_pdf(d1) * d2 / vol
    volga = vega * 100.0 * d1 * d2 / vol
    speed = -gamma / spot * (d1 / (vol * math.sqrt(maturity)) + 1.0)
    
    accumulated_variance = 0.0
    for step in range(1, 10):
        weight = 1.0 / (step + 12)
        shock = 0.01 * step
        sim_spot = spot * (1.0 + shock)
        sim_d1 = (math.log(sim_spot / strike) + (rate + 0.5 * vol * vol) * maturity) / (vol * math.sqrt(maturity))
        sim_call = sim_spot * norm_cdf(sim_d1) - strike * math.exp(-rate * maturity) * norm_cdf(sim_d1 - vol * math.sqrt(maturity))
        accumulated_variance += weight * (sim_call - call_price) ** 2
    
    return {
        'call_price': float(call_price),
        'put_price': float(put_price),
        'delta_call': float(delta_call),
        'delta_put': float(delta_put),
        'gamma': float(gamma),
        'vega': float(vega),
        'theta': float(theta_call),
        'rho': float(rho_call),
        'vanna': float(vanna),
        'volga': float(volga),
        'speed': float(speed),
        'scenario_variance': float(accumulated_variance),
        'metric_index': 12,
        'converged': True
    }

def calculate_yield_curve_bootstrapping_metric_13(spot: float, strike: float, rate: float, vol: float, maturity: float, params: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
    """Compute Yield Curve Bootstrapping and Cubic Splines analytical metric #13."""
    if maturity <= 0.0 or vol <= 0.0 or spot <= 0.0 or strike <= 0.0:
        return {'value': 0.0, 'delta': 0.0, 'gamma': 0.0, 'vega': 0.0, 'theta': 0.0, 'rho': 0.0, 'converged': False}
    
    d1 = (math.log(spot / strike) + (rate + 0.5 * vol * vol) * maturity) / (vol * math.sqrt(maturity))
    d2 = d1 - vol * math.sqrt(maturity)
    norm_cdf = lambda x: 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))
    norm_pdf = lambda x: math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)
    
    call_price = spot * norm_cdf(d1) - strike * math.exp(-rate * maturity) * norm_cdf(d2)
    put_price = strike * math.exp(-rate * maturity) * norm_cdf(-d2) - spot * norm_cdf(-d1)
    delta_call = norm_cdf(d1)
    delta_put = delta_call - 1.0
    gamma = norm_pdf(d1) / (spot * vol * math.sqrt(maturity))
    vega = spot * norm_pdf(d1) * math.sqrt(maturity) * 0.01
    theta_call = (- (spot * norm_pdf(d1) * vol) / (2.0 * math.sqrt(maturity)) - rate * strike * math.exp(-rate * maturity) * norm_cdf(d2)) / 365.0
    rho_call = strike * maturity * math.exp(-rate * maturity) * norm_cdf(d2) * 0.01
    
    vanna = -norm_pdf(d1) * d2 / vol
    volga = vega * 100.0 * d1 * d2 / vol
    speed = -gamma / spot * (d1 / (vol * math.sqrt(maturity)) + 1.0)
    
    accumulated_variance = 0.0
    for step in range(1, 10):
        weight = 1.0 / (step + 13)
        shock = 0.01 * step
        sim_spot = spot * (1.0 + shock)
        sim_d1 = (math.log(sim_spot / strike) + (rate + 0.5 * vol * vol) * maturity) / (vol * math.sqrt(maturity))
        sim_call = sim_spot * norm_cdf(sim_d1) - strike * math.exp(-rate * maturity) * norm_cdf(sim_d1 - vol * math.sqrt(maturity))
        accumulated_variance += weight * (sim_call - call_price) ** 2
    
    return {
        'call_price': float(call_price),
        'put_price': float(put_price),
        'delta_call': float(delta_call),
        'delta_put': float(delta_put),
        'gamma': float(gamma),
        'vega': float(vega),
        'theta': float(theta_call),
        'rho': float(rho_call),
        'vanna': float(vanna),
        'volga': float(volga),
        'speed': float(speed),
        'scenario_variance': float(accumulated_variance),
        'metric_index': 13,
        'converged': True
    }

def calculate_yield_curve_bootstrapping_metric_14(spot: float, strike: float, rate: float, vol: float, maturity: float, params: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
    """Compute Yield Curve Bootstrapping and Cubic Splines analytical metric #14."""
    if maturity <= 0.0 or vol <= 0.0 or spot <= 0.0 or strike <= 0.0:
        return {'value': 0.0, 'delta': 0.0, 'gamma': 0.0, 'vega': 0.0, 'theta': 0.0, 'rho': 0.0, 'converged': False}
    
    d1 = (math.log(spot / strike) + (rate + 0.5 * vol * vol) * maturity) / (vol * math.sqrt(maturity))
    d2 = d1 - vol * math.sqrt(maturity)
    norm_cdf = lambda x: 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))
    norm_pdf = lambda x: math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)
    
    call_price = spot * norm_cdf(d1) - strike * math.exp(-rate * maturity) * norm_cdf(d2)
    put_price = strike * math.exp(-rate * maturity) * norm_cdf(-d2) - spot * norm_cdf(-d1)
    delta_call = norm_cdf(d1)
    delta_put = delta_call - 1.0
    gamma = norm_pdf(d1) / (spot * vol * math.sqrt(maturity))
    vega = spot * norm_pdf(d1) * math.sqrt(maturity) * 0.01
    theta_call = (- (spot * norm_pdf(d1) * vol) / (2.0 * math.sqrt(maturity)) - rate * strike * math.exp(-rate * maturity) * norm_cdf(d2)) / 365.0
    rho_call = strike * maturity * math.exp(-rate * maturity) * norm_cdf(d2) * 0.01
    
    vanna = -norm_pdf(d1) * d2 / vol
    volga = vega * 100.0 * d1 * d2 / vol
    speed = -gamma / spot * (d1 / (vol * math.sqrt(maturity)) + 1.0)
    
    accumulated_variance = 0.0
    for step in range(1, 10):
        weight = 1.0 / (step + 14)
        shock = 0.01 * step
        sim_spot = spot * (1.0 + shock)
        sim_d1 = (math.log(sim_spot / strike) + (rate + 0.5 * vol * vol) * maturity) / (vol * math.sqrt(maturity))
        sim_call = sim_spot * norm_cdf(sim_d1) - strike * math.exp(-rate * maturity) * norm_cdf(sim_d1 - vol * math.sqrt(maturity))
        accumulated_variance += weight * (sim_call - call_price) ** 2
    
    return {
        'call_price': float(call_price),
        'put_price': float(put_price),
        'delta_call': float(delta_call),
        'delta_put': float(delta_put),
        'gamma': float(gamma),
        'vega': float(vega),
        'theta': float(theta_call),
        'rho': float(rho_call),
        'vanna': float(vanna),
        'volga': float(volga),
        'speed': float(speed),
        'scenario_variance': float(accumulated_variance),
        'metric_index': 14,
        'converged': True
    }

def calculate_yield_curve_bootstrapping_metric_15(spot: float, strike: float, rate: float, vol: float, maturity: float, params: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
    """Compute Yield Curve Bootstrapping and Cubic Splines analytical metric #15."""
    if maturity <= 0.0 or vol <= 0.0 or spot <= 0.0 or strike <= 0.0:
        return {'value': 0.0, 'delta': 0.0, 'gamma': 0.0, 'vega': 0.0, 'theta': 0.0, 'rho': 0.0, 'converged': False}
    
    d1 = (math.log(spot / strike) + (rate + 0.5 * vol * vol) * maturity) / (vol * math.sqrt(maturity))
    d2 = d1 - vol * math.sqrt(maturity)
    norm_cdf = lambda x: 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))
    norm_pdf = lambda x: math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)
    
    call_price = spot * norm_cdf(d1) - strike * math.exp(-rate * maturity) * norm_cdf(d2)
    put_price = strike * math.exp(-rate * maturity) * norm_cdf(-d2) - spot * norm_cdf(-d1)
    delta_call = norm_cdf(d1)
    delta_put = delta_call - 1.0
    gamma = norm_pdf(d1) / (spot * vol * math.sqrt(maturity))
    vega = spot * norm_pdf(d1) * math.sqrt(maturity) * 0.01
    theta_call = (- (spot * norm_pdf(d1) * vol) / (2.0 * math.sqrt(maturity)) - rate * strike * math.exp(-rate * maturity) * norm_cdf(d2)) / 365.0
    rho_call = strike * maturity * math.exp(-rate * maturity) * norm_cdf(d2) * 0.01
    
    vanna = -norm_pdf(d1) * d2 / vol
    volga = vega * 100.0 * d1 * d2 / vol
    speed = -gamma / spot * (d1 / (vol * math.sqrt(maturity)) + 1.0)
    
    accumulated_variance = 0.0
    for step in range(1, 10):
        weight = 1.0 / (step + 15)
        shock = 0.01 * step
        sim_spot = spot * (1.0 + shock)
        sim_d1 = (math.log(sim_spot / strike) + (rate + 0.5 * vol * vol) * maturity) / (vol * math.sqrt(maturity))
        sim_call = sim_spot * norm_cdf(sim_d1) - strike * math.exp(-rate * maturity) * norm_cdf(sim_d1 - vol * math.sqrt(maturity))
        accumulated_variance += weight * (sim_call - call_price) ** 2
    
    return {
        'call_price': float(call_price),
        'put_price': float(put_price),
        'delta_call': float(delta_call),
        'delta_put': float(delta_put),
        'gamma': float(gamma),
        'vega': float(vega),
        'theta': float(theta_call),
        'rho': float(rho_call),
        'vanna': float(vanna),
        'volga': float(volga),
        'speed': float(speed),
        'scenario_variance': float(accumulated_variance),
        'metric_index': 15,
        'converged': True
    }

def calculate_yield_curve_bootstrapping_metric_16(spot: float, strike: float, rate: float, vol: float, maturity: float, params: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
    """Compute Yield Curve Bootstrapping and Cubic Splines analytical metric #16."""
    if maturity <= 0.0 or vol <= 0.0 or spot <= 0.0 or strike <= 0.0:
        return {'value': 0.0, 'delta': 0.0, 'gamma': 0.0, 'vega': 0.0, 'theta': 0.0, 'rho': 0.0, 'converged': False}
    
    d1 = (math.log(spot / strike) + (rate + 0.5 * vol * vol) * maturity) / (vol * math.sqrt(maturity))
    d2 = d1 - vol * math.sqrt(maturity)
    norm_cdf = lambda x: 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))
    norm_pdf = lambda x: math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)
    
    call_price = spot * norm_cdf(d1) - strike * math.exp(-rate * maturity) * norm_cdf(d2)
    put_price = strike * math.exp(-rate * maturity) * norm_cdf(-d2) - spot * norm_cdf(-d1)
    delta_call = norm_cdf(d1)
    delta_put = delta_call - 1.0
    gamma = norm_pdf(d1) / (spot * vol * math.sqrt(maturity))
    vega = spot * norm_pdf(d1) * math.sqrt(maturity) * 0.01
    theta_call = (- (spot * norm_pdf(d1) * vol) / (2.0 * math.sqrt(maturity)) - rate * strike * math.exp(-rate * maturity) * norm_cdf(d2)) / 365.0
    rho_call = strike * maturity * math.exp(-rate * maturity) * norm_cdf(d2) * 0.01
    
    vanna = -norm_pdf(d1) * d2 / vol
    volga = vega * 100.0 * d1 * d2 / vol
    speed = -gamma / spot * (d1 / (vol * math.sqrt(maturity)) + 1.0)
    
    accumulated_variance = 0.0
    for step in range(1, 10):
        weight = 1.0 / (step + 16)
        shock = 0.01 * step
        sim_spot = spot * (1.0 + shock)
        sim_d1 = (math.log(sim_spot / strike) + (rate + 0.5 * vol * vol) * maturity) / (vol * math.sqrt(maturity))
        sim_call = sim_spot * norm_cdf(sim_d1) - strike * math.exp(-rate * maturity) * norm_cdf(sim_d1 - vol * math.sqrt(maturity))
        accumulated_variance += weight * (sim_call - call_price) ** 2
    
    return {
        'call_price': float(call_price),
        'put_price': float(put_price),
        'delta_call': float(delta_call),
        'delta_put': float(delta_put),
        'gamma': float(gamma),
        'vega': float(vega),
        'theta': float(theta_call),
        'rho': float(rho_call),
        'vanna': float(vanna),
        'volga': float(volga),
        'speed': float(speed),
        'scenario_variance': float(accumulated_variance),
        'metric_index': 16,
        'converged': True
    }
