import numpy as np

# ET and Water Balance functions
def calculate_et(temperature, wind_speed, solar_index, humidity):
    """
    Calculate daily evapotranspiration (ET) using simplified empirical formula.
    
    Formula: ET = max(0, 0.12*T + 0.35*W + 2.4*Solar - 0.025*H)
    
    Parameters:
        temperature (float or array): Air temperature in °C
        wind_speed (float or array): Wind speed in m/s
        solar_index (float or array): Solar radiation index (0-1 scale)
        humidity (float or array): Relative humidity in %
    
    Returns:
        float or array: Evapotranspiration in mm/day
    """
    et = 0.12 * temperature + 0.35 * wind_speed + 2.4 * solar_index - 0.025 * humidity
    return np.maximum(0, et)  # Changed from max(0, et) to np.maximum(0, et)


def water_balance(soil_moisture, rainfall, irrigation, et, drainage_coefficient):
    """
    Calculate next day's soil moisture using water balance equation.
    
    Equation: S(t+1) = S(t) + R(t) + I(t) - ET(t) - D(t)
    where D(t) = drainage_coefficient * S(t) when S(t) exceeds field capacity
    
    Parameters:
        soil_moisture (float): Current soil moisture in %
        rainfall (float): Daily rainfall in mm
        irrigation (float): Daily irrigation applied in mm
        et (float): Daily evapotranspiration in mm
        drainage_coefficient (float): Drainage loss coefficient (0-1)
    
    Returns:
        float: Next day's soil moisture in %
    """
    drainage = drainage_coefficient * soil_moisture
    next_moisture = soil_moisture + rainfall + irrigation - et - drainage
    return np.maximum(0, next_moisture)

# Testing the functions
print("Testing ET function:")
print(f"ET at 25°C, 2m/s wind, 0.7 solar, 60% humidity: {calculate_et(25, 2, 0.7, 60):.2f} mm")

print("\nTesting Water Balance function:")
initial_moisture = 30
next_moisture = water_balance(initial_moisture, rainfall=10, irrigation=0, et=4, drainage_coefficient=0.15)
print(f"Starting at {initial_moisture}%, after rain + ET - drainage: {next_moisture:.2f}%")

# ============================================================================
# ROOT FINDING METHODS
# ============================================================================

def bisection(f, a, b, tol=1e-6, max_iter=100):
    """
    Find root using Bisection method.
    
    Parameters:
        f: function
        a, b: interval endpoints (f(a)*f(b) < 0)
        tol: tolerance
        max_iter: maximum iterations
    
    Returns:
        root, iterations, error
    """
    if f(a) * f(b) >= 0:
        raise ValueError("f(a) and f(b) must have opposite signs")
    
    for i in range(max_iter):
        c = (a + b) / 2
        if f(c) == 0 or (b - a) / 2 < tol:
            return c, i + 1, abs(f(c))
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
    
    c = (a + b) / 2
    return c, max_iter, abs(f(c))


def newton_raphson(f, df, x0, tol=1e-6, max_iter=100):
    """
    Find root using Newton-Raphson method.
    
    Parameters:
        f: function
        df: derivative of f
        x0: initial guess
        tol: tolerance
        max_iter: maximum iterations
    
    Returns:
        root, iterations, error
    """
    x = x0
    for i in range(max_iter):
        fx = f(x)
        dfx = df(x)
        
        if dfx == 0:
            raise ValueError("Derivative is zero")
        
        x_new = x - fx / dfx
        
        if abs(x_new - x) < tol or abs(f(x_new)) < tol:
            return x_new, i + 1, abs(f(x_new))
        
        x = x_new
    
    return x, max_iter, abs(f(x))


def secant(f, x0, x1, tol=1e-6, max_iter=100):
    """
    Find root using Secant method.
    
    Parameters:
        f: function
        x0, x1: initial guesses
        tol: tolerance
        max_iter: maximum iterations
    
    Returns:
        root, iterations, error
    """
    for i in range(max_iter):
        fx0 = f(x0)
        fx1 = f(x1)
        
        if fx1 - fx0 == 0:
            raise ValueError("Division by zero")
        
        x_new = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
        
        if abs(x_new - x1) < tol or abs(f(x_new)) < tol:
            return x_new, i + 2, abs(f(x_new))
        
        x0, x1 = x1, x_new
    
    return x1, max_iter, abs(f(x1))


def irrigation_root_function(soil_moisture, target=35, et=5, rain=0, drainage=0.15):
    """
    Function whose root gives required irrigation amount.
    
    Water balance: S_next = S_current + rain + I - ET - drainage*S_current
    Want: S_next = target
    
    Rearranged: f(I) = S_current + rain + I - ET - drainage*S_current - target = 0
    """
    def f(I):
        return soil_moisture + rain + I - et - drainage * soil_moisture - target
    return f


# ============================================================================
# NUMERICAL DIFFERENTIATION
# ============================================================================

def forward_difference(y, x, i):
    """Forward difference: f'(x_i) ≈ (y_{i+1} - y_i) / h"""
    h = x[i+1] - x[i]
    return (y[i+1] - y[i]) / h


def backward_difference(y, x, i):
    """Backward difference: f'(x_i) ≈ (y_i - y_{i-1}) / h"""
    h = x[i] - x[i-1]
    return (y[i] - y[i-1]) / h


