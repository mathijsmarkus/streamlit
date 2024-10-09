import streamlit as st
import folium
from folium import plugins
import pandas as pd
from folium.plugins import HeatMap
import math
from pathlib import Path
import numpy as np
import pydeck as pdk

# Data provided
data = pd.read_csv("data/Randstad.csv")
df = data

def create_map():
    # Start the map at a middle point (Amsterdam)
    m = folium.Map(location=[52.379189, 4.899431], zoom_start=10)
    
    # Loop through the dataframe to plot the stations
    for idx, row in df.iterrows():
        lat, lon = row['Lat-coord'], row['Lng-coord']
        
        # Determine color based on the Randstad value
        if row['Randstad'] == 0.0:
            color = "blue"
        else:
            color = "red"
        
        # Add a colored dot for each station based on Randstad value
        folium.CircleMarker(
            location=[lat, lon],
            radius=7,  # Size of the dot
            color=color,  # Set color based on Randstad value
            fill=True,
            fill_color=color,  # Fill color
            fill_opacity=0.6  # Transparency of the dot fill
        ).add_to(m)
    
    return m

# Streamlit interface
st.title("Map with Lines Between Stations")

# Create the map
map_object = create_map()

# Display the map in Streamlit
st.components.v1.html(map_object._repr_html_(), height=600)