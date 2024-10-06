import pandas as pd
import streamlit as st
import folium
from folium.plugins import HeatMap
import plotly.express as px
from scipy.stats import pearsonr
from streamlit_folium import st_folium
import requests

# Set up Streamlit layout
st.set_page_config(layout="wide")

# Load the data
@st.cache_data
def load_data():
    sightings_data = pd.read_csv('monarch_sightings_all_years.csv')
    pesticide_data = pd.read_csv('USDA_PDP_AnalyticalResults.csv', dtype={'Column9': str, 'Column13': str})
    
    sightings_data['Date'] = pd.to_datetime(sightings_data['Date'], errors='coerce')
    sightings_data['Year'] = sightings_data['Date'].dt.year
    
    return sightings_data, pesticide_data

# Load all data
sightings_data, pesticide_data = load_data()

# Sidebar: State selection and analysis options
st.sidebar.title("Monarch Butterfly Analysis Dashboard")
selected_state = st.sidebar.selectbox('Select State', sightings_data['State/Province'].unique())
analysis_option = st.sidebar.radio("Choose Analysis", ["Population Fluctuations", "Pesticide Analysis", "Texas Migration Comparison"])

# Main content
st.title(f'Monarch Butterfly Analysis for {selected_state}')

if analysis_option == "Population Fluctuations":
    st.header("Monarch Butterfly Population Fluctuations")
    
    # Time series of monarch sightings
    yearly_sightings = sightings_data[sightings_data['State/Province'] == selected_state].groupby('Year')['Number'].sum().reset_index()
    fig_sightings = px.line(yearly_sightings, x='Year', y='Number', title=f'Monarch Sightings in {selected_state} Over Time')
    st.plotly_chart(fig_sightings, use_container_width=True)
    
    # Map of sightings
    st.subheader(f'Map of Monarch Butterfly Sightings in {selected_state}')
    m = folium.Map(location=[sightings_data[sightings_data['State/Province'] == selected_state]['Latitude'].mean(), 
                             sightings_data[sightings_data['State/Province'] == selected_state]['Longitude'].mean()], 
                   zoom_start=6)
    
    heat_data = [[row['Latitude'], row['Longitude'], row['Number']] for _, row in sightings_data[sightings_data['State/Province'] == selected_state].iterrows()]
    HeatMap(heat_data).add_to(m)
    
    st_folium(m, width=700, height=450)

elif analysis_option == "Pesticide Analysis":
    st.header("Pesticide Usage Analysis")
    
    # Display sample of pesticide data
    st.subheader("Sample of Pesticide Data")
    st.write(pesticide_data.head())
    
    st.write("""
    To perform a detailed pesticide analysis:
    1. We need to process the USDA PDP Analytical Results data to extract state-level pesticide information.
    2. Identify the pesticides with the highest concentrations in each state.
    3. Create a color map showing pesticide concentrations by state.
    4. Investigate potential correlations between pesticide use and monarch butterfly populations.
    """)

else:  # Texas Migration Comparison
    st.header("Texas Migration Comparison")
    
    # Compare Texas with other states
    texas_data = sightings_data[sightings_data['State/Province'] == 'TX'].groupby('Year')['Number'].sum().reset_index()
    other_states = sightings_data[sightings_data['State/Province'] != 'TX'].groupby(['State/Province', 'Year'])['Number'].sum().reset_index()
    
    fig_comparison = px.line(other_states, x='Year', y='Number', color='State/Province', title='Monarch Sightings: Texas vs Other States')
    fig_comparison.add_trace(px.line(texas_data, x='Year', y='Number', title='Texas').data[0])
    
    st.plotly_chart(fig_comparison, use_container_width=True)