def central_difference(y, x, i):
    """Central difference: f'(x_i) ≈ (y_{i+1} - y_{i-1}) / (2h)"""
    h = x[i+1] - x[i]
    return (y[i+1] - y[i-1]) / (2 * h)


def soil_moisture_rate(soil_moisture, time_days):
    """
    Estimate rate of soil moisture change using all three difference methods.
    
    Returns:
        dict with forward, backward, central rates
    """
    n = len(soil_moisture)
    rates = {'forward': [], 'backward': [], 'central': []}
    
    for i in range(n):
        if i < n - 1:
            rates['forward'].append(forward_difference(soil_moisture, time_days, i))
        if i > 0:
            rates['backward'].append(backward_difference(soil_moisture, time_days, i))
        if 0 < i < n - 1:
            rates['central'].append(central_difference(soil_moisture, time_days, i))
    
    return rates


# ============================================================================
# NUMERICAL INTEGRATION
# ============================================================================

def trapezoidal_rule(y, x):
    """
    Composite Trapezoidal Rule.
    ∫ y dx ≈ (h/2)[y0 + 2(y1+...+y_{n-1}) + yn]
    """
    n = len(y)
    h = (x[-1] - x[0]) / (n - 1)
    integral = (h / 2) * (y[0] + 2 * np.sum(y[1:-1]) + y[-1])
    return integral


def simpsons_13_rule(y, x):
    """
    Composite Simpson's 1/3 Rule.
    n must be even.
    ∫ y dx ≈ (h/3)[y0 + 4∑odd + 2∑even + yn]
    """
    n = len(y)
    if n % 2 == 0:
        raise ValueError("Number of points must be odd (even number of intervals)")
    
    h = (x[-1] - x[0]) / (n - 1)
    integral = (h / 3) * (y[0] + 4 * np.sum(y[1:-1:2]) + 2 * np.sum(y[2:-2:2]) + y[-1])
    return integral


def cumulative_water_deficit(et, rainfall, irrigation, time_days):
    """
    Estimate cumulative water deficit: ∫ (ET - Rain - I) dt
    Positive deficit means crop water stress.
    """
    deficit_rate = np.array(et) - np.array(rainfall) - np.array(irrigation)
    deficit_rate = np.maximum(deficit_rate, 0)  # Only positive deficit matters
    
    return trapezoidal_rule(deficit_rate, time_days)


# ============================================================================
# LINEAR SYSTEMS (Three-Zone Water Allocation)
# ============================================================================

def gaussian_elimination(A, b):
    """
    Solve Ax = b using Gaussian elimination with partial pivoting.
    
    Parameters:
        A: n x n matrix
        b: n x 1 vector
    
    Returns:
        x: solution vector
    """
    A = A.astype(float)
    b = b.astype(float)
    n = len(b)
    
    # Forward elimination with partial pivoting
    for i in range(n):
        # Pivot: find max row
        max_row = i + np.argmax(np.abs(A[i:, i]))
        if max_row != i:
            A[[i, max_row]] = A[[max_row, i]]
            b[[i, max_row]] = b[[max_row, i]]
        
        # Eliminate below
        for j in range(i + 1, n):
            factor = A[j, i] / A[i, i]
            A[j, i:] -= factor * A[i, i:]
            b[j] -= factor * b[i]
    
    # Back substitution
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - np.dot(A[i, i + 1:], x[i + 1:])) / A[i, i]
    
    return x


def lu_decomposition(A, b):
    """
    Solve Ax = b using LU decomposition (Doolittle method).
    
    Returns:
        x: solution vector
        L, U: decomposition matrices
    """
    A = A.astype(float)
    n = len(b)
    L = np.eye(n)
    U = np.zeros((n, n))
    
    # Doolittle decomposition
    for i in range(n):
        # Upper triangular
        for j in range(i, n):
            U[i, j] = A[i, j] - np.sum(L[i, :i] * U[:i, j])
        
        # Lower triangular
        for j in range(i + 1, n):
            L[j, i] = (A[j, i] - np.sum(L[j, :i] * U[:i, i])) / U[i, i]
    
    # Forward substitution: Ly = b
    y = np.zeros(n)
    for i in range(n):
        y[i] = b[i] - np.sum(L[i, :i] * y[:i])
    
    # Back substitution: Ux = y
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - np.sum(U[i, i + 1:] * x[i + 1:])) / U[i, i]
    
    return x, L, U


def three_zone_water_allocation(demands, total_water):
    """
    Solve three-zone water allocation problem.
    
    Zones: Tomato (A), Kale (B), Maize (C)
    Equations based on area and moisture requirements.
    
    Parameters:
        demands: list of water demands per zone [A, B, C] in mm
        total_water: total available water in mm
    
    Returns:
        allocation: solution vector [A, B, C]
        method_used: 'gaussian' or 'lu'
    """
    # Matrix A represents allocation constraints
    # Row1: Zone A demand
    # Row2: Zone B demand  
    # Row3: Total water constraint
    A = np.array([
        [1, 0, 0],   # Zone A allocation
        [0, 1, 0],   # Zone B allocation
        [1, 1, 1]    # Sum of all allocations = total_water
    ])
    
    b = np.array([demands[0], demands[1], total_water])
    
    # Try Gaussian elimination
    try:
        x_gauss = gaussian_elimination(A.copy(), b.copy())
        return x_gauss, 'gaussian'
    except:
        x_lu, L, U = lu_decomposition(A.copy(), b.copy())
        return x_lu, 'lu'