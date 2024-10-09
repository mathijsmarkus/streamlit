import streamlit as st
import folium
import pandas as pd
import geopandas as gpd
from shapely import wkt

# Load station data with Pandas
data = pd.read_csv("data/Randstad.csv")
df = data

# Load geospatial data (geometry in WKT format) using Pandas
geodata = pd.read_csv("data/PlotDataHeleWeek.csv")

# Convert 'geometry' column from WKT format to Shapely geometries
geodata['geometry'] = geodata['geometry'].apply(wkt.loads)

def create_map():
    # Start the map at a middle point (Amsterdam)
    m = folium.Map(location=[52.379189, 4.899431], zoom_start=10)
    
    # Plot the stations from the df
    for idx, row in df.iterrows():
        lat, lon = row['Lat-coord'], row['Lng-coord']

        # Determine color based on the Randstad value
        color = "blue" if row['Randstad'] == 0.0 else "red"
        
        # Add a colored dot for each station based on Randstad value
        folium.CircleMarker(
            location=[lat, lon],
            radius=7,  # Size of the dot
            color=color,  # Set color based on Randstad value
            fill=True,
            fill_color=color,  # Fill color
            fill_opacity=0.6  # Transparency of the dot fill
        ).add_to(m)
    
    # Plot lines (connections) from the geodata
    for _, row in geodata.iterrows():
        if row.geometry.geom_type == 'LineString':  # Ensure it is a LineString
            # Convert the LineString into a list of [lat, lon] pairs
            line_coordinates = [[point[1], point[0]] for point in row.geometry.coords]  # Folium expects [lat, lon]
            
            # Add a PolyLine to the map for each connection
            folium.PolyLine(locations=line_coordinates, color='green', weight=2.5).add_to(m)

    return m

# Streamlit interface
st.title("Map with Lines Between Stations")

# Create the map
map_object = create_map()

# Display the map in Streamlit
st.components.v1.html(map_object._repr_html_(), height=600)



