"""
Unit tests for root finding methods (Level 3)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import numpy as np
from src.numerical_methods import bisection, newton_raphson, secant, irrigation_root_function


def f1(x):
    """Test function: x² - 4 = 0, roots at x = ±2"""
    return x**2 - 4


def df1(x):
    return 2*x


def f2(x):
    """Test function: cos(x) - x = 0, root near 0.739"""
    return np.cos(x) - x


def df2(x):
    return -np.sin(x) - 1


def test_bisection_x2_minus_4():
    root, iterations, error = bisection(f1, 0, 3, tol=1e-6)
    assert abs(root - 2.0) < 1e-5
    assert iterations > 0
    assert error < 1e-6


def test_bisection_sign_condition():
    with pytest.raises(ValueError):
        bisection(f1, 0, 1, tol=1e-6)


def test_newton_raphson_x2_minus_4():
    root, iterations, error = newton_raphson(f1, df1, x0=3, tol=1e-6)
    assert abs(root - 2.0) < 1e-6
    assert iterations < 10
    assert error < 1e-6


def test_newton_raphson_cos_x():
    root, iterations, error = newton_raphson(f2, df2, x0=0.5, tol=1e-6)
    assert abs(root - 0.739085) < 1e-5
    assert iterations <= 5  # Quadratic convergence


def test_secant_x2_minus_4():
    root, iterations, error = secant(f1, x0=0, x1=3, tol=1e-6)
    assert abs(root - 2.0) < 1e-5
    assert iterations > 0


def test_irrigation_root_function():
    f = irrigation_root_function(soil_moisture=22, target=35, et=4.5, rain=0, drainage=0.15)
    # At I=0, f(0) = 22 + 0 + 0 - 4.5 - 0.15*22 - 35 = -20.8
    # At I=20, f(20) = 22 + 0 + 20 - 4.5 - 3.3 - 35 = -0.8
    # At I=21, f(21) = 22 + 0 + 21 - 4.5 - 3.3 - 35 = 0.2
    # Root should be ~20.8
    assert f(0) < 0
    assert f(21) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])