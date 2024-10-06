# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from statsmodels.tsa.stattools import grangercausalitytests

# Load the dataset
data = pd.read_csv('/content/final_merged_try.csv')

# Step 1: Data Preprocessing
data.dropna(inplace=True)  # Drop rows with missing values if not done already

# Ensure 'year' is treated as an integer and convert to datetime if necessary
data['year'] = data['year'].astype(int)  # Convert year to integer

# Create AQI and Temperature Ranges for ANOVA
# Define AQI ranges (you can adjust these ranges based on your data)
bins_aqi = [0, 50, 100, 150, 200, 300]
labels_aqi = ['Good', 'Moderate', 'Unhealthy for Sensitive Groups', 'Unhealthy', 'Very Unhealthy']
data['AQI_Category'] = pd.cut(data['aqi_mean'], bins=bins_aqi, labels=labels_aqi)

# Define Temperature ranges (you can adjust these ranges based on your data)
bins_temp = [0, 10, 20, 30, 40]
labels_temp = ['Very Cold', 'Cold', 'Warm', 'Hot']
data['Temp_Category'] = pd.cut(data['temp_mean'], bins=bins_temp, labels=labels_temp)

# Step 2: ANOVA Test for AQI Categories
anova_results_aqi = stats.f_oneway(
    data[data['AQI_Category'] == 'Good']['monarch_count'],
    data[data['AQI_Category'] == 'Moderate']['monarch_count'],
    data[data['AQI_Category'] == 'Unhealthy for Sensitive Groups']['monarch_count'],
    data[data['AQI_Category'] == 'Unhealthy']['monarch_count'],
    data[data['AQI_Category'] == 'Very Unhealthy']['monarch_count']
)

print("ANOVA Results for AQI Categories:")
print(f"F-statistic: {anova_results_aqi.statistic:.2f}, p-value: {anova_results_aqi.pvalue:.4f}")

# Step 3: ANOVA Test for Temperature Categories
anova_results_temp = stats.f_oneway(
    data[data['Temp_Category'] == 'Very Cold']['monarch_count'],
    data[data['Temp_Category'] == 'Cold']['monarch_count'],
    data[data['Temp_Category'] == 'Warm']['monarch_count'],
    data[data['Temp_Category'] == 'Hot']['monarch_count']
)

print("ANOVA Results for Temperature Categories:")
print(f"F-statistic: {anova_results_temp.statistic:.2f}, p-value: {anova_results_temp.pvalue:.4f}")

# Step 4: Granger Causality Test
# Prepare the data for Granger causality testing
granger_data = data[['monarch_count', 'aqi_mean', 'temp_mean']]
granger_data.dropna(inplace=True)  # Drop rows with missing values

# Conduct Granger causality test (testing if AQI affects butterfly sightings)
max_lag = 5  # You can adjust this based on your analysis needs
granger_test_aqi = grangercausalitytests(granger_data[['monarch_count', 'aqi_mean']], max_lag, verbose=True)

# Conduct Granger causality test (testing if Temperature affects butterfly sightings)
granger_test_temp = grangercausalitytests(granger_data[['monarch_count', 'temp_mean']], max_lag, verbose=True)

