import pandas as pd
import streamlit as st
import folium
from folium.plugins import HeatMap
import plotly.express as px
from scipy.stats import pearsonr
from streamlit_folium import st_folium
import os

# Set up Streamlit layout
st.set_page_config(layout="wide")

# Load the data
@st.cache_data
def load_data():
    sightings_data = pd.read_csv('monarch_sightings_all_years.csv')
    ozone_temp_data = pd.read_csv('texas_ozone_temperature_data_2020_to_2024.csv')
    pesticide_data = pd.read_csv('USDA_PDP_AnalyticalResults.csv', dtype={'Column9': str, 'Column13': str})

    sightings_data['Date'] = pd.to_datetime(sightings_data['Date'], errors='coerce')
    ozone_temp_data['date_local'] = pd.to_datetime(ozone_temp_data['date_local'], errors='coerce')
    
    sightings_data['Year'] = sightings_data['Date'].dt.year
    ozone_temp_data['Year'] = ozone_temp_data['date_local'].dt.year
    
    return sightings_data, ozone_temp_data, pesticide_data

# Load all data
sightings_data, ozone_temp_data, pesticide_data = load_data()

# Function to create the folium map
def create_folium_map(state='TX'):
    m = folium.Map(location=[31.9686, -99.9018], zoom_start=6)
    state_data = sightings_data[sightings_data['State/Province'] == state]
    
    # Add heatmap layer
    heat_data = [[row['Latitude'], row['Longitude']] for _, row in state_data.iterrows()]
    HeatMap(heat_data).add_to(m)
    
    return m

# Sidebar: State selection
st.sidebar.title("Monarch Butterfly Dashboard")
selected_state = st.sidebar.selectbox(
    'Select State', sightings_data['State/Province'].unique(), index=list(sightings_data['State/Province'].unique()).index('TX')
)

# Main content: Title
st.title(f'Monarch Butterfly Sightings and Environmental Data for {selected_state}')

# Create the folium map and display it in Streamlit
st.subheader(f'Map of Monarch Butterfly Sightings in {selected_state}')
folium_map = create_folium_map(selected_state)
st_folium(folium_map, width=700, height=450)

# Monarch Sightings Over Time
st.subheader(f'Monarch Butterfly Sightings Over Time in {selected_state}')
filtered_sightings = sightings_data[sightings_data['State/Province'] == selected_state]
yearly_sightings = filtered_sightings.groupby('Year')['Number'].sum().reset_index()

fig_sightings = px.line(yearly_sightings, x='Year', y='Number', title=f'Monarch Sightings in {selected_state}')
st.plotly_chart(fig_sightings, use_container_width=True)

# Temperature and Ozone Data Over Time
st.subheader(f'Temperature and Ozone Levels Over Time in {selected_state}')
filtered_ozone_temp = ozone_temp_data[ozone_temp_data['state_ozone'] == selected_state]

fig_temp_ozone = px.line(filtered_ozone_temp, x='date_local', y=['arithmetic_mean_temperature', 'arithmetic_mean_ozone'],
                         labels={'value': 'Mean Value', 'date_local': 'Date'},
                         title=f'Temperature and Ozone Levels in {selected_state}')
st.plotly_chart(fig_temp_ozone, use_container_width=True)

# Correlation Analysis
st.subheader(f'Correlation Analysis Between Monarch Sightings and Environmental Factors in {selected_state}')
common_years = set(filtered_sightings['Year']).intersection(set(filtered_ozone_temp['Year']))
if len(common_years) > 0:
    # Merge data by Year for correlation analysis
    merged_data = pd.merge(
        filtered_sightings.groupby('Year')['Number'].sum().reset_index(),
        filtered_ozone_temp.groupby('Year')[['arithmetic_mean_temperature', 'arithmetic_mean_ozone']].mean().reset_index(),
        on='Year'
    )

    # Calculate correlations
    corr_temp, _ = pearsonr(merged_data['Number'], merged_data['arithmetic_mean_temperature'])
    corr_ozone, _ = pearsonr(merged_data['Number'], merged_data['arithmetic_mean_ozone'])

    st.write(f"**Correlation between Monarch Sightings and Temperature**: {corr_temp:.2f}")
    st.write(f"**Correlation between Monarch Sightings and Ozone Levels**: {corr_ozone:.2f}")
else:
    st.write("No common years of data available for correlation analysis.")

# Show Pesticide Data (Example table)
st.subheader('Pesticide Data (Sample)')
st.write(pesticide_data.head())

# Debugging: Check available years in both datasets
st.write(f"Available years in Monarch sightings data for {selected_state}: {filtered_sightings['Year'].unique()}")
st.write(f"Available years in Ozone/Temperature data for {selected_state}: {filtered_ozone_temp['Year'].unique()}")
