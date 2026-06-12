import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import numpy as np
from src.numerical_methods import trapezoidal_rule, simpsons_13_rule, cumulative_water_deficit


def test_trapezoidal_linear():
    """Trapezoidal rule should be exact for linear functions"""
    x = np.linspace(0, 10, 11)
    y = 2*x + 1  # Linear function
    exact = 110  # ∫(2x+1)dx from 0 to 10 = 110
    
    result = trapezoidal_rule(y, x)
    assert abs(result - exact) < 1e-10


def test_trapezoidal_quadratic():
    """Trapezoidal rule has O(h²) error for quadratic"""
    x = np.linspace(0, 10, 11)
    y = x**2
    exact = 1000/3  # 333.333...
    
    result = trapezoidal_rule(y, x)
    error = abs(result - exact)
    assert error < 0.5  # Should be within ~0.3


def test_simpsons_quadratic():
    """Simpson's rule should be exact for quadratic (degree ≤ 3)"""
    x = np.linspace(0, 10, 11)  # 11 points = 10 intervals (even)
    y = x**2
    exact = 1000/3
    
    result = simpsons_13_rule(y, x)
    assert abs(result - exact) < 1e-10


def test_simpsons_even_points():
    """Simpson's rule requires odd number of points (even intervals)"""
    x = np.linspace(0, 10, 10)  # 10 points = 9 intervals (odd)
    y = x**2
    
    with pytest.raises(ValueError):
        simpsons_13_rule(y, x)


def test_cumulative_deficit():
    """Cumulative deficit should be zero when ET ≤ Rain + I"""
    et = np.array([2, 2, 2])
    rain = np.array([3, 3, 3])
    irrigation = np.array([0, 0, 0])
    time = np.array([0, 1, 2])
    
    deficit = cumulative_water_deficit(et, rain, irrigation, time)
    assert deficit == 0  # No deficit when rain exceeds ET


def test_cumulative_deficit_positive():
    """Cumulative deficit should be positive when ET > Rain + I"""
    et = np.array([5, 5, 5])
    rain = np.array([1, 1, 1])
    irrigation = np.array([0, 0, 0])
    time = np.array([0, 1, 2])
    
    deficit = cumulative_water_deficit(et, rain, irrigation, time)
    assert deficit > 0
    assert deficit == 8  # (5-1)*2 = 8mm


if __name__ == "__main__":
    pytest.main([__file__, "-v"])