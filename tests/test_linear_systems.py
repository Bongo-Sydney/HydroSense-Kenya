import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import numpy as np
from src.numerical_methods import gaussian_elimination, lu_decomposition, three_zone_water_allocation


def test_gaussian_elimination_2x2():
    """Test 2x2 system"""
    A = np.array([[2, 1], [1, 3]])
    b = np.array([5, 6])
    
    x = gaussian_elimination(A.copy(), b.copy())
    
    # Expected solution: x = [1.8, 1.4]
    assert np.allclose(A @ x, b, rtol=1e-6)


def test_gaussian_elimination_3x3():
    """Test 3x3 system"""
    A = np.array([[3, 2, 1], [1, 1, 1], [2, 3, 1]])
    b = np.array([10, 6, 11])
    
    x = gaussian_elimination(A.copy(), b.copy())
    
    # Expected solution: x = [1, 2, 3]
    assert np.allclose(A @ x, b, rtol=1e-6)
    assert np.allclose(x, [1, 2, 3], rtol=1e-6)


def test_gaussian_elimination_identity():
    """Test identity matrix"""
    A = np.eye(3)
    b = np.array([5, 10, 15])
    
    x = gaussian_elimination(A.copy(), b.copy())
    
    assert np.allclose(x, b, rtol=1e-6)


def test_lu_decomposition():
    """Test LU decomposition"""
    A = np.array([[4, 3], [6, 3]])
    b = np.array([10, 12])
    
    x, L, U = lu_decomposition(A.copy(), b.copy())
    
    # Verify L*U = A
    assert np.allclose(L @ U, A, rtol=1e-6)
    # Verify solution correct
    assert np.allclose(A @ x, b, rtol=1e-6)


def test_three_zone_allocation():
    """Test three-zone water allocation"""
    demands = [4.5, 3.8, 4.0]
    total_water = 12.0
    
    allocation, method = three_zone_water_allocation(demands, total_water)
    
    # Check total allocation equals total water
    assert np.allclose(np.sum(allocation), total_water, rtol=1e-6)
    # Check all allocations non-negative
    assert np.all(allocation >= -1e-6)
    # Check method returns string
    assert method in ['gaussian', 'lu']


def test_three_zone_allocation_scarcity():
    """Test when total water is less than sum of demands"""
    demands = [4.5, 3.8, 4.0]
    total_water = 8.0
    
    allocation, method = three_zone_water_allocation(demands, total_water)
    
    # Check total equals available water
    assert np.allclose(np.sum(allocation), total_water, rtol=1e-6)
    # Each zone gets its demand or less
    assert allocation[0] <= demands[0]
    assert allocation[1] <= demands[1]
    assert allocation[2] <= demands[2]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])