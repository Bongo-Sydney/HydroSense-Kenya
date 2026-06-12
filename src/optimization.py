import numpy as np

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
        irrigation: array of irrigation amounts per day
        S: array of soil moisture over time
    """
    n_days = len(rainfall_forecast)
    irrigation = np.zeros(n_days)
    S = np.zeros(n_days)
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
    
    # Handle last day
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
    pump_energy_kwh = total_water * 0.5 / 10
    
    # Water use efficiency
    water_use_efficiency = (np.sum(ET) - total_water) / (np.sum(rainfall) + total_water + 0.01)
    
    return {
        'total_irrigation_mm': total_water,
        'stress_days': stress_days,
        'severe_stress_days': severe_stress_days,
        'pump_energy_kwh': pump_energy_kwh,
        'water_use_efficiency': water_use_efficiency
    }


def greedy_water_allocation(demands, total_water, priorities=None):
    """
    Greedy allocation of water to zones based on priorities.
    
    Parameters:
        demands: list of water demands per zone
        total_water: total available water
        priorities: list of priority weights (higher = more priority)
    
    Returns:
        allocation: list of allocated water per zone
    """
    n_zones = len(demands)
    if priorities is None:
        priorities = [1] * n_zones
    
    allocation = np.zeros(n_zones)
    remaining_water = total_water
    
    # Sort zones by priority (higher first)
    indices = np.argsort(priorities)[::-1]
    
    for i in indices:
        allocation[i] = min(demands[i], remaining_water)
        remaining_water -= allocation[i]
    
    return allocation


def cost_benefit_analysis(irrigation_amount, water_cost_per_mm=0.5, crop_value_per_ha=50000, area_ha=0.18):
    """
    Calculate cost-benefit of irrigation.
    
    Parameters:
        irrigation_amount: total irrigation in mm
        water_cost_per_mm: cost of water per mm per ha
        crop_value_per_ha: value of crop yield per hectare
        area_ha: area in hectares
    
    Returns:
        dict with cost, benefit, net return
    """
    water_cost = irrigation_amount * water_cost_per_mm * area_ha
    
    # Estimated yield loss per stress day (simplified)
    # Each stress day reduces yield by ~2%
    # This is a placeholder - should be calibrated with actual crop data
    
    benefit = crop_value_per_ha * area_ha
    
    net_return = benefit - water_cost
    
    return {
        'water_cost': water_cost,
        'estimated_benefit': benefit,
        'net_return': net_return,
        'cost_per_mm': water_cost / (irrigation_amount + 0.01)
    }