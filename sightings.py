import pandas as pd
import requests
import folium
import geopandas as gpd
from geopy.geocoders import Nominatim

# Load monarch sightings data
data = pd.read_csv(r'C:\Users\anude\Downloads\Datathon 2024\monarch_sightings.csv')

# Load US counties shapefile
counties = gpd.read_file(r'C:\Users\anude\Downloads\Datathon 2024\AgChange\shapefiles\US_counties_2012_geoid.shp')

# Function to get county from latitude and longitude
def get_county(lat, lon):
    try:
        response = requests.get(f"https://geo.fcc.gov/api/census/area?lat={lat}&lon={lon}&format=json")
        county = response.json()['results'][0]['county_name']
        return county
    except Exception as e:
        print(f"Error fetching county for coordinates ({lat}, {lon}): {e}")
    return None

# Add county information to the dataset
data['County'] = data.apply(lambda row: get_county(row['Latitude'], row['Longitude']), axis=1)

# Aggregate sightings by county
county_sightings = data['County'].value_counts().reset_index()
county_sightings.columns = ['County', 'Sightings']

# Merge sightings data with counties shapefile
counties = counties.rename(columns={'NAME': 'County'})  # Assuming 'NAME' column has county names
county_sightings_geo = counties.merge(county_sightings, on='County', how='left').fillna(0)

# Create a map
m = folium.Map(location=[37.8, -96.9], zoom_start=4)

# Add county sightings to the map
folium.Choropleth(
    geo_data=county_sightings_geo,
    data=county_sightings_geo,
    columns=['County', 'Sightings'],
    key_on='feature.properties.County',
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Monarch Butterfly Sightings'
).add_to(m)

# Save the map to an HTML file
m.save('monarch_sightings_map.html')