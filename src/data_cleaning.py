import os
import pandas as pd
from datetime import datetime

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

# Define file paths
raw_data_dir = os.path.join(project_root, "data", "raw")
processed_data_dir = os.path.join(project_root, "data", "processed")

# Load datasets
weather = pd.read_csv(os.path.join(raw_data_dir, "weather_daily.csv"), na_values=["NA", ""])
soil = pd.read_csv(os.path.join(raw_data_dir, "soil_sensor_data.csv"), na_values=["NA", ""])
params = pd.read_csv(os.path.join(raw_data_dir, "crop_zone_parameters.csv"), na_values=["NA", ""])

print("DATA INFORMATION")
print("-"*50)
print("\nWeather Data:")
print(weather.info())
print(f"\nShape: {weather.shape}")

print("\nSoil Data:")
print(soil.info())
print(f"\nShape: {soil.shape}")

print("\nParameters Data:")
print(params.info())
print(f"\nShape: {params.shape}")

print("FIRST & LAST ROWS")
print("-"*50)
print(f"\nFirst 3 rows of weather:\n{weather.head(3)}")
print(f"\nLast 3 rows of soil:\n{soil.tail(3)}")

# DATA CLEANING PROCESS
# Drop missing values
initial_rows = len(weather)
weather_clean = weather.dropna()
print(f"Weather: Removed {initial_rows - len(weather_clean)} rows with missing values")

initial_rows = len(soil)
soil_clean = soil.dropna()
print(f"Soil: Removed {initial_rows - len(soil_clean)} rows with missing values\n\n")

# Function to remove outliers
def remove_outliers(df, column_name, min_value, max_value):
    original_count = len(df)
    outliers_mask = (df[column_name] < min_value) | (df[column_name] > max_value)
    num_outliers = outliers_mask.sum()
    cleaned_df = df[~outliers_mask].copy()
    print(f"  {column_name}: Removed {num_outliers} outliers (expected range: [{min_value}, {max_value}])")
    return cleaned_df, num_outliers

# Function to fix pump flow zero readings
def fix_pump_flow_zero(df):
    mask = (df['pump_flow_lpm'] == 0) & (df['pump_power_watts'] > 0)
    num_fixed = mask.sum()
    df.loc[mask, 'pump_flow_lpm'] = pd.NA
    print(f"  pump_flow_lpm: Set {num_fixed} inconsistent zero readings to NaN")
    return df, num_fixed

# Define expected ranges for weather variables
weather_ranges = {
    'temperature_c': (15, 35),
    'humidity_pct': (30, 85),
    'rainfall_mm': (0, 150),
    'wind_speed_mps': (0, 8),
    'solar_index': (.4, .9)
}

# Apply outlier removal
for column, (min_val, max_val) in weather_ranges.items():
    weather_clean, removed = remove_outliers(weather_clean, column, min_val, max_val)

# Fix pump flow inconsistencies
soil_clean, fixed_pump = fix_pump_flow_zero(soil_clean)

# Function to generate description
def generate_description(column_name, dataset_name):
    col_lower = column_name.lower()
    if 'temp' in col_lower:
        return 'Air temperature measured in degrees Celsius.'
    elif 'humid' in col_lower:
        return 'Relative humidity as percentage of saturation.'
    elif 'rainfall' in col_lower:
        return 'Daily rainfall/precipitation amount in millimeters.'
    elif 'wind' in col_lower:
        return 'Wind speed affecting evapotranspiration rates in m/s.'
    elif 'solar' in col_lower or 'radiation' in col_lower:
        return 'Incoming solar radiation for energy balance based on the solar index.'
    elif 'soil_moisture' in col_lower:
        return 'Volumetric soil water content in percentage'
    elif 'tank_level' in col_lower:
        return 'Reservoir or tank water level in litres'
    elif 'pump_flow' in col_lower:
        return 'Pump flow rate in liters per minute'
    elif 'pump_power' in col_lower:
        return 'Pump power consumption in watts'
    elif 'sensor_status' in col_lower:
        return 'Working status of the sensor'
    elif 'crop_type' in col_lower:
        return 'The type of crop being cultivated'
    elif 'area_m2' in col_lower:
        return 'Area of the land in square meters'
    elif 'min_moisture' in col_lower:
        return 'Minimum soil moisture threshold for irrigation in percentage'
    elif 'target_moisture' in col_lower:
        return 'Target soil moisture level for irrigation in percentage'
    elif 'field_capacity' in col_lower:
        return 'Field capacity for water retention in percentage'
    elif 'drainage_coefficient' in col_lower:
        return 'Drainage coefficient representing water loss from the soil'
    elif 'date' in col_lower:
        return 'Date of observation (YYYY-MM-DD)'
    elif 'time' in col_lower:
        return 'Time of measurement'
    elif 'zone' in col_lower:
        return 'Crop zone identifier'
    return f'{column_name} variable from {dataset_name} dataset'

