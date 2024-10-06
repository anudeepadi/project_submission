
# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import seaborn as sns

# Load the dataset
data = pd.read_csv('final_merged_try.csv')

# Step 1: Data Preprocessing
# Check for missing values
print("Missing values in each column:")
print(data.isnull().sum())

# Drop rows with missing values (or handle them as needed)
data.dropna(inplace=True)

# Ensure 'year' is treated as an integer and convert to datetime
data['year'] = data['year'].astype(int)  # Convert year to integer
data['date'] = pd.to_datetime(data['year'].astype(str) + '-01-01')  # Assuming January 1st for simplicity

# Check for duplicates in the date column
duplicate_dates = data[data.duplicated(['date'], keep=False)]
if not duplicate_dates.empty:
    print("Duplicate dates found:")
    print(duplicate_dates)

# Option 1: Remove duplicates (keeping the first occurrence)
data = data.drop_duplicates(subset=['date'], keep='first')

# Option 2: Aggregate duplicates (e.g., take the mean of other columns)
# data = data.groupby('date').mean().reset_index()  # Uncomment this line if you prefer aggregation

# Set date as index for time series analysis
data.set_index('date', inplace=True)

# Step 2: Time Series Decomposition
# Decompose butterfly sightings time series
decomposition = sm.tsa.seasonal_decompose(data['monarch_count'], model='additive')
decomposition.plot()
plt.title('Decomposition of Butterfly Sightings')
plt.show()

# Decompose AQI and Temperature
decomposition_aqi = sm.tsa.seasonal_decompose(data['aqi_mean'], model='additive')
decomposition_aqi.plot()
plt.title('Decomposition of AQI Mean')
plt.show()

decomposition_temp = sm.tsa.seasonal_decompose(data['temp_mean'], model='additive')
decomposition_temp.plot()
plt.title('Decomposition of Temperature Mean')
plt.show()

# Step 3: Lag Correlation Analysis
# Calculate lagged correlations for butterfly sightings with AQI and temperature
lags = range(1, 13)  # Lag from 1 to 12 months
correlations = {}

for lag in lags:
    correlation_aqi = data['monarch_count'].corr(data['aqi_mean'].shift(lag))
    correlation_temp = data['monarch_count'].corr(data['temp_mean'].shift(lag))
    correlations[lag] = {'AQI': correlation_aqi, 'Temperature': correlation_temp}

# Convert to DataFrame for easier plotting
correlation_df = pd.DataFrame(correlations).T

# Plot lag correlations
plt.figure(figsize=(12, 6))
sns.lineplot(data=correlation_df)
plt.title('Lag Correlation between Butterfly Sightings and Environmental Factors')
plt.xlabel('Lag (Months)')
plt.ylabel('Correlation Coefficient')
plt.axhline(0, color='gray', linestyle='--')
plt.legend(['AQI', 'Temperature'])
plt.show()

