import numpy as np

def water_balance_euler(S0, rainfall, irrigation, ET, drainage_coef, dt=1.0):
    """
    Euler method for soil moisture simulation.
    dS/dt = rain + irrigation - ET - drainage*S
    
    Parameters:
        S0: initial soil moisture (%)
        rainfall: array of daily rainfall (mm)
        irrigation: array of daily irrigation (mm)
        ET: array of daily evapotranspiration (mm)
        drainage_coef: drainage coefficient (0-1)
        dt: time step (days)
    
    Returns:
        S: array of soil moisture over time
    """
    n = len(rainfall)
    S = np.zeros(n)
    S[0] = S0
    
    for t in range(n - 1):
        drainage = drainage_coef * S[t]
        dS = (rainfall[t] + irrigation[t] - ET[t] - drainage) * dt
        S[t + 1] = max(0, S[t] + dS)
    
    return S


def water_balance_runge_kutta(S0, rainfall, irrigation, ET, drainage_coef, dt=1.0):
    """
    4th order Runge-Kutta method for soil moisture simulation.
    More accurate than Euler for continuous dynamics.
    
    dS/dt = f(S,t) = rain + irrigation - ET - drainage*S
    """
    n = len(rainfall)
    S = np.zeros(n)
    S[0] = S0
    
    for t in range(n - 1):
        def f(S_val):
            return rainfall[t] + irrigation[t] - ET[t] - drainage_coef * S_val
        
        k1 = f(S[t])
        k2 = f(S[t] + 0.5 * dt * k1)
        k3 = f(S[t] + 0.5 * dt * k2)
        k4 = f(S[t] + dt * k3)
        
        S[t + 1] = max(0, S[t] + (dt / 6) * (k1 + 2*k2 + 2*k3 + k4))
    
    return S


def monte_carlo_rainfall(historical_rain, n_scenarios=1000, n_days=30):
    """
    Generate rainfall scenarios using bootstrapping.
    
    Parameters:
        historical_rain: array of historical daily rainfall
        n_scenarios: number of Monte Carlo scenarios
        n_days: number of days to simulate
    
    Returns:
        scenarios: n_scenarios x n_days array of rainfall
    """
    scenarios = np.zeros((n_scenarios, n_days))
    
    for i in range(n_scenarios):
        # Sample with replacement from historical data
        scenarios[i, :] = np.random.choice(historical_rain, size=n_days, replace=True)
    
    return scenarios


def simulate_irrigation_needs(S0, rainfall_scenarios, ET, drainage_coef, target=35, min_threshold=25):
    """
    Simulate irrigation needs across multiple rainfall scenarios.
    
    Returns:
        irrigation_needed: daily irrigation amounts
        shortage_days: days where moisture falls below threshold
        over_irrigation: days where irrigation exceeded needs
    """
    n_scenarios, n_days = rainfall_scenarios.shape
    irrigation_needed = np.zeros((n_scenarios, n_days))
    shortage_count = np.zeros(n_scenarios)
    
    for i in range(n_scenarios):
        S = S0
        for t in range(n_days):
            if S < min_threshold:
                deficit = target - S
                irrigation = max(0, deficit)
                irrigation_needed[i, t] = irrigation
            else:
                irrigation = 0
                irrigation_needed[i, t] = 0
            
            # Update soil moisture
            drainage = drainage_coef * S
            S = S + rainfall_scenarios[i, t] + irrigation - ET[t] - drainage
            S = max(0, S)
            
            if S < min_threshold:
                shortage_count[i] += 1
    
    return irrigation_needed, shortage_count


def optimize_irrigation_schedule(S0, rainfall_forecast, ET_forecast, drainage_coef, 
                                  target=35, min_threshold=25, max_irrigation=15):
    """
    Optimize irrigation schedule to minimize water use while avoiding stress.
    
    Parameters:
        S0: initial soil moisture (%)
        rainfall_forecast: array of daily rainfall (mm)
        ET_forecast: array of daily evapotranspiration (mm)
        drainage_coef: drainage coefficient
        target: target soil moisture (%)
        min_threshold: minimum threshold (%)
        max_irrigation: maximum irrigation per day (mm)
    
    Returns:
        irrigation: array of irrigation amounts per day (length n_days)
        S: array of soil moisture over time (length n_days)
    """
    n_days = len(rainfall_forecast)
    irrigation = np.zeros(n_days)
    S = np.zeros(n_days)  # Initialize as array
    S[0] = S0
    
    for t in range(n_days - 1):
        # Check if irrigation needed today
        if S[t] < min_threshold:
            deficit = target - S[t]
            irrigation[t] = min(max_irrigation, max(0, deficit))
        
        # Update soil moisture for next day
        drainage = drainage_coef * S[t]
        S[t + 1] = S[t] + rainfall_forecast[t] + irrigation[t] - ET_forecast[t] - drainage
        S[t + 1] = max(0, S[t + 1])
    
    # Handle last day (no update after)
    if S[n_days - 1] < min_threshold:
        deficit = target - S[n_days - 1]
        irrigation[n_days - 1] = min(max_irrigation, max(0, deficit))
    
    return irrigation, S


def calculate_tradeoffs(irrigation_schedule, soil_moisture, ET, rainfall):
    """
    Calculate trade-off metrics between water conservation and crop stress.
    
    Returns:
        dict with metrics
    """
    total_water = np.sum(irrigation_schedule)
    stress_days = np.sum(soil_moisture < 25)
    severe_stress_days = np.sum(soil_moisture < 20)
    
    # Pump energy estimate (500W pump, 1 hour = 0.5 kWh)
    pump_energy_kwh = total_water * 0.5 / 10  # Rough estimate
    
    # Water use efficiency
    water_use_efficiency = (np.sum(ET) - total_water) / (np.sum(rainfall) + total_water + 0.01)
    
    return {
        'total_irrigation_mm': total_water,
        'stress_days': stress_days,
        'severe_stress_days': severe_stress_days,
        'pump_energy_kwh': pump_energy_kwh,
        'water_use_efficiency': water_use_efficiency
    }