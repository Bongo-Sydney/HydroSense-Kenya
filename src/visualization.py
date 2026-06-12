import numpy as np
import matplotlib.pyplot as plt


def plot_weather_patterns(weather_data, save_path=None):
    """
    Create 4-panel weather visualization.
    
    Parameters:
        weather_data: DataFrame with date, temperature_c, rainfall_mm, humidity_pct, solar_index
        save_path: optional path to save figure
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Temperature
    axes[0, 0].plot(weather_data['date'], weather_data['temperature_c'], 'o-', 
                    color='red', linewidth=1.5, markersize=4)
    axes[0, 0].set_xlabel('Date')
    axes[0, 0].set_ylabel('Temperature (°C)')
    axes[0, 0].set_title('Daily Temperature Variation')
    axes[0, 0].grid(True, alpha=0.3)
    
    # Rainfall
    axes[0, 1].bar(weather_data['date'], weather_data['rainfall_mm'], 
                   color='skyblue', alpha=0.7)
    axes[0, 1].set_xlabel('Date')
    axes[0, 1].set_ylabel('Rainfall (mm)')
    axes[0, 1].set_title('Daily Rainfall Distribution')
    axes[0, 1].grid(True, alpha=0.3, axis='y')
    
    # Humidity
    axes[1, 0].plot(weather_data['date'], weather_data['humidity_pct'], 's-',
                    color='green', linewidth=1.5, markersize=4)
    axes[1, 0].set_xlabel('Date')
    axes[1, 0].set_ylabel('Humidity (%)')
    axes[1, 0].set_title('Humidity Trend')
    axes[1, 0].grid(True, alpha=0.3)
    
    # Solar index
    axes[1, 1].plot(weather_data['date'], weather_data['solar_index'], 'd-',
                    color='orange', linewidth=1.5, markersize=4)
    axes[1, 1].set_xlabel('Date')
    axes[1, 1].set_ylabel('Solar Index')
    axes[1, 1].set_title('Solar Radiation Index')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.suptitle('Weather Patterns', fontsize=14)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    
    return fig


def plot_soil_moisture_zones(soil_data, zones, min_threshold, target, save_path=None):
    """
    Plot soil moisture across multiple zones.
    
    Parameters:
        soil_data: DataFrame with timestamp, zone_id, soil_moisture_pct
        zones: dict of zone names to colors
        min_threshold: minimum moisture line
        target: target moisture line
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    for zone, color in zones.items():
        zone_data = soil_data[soil_data['zone_id'] == zone]
        ax.plot(zone_data['day'], zone_data['soil_moisture_pct'], 'o-',
                color=color, linewidth=2, markersize=6, label=zone)
    
    ax.axhline(y=target, color='green', linestyle='--', linewidth=1.5, label=f'Target ({target}%)')
    ax.axhline(y=min_threshold, color='red', linestyle='--', linewidth=1.5, label=f'Minimum ({min_threshold}%)')
    
    ax.set_xlabel('Day')
    ax.set_ylabel('Soil Moisture (%)')
    ax.set_title('Soil Moisture Evolution - Three Farm Zones')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    
    return fig


def plot_et_vs_rainfall(weather_data, save_path=None):
    """
    Plot evapotranspiration vs rainfall comparison.
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # ET bar chart
    axes[0].bar(weather_data['date'], weather_data['ET'], color='teal', alpha=0.7)
    axes[0].set_xlabel('Date')
    axes[0].set_ylabel('Evapotranspiration (mm/day)')
    axes[0].set_title('Daily Evapotranspiration')
    axes[0].grid(True, alpha=0.3, axis='y')
    
    # ET vs rainfall line plot
    axes[1].plot(weather_data['date'], weather_data['ET'], 'o-', 
                 label='ET', color='red', linewidth=2)
    axes[1].plot(weather_data['date'], weather_data['rainfall_mm'], 's-',
                 label='Rainfall', color='blue', linewidth=2)
    axes[1].set_xlabel('Date')
    axes[1].set_ylabel('Amount (mm)')
    axes[1].set_title('ET vs Rainfall Comparison')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.suptitle('Evapotranspiration Analysis', fontsize=14)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    
    return fig


def plot_simulation_comparison(dates, S_euler, S_rk4, min_threshold, target, save_path=None):
    """
    Plot Euler vs Runge-Kutta simulation comparison.
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.plot(dates, S_euler, 'o-', label='Euler Method', linewidth=2, markersize=4)
    ax.plot(dates, S_rk4, 's-', label='Runge-Kutta (4th order)', linewidth=2, markersize=4)
    ax.axhline(y=min_threshold, color='red', linestyle='--', linewidth=1.5, label=f'Minimum ({min_threshold}%)')
    ax.axhline(y=target, color='green', linestyle='--', linewidth=1.5, label=f'Target ({target}%)')
    
    ax.set_xlabel('Date')
    ax.set_ylabel('Soil Moisture (%)')
    ax.set_title('Soil Moisture Simulation - Euler vs Runge-Kutta')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    
    return fig


def plot_optimized_irrigation(dates, S_optimized, S_no_irrigation, irrigation_optimized, 
                               min_threshold, target, save_path=None):
    """
    Plot optimized irrigation schedule results.
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.plot(dates, S_optimized, 'g-', linewidth=2, label='With Optimized Irrigation')
    ax.plot(dates, S_no_irrigation, 'r--', linewidth=2, label='No Irrigation')
    ax.axhline(y=min_threshold, color='orange', linestyle=':', linewidth=2, label=f'Minimum ({min_threshold}%)')
    ax.axhline(y=target, color='blue', linestyle=':', linewidth=2, label=f'Target ({target}%)')
    
    irrigation_days = np.where(irrigation_optimized > 0)[0]
    for day in irrigation_days:
        ax.axvline(x=dates[day], color='green', alpha=0.3, linewidth=1)
    
    ax.set_xlabel('Date')
    ax.set_ylabel('Soil Moisture (%)')
    ax.set_title('Soil Moisture with Optimized Irrigation Schedule')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    
    return fig


def plot_trade_offs(tradeoff_results, save_path=None):
    """
    Plot trade-off analysis results.
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    strategies = list(tradeoff_results.keys())
    water_use = [tradeoff_results[s]['total_irrigation_mm'] for s in strategies]
    stress_days = [tradeoff_results[s]['stress_days'] for s in strategies]
    efficiency = [tradeoff_results[s]['water_use_efficiency'] * 100 for s in strategies]
    
    # Water vs Stress scatter
    axes[0].scatter(water_use, stress_days, s=100, c=range(len(strategies)), cmap='viridis')
    for i, name in enumerate(strategies):
        axes[0].annotate(name, (water_use[i], stress_days[i]), fontsize=9, ha='center')
    axes[0].set_xlabel('Total Irrigation Water (mm)')
    axes[0].set_ylabel('Crop Stress Days')
    axes[0].set_title('Water-Stress Trade-off Curve')
    axes[0].grid(True, alpha=0.3)
    
    # Efficiency bar chart
    colors = ['red', 'green', 'orange', 'blue', 'purple']
    axes[1].bar(strategies, efficiency, color=colors, alpha=0.7)
    axes[1].set_xlabel('Irrigation Strategy')
    axes[1].set_ylabel('Water Use Efficiency (%)')
    axes[1].set_title('Water Use Efficiency by Strategy')
    axes[1].tick_params(axis='x', rotation=15)
    axes[1].grid(True, alpha=0.3, axis='y')
    
    plt.suptitle('Trade-off Analysis: Water vs Stress vs Efficiency', fontsize=14)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    
    return fig