# Function to infer units
def infer_units(column_name, dataset_name):
    col_lower = column_name.lower()
    if 'temp' in col_lower:
        return '°C'
    elif 'humid' in col_lower or 'rh' in col_lower:
        return '%'
    elif 'rainfall' in col_lower or 'precip' in col_lower or 'rain' in col_lower:
        return 'mm'
    elif 'wind' in col_lower or 'windspeed' in col_lower:
        return 'm/s'
    elif 'soil_moisture' in col_lower or 'moisture' in col_lower:
        return '%'
    elif 'tank_level' in col_lower:
        return 'L'
    elif 'pump_flow' in col_lower or 'flow_rate' in col_lower:
        return 'L/min'
    elif 'pump_power' in col_lower or 'power' in col_lower:
        return 'W'
    elif 'area_m2' in col_lower or 'area' in col_lower:
        return 'm²'
    elif 'min_moisture' in col_lower or 'target_moisture' in col_lower or 'field_capacity' in col_lower:
        return '%'
    elif 'date' in col_lower:
        return 'YYYY-MM-DD'
    elif 'time' in col_lower:
        return 'HH:MM:SS'
    return 'various'

# Function to create data dictionary
def create_data_dictionary(df, dataset_name, description_dict=None):
    data_dict_entries = []
    for column in df.columns:
        dtype = str(df[column].dtype)
        unique_count = df[column].nunique()
        sample_value = str(df[column].iloc[0]) if len(df) > 0 else 'NA'
        
        if description_dict and column in description_dict:
            description = description_dict[column]
        else:
            description = generate_description(column, dataset_name)
        
        entry = {
            'Dataset': dataset_name,
            'Variable': column,
            'Data_Type': dtype,
            'Description': description,
            'Units': infer_units(column, dataset_name),
            'Unique_Values': unique_count,
            'Sample_Value': sample_value,
        }
        
        if pd.api.types.is_numeric_dtype(df[column]):
            entry.update({
                'Min': round(df[column].min(), 2),
                'Max': round(df[column].max(), 2),
                'Mean': round(df[column].mean(), 2),
                'Std_Dev': round(df[column].std(), 2),
                'Median': round(df[column].median(), 2)
            })
        else:
            entry.update({
                'Min': 'N/A',
                'Max': 'N/A',
                'Mean': 'N/A',
                'Std_Dev': 'N/A',
                'Median': 'N/A'
            })
        data_dict_entries.append(entry)
    return pd.DataFrame(data_dict_entries)

# Generate data dictionaries
print("\nGenerating data dictionaries...")
weather_dict = create_data_dictionary(weather_clean, 'Weather')
soil_dict = create_data_dictionary(soil_clean, 'Soil')
params_dict = create_data_dictionary(params, 'Parameters')

full_data_dict = pd.concat([weather_dict, soil_dict, params_dict], ignore_index=True)
print(f"Data dictionary created with {len(full_data_dict)} variables across 3 datasets")

print("SAVING TO A SINGLE CSV FILE")

# Add identifier columns
weather_clean['dataset_source'] = 'weather'
weather_clean['record_id'] = range(1, len(weather_clean) + 1)

soil_clean['dataset_source'] = 'soil'
soil_clean['record_id'] = range(1, len(soil_clean) + 1)

params['dataset_source'] = 'parameters'
params['record_id'] = range(1, len(params) + 1)

# Combine datasets
combined_dataset = pd.concat([weather_clean, soil_clean, params], ignore_index=True)

# Save to CSV
csv_output_path = os.path.join(processed_data_dir, "cleaned_irrigation_dataset.csv")
combined_dataset.to_csv(csv_output_path, index=False)

print("SAVING METADATA FILES")
print("-"*60)

# Save data dictionary
dictionary_csv_path = os.path.join(processed_data_dir, "data_dictionary.csv")
full_data_dict.to_csv(dictionary_csv_path, index=False)
print(f"✓ Saved data dictionary to: {dictionary_csv_path}")

# Create and save cleaning summary
cleaning_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

cleaning_summary = pd.DataFrame({
    'Metric': [
        'Cleaning Date',
        'Weather Original Rows',
        'Weather Final Rows',
        'Weather Rows Removed',
        'Soil Original Rows',
        'Soil Final Rows',
        'Soil Rows Removed',
        'Parameters Original Rows',
        'Output CSV File',
        'Total Rows in CSV',
        'Total Columns in CSV'
    ],
    'Value': [
        cleaning_date,
        len(weather),
        len(weather_clean),
        len(weather) - len(weather_clean),
        len(soil),
        len(soil_clean),
        len(soil) - len(soil_clean),
        len(params),
        'cleaned_irrigation_dataset.csv',
        len(combined_dataset),
        len(combined_dataset.columns)
    ]
})

summary_csv_path = os.path.join(processed_data_dir, "cleaning_summary.csv")
cleaning_summary.to_csv(summary_csv_path, index=False)
print(f"✓ Saved cleaning summary to: {summary_csv_path}")