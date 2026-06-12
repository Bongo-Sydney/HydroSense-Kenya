"""
Unit tests for simulation methods (Level 5)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import numpy as np
from src.simulation import water_balance_euler, water_balance_runge_kutta, monte_carlo_rainfall


def test_euler_no_change():
    """If inputs are zero, soil moisture should stay constant"""
    S0 = 30.0
    rainfall = np.zeros(10)
    irrigation = np.zeros(10)
    ET = np.zeros(10)
    drainage_coef = 0
    
    S = water_balance_euler(S0, rainfall, irrigation, ET, drainage_coef)
    assert np.all(S == S0)


def test_euler_drainage_only():
    """With drainage only, moisture should decrease exponentially"""
    S0 = 30.0
    rainfall = np.zeros(10)
    irrigation = np.zeros(10)
    ET = np.zeros(10)
    drainage_coef = 0.1
    dt = 1.0
    
    S = water_balance_euler(S0, rainfall, irrigation, ET, drainage_coef, dt)
    
    # Euler: S[t+1] = S[t] - drainage_coef*S[t]
    expected = S0 * (1 - drainage_coef) ** np.arange(10)
    assert np.allclose(S, expected, rtol=1e-5)


def test_euler_vs_rk4_initial():
    """Both methods should start at same initial condition"""
    S0 = 28.0
    rainfall = np.random.uniform(0, 20, 30)
    irrigation = np.zeros(30)
    ET = np.random.uniform(2, 6, 30)
    drainage_coef = 0.15
    
    S_euler = water_balance_euler(S0, rainfall, irrigation, ET, drainage_coef)
    S_rk4 = water_balance_runge_kutta(S0, rainfall, irrigation, ET, drainage_coef)
    
    assert S_euler[0] == S_rk4[0] == S0


def test_moisture_non_negative():
    """Soil moisture should never go below zero"""
    S0 = 10.0
    rainfall = np.zeros(30)
    irrigation = np.zeros(30)
    ET = np.ones(30) * 100  # Very high ET
    drainage_coef = 0.5
    
    S_euler = water_balance_euler(S0, rainfall, irrigation, ET, drainage_coef)
    S_rk4 = water_balance_runge_kutta(S0, rainfall, irrigation, ET, drainage_coef)
    
    assert np.all(S_euler >= 0)
    assert np.all(S_rk4 >= 0)


def test_monte_carlo_dimensions():
    historical = np.array([0, 5, 10, 15, 20, 25])
    n_scenarios = 100
    n_days = 30
    
    scenarios = monte_carlo_rainfall(historical, n_scenarios, n_days)
    
    assert scenarios.shape == (n_scenarios, n_days)
    assert np.all(scenarios >= 0)
    assert np.all(scenarios <= np.max(historical))


def test_monte_carlo_mean():
    """Mean of many scenarios should approximate historical mean"""
    historical = np.array([0, 5, 10, 15, 20, 25])
    n_scenarios = 10000
    n_days = 100
    
    scenarios = monte_carlo_rainfall(historical, n_scenarios, n_days)
    
    historical_mean = np.mean(historical)
    scenario_mean = np.mean(scenarios)
    
    assert abs(scenario_mean - historical_mean) < 0.5  # Within 0.5 mm


if __name__ == "__main__":
    pytest.main([__file__, "-v"])