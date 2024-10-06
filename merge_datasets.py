# Import necessary libraries
import pandas as pd

# Load the CSV files
file1 = pd.read_csv("monarch_sightings_2023_cleaned.csv")
file2 = pd.read_csv("monarch_sightings_2024.csv")
file3 = pd.read_csv("monarch_sightings_all_years.csv")

# Merge the datasets
merged_data = pd.concat([file1, file2, file3], ignore_index=True)

# Save the merged dataset
merged_data.to_csv("merged/merged_monarch_sightings.csv", index=False)

# Sort the merged data by 'Date' column (assuming 'Date' is a column in the dataset)# Ensure the 'Date' column is properly parsed as datetime, and invalid parsing results in NaT (Not a Time)
merged_data['Date'] = pd.to_datetime(merged_data['Date'], errors='coerce')

# Now sort the merged data by 'Date'
merged_data_sorted = merged_data.sort_values(by='Date')

# Save the sorted data to a new CSV file
merged_data_sorted.to_csv('merged/merged_monarch_sightings_sorted.csv', index=False)

# Print confirmation
print("Sorted data saved as 'merged_monarch_sightings_sorted.csv'")
