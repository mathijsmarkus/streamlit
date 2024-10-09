import streamlit as st
import folium
from folium import plugins
import pandas as pd
from folium.plugins import HeatMap
import math
from pathlib import Path
import numpy as np
import pydeck as pdk
import ast  # For safely parsing the color string to a list
import geojson  # For working with GeoJSON
# Data provided
#df = pd.read_csv("data/PlotDataHeleWeek.csv")

data = {
    'index': [266, 267],
    'From': ['Sd', 'St'],
    'To': ['St', 'Stz'],
    'Seats': [54746.0, 54746.0],
    'geometry': [
        "LINESTRING (657238.9927340271 5783953.915246224, 657245.7314487227 5783914.055268104, 657260.13064255 5783869.985731723, 657282.8388330762 5783822.840435279, 657423.3518507092 5783556.803324254, 657444.9199685294 5783524.093545601, 657483.3899316911 5783476.336571048, 657848.7350524032 5783070.520843029, 657880.9173542743 5783027.019067468, 657927.5428485536 5782938.337747127, 657962.6885419483 5782844.838326911, 657965.0940151525 5782833.783305251)",
        "LINESTRING (657965.0940151525 5782833.783305251, 657973.9259698781 5782792.8775562, 657985.1072983723 5782699.72784192, 657986.0890796197 5782647.440288878, 657980.2333731261 5782594.934862826, 657971.4298916726 5782549.014530083, 657958.5590881552 5782501.851476166, 657940.2533044477 5782453.402172611, 657921.0508414729 5782411.603392244, 657894.4681320117 5782365.1170173995, 657874.1916226181 5782335.529072614, 657833.3546649527 5782285.249748696, 657508.0215373632 5781925.372268916)"
    ],
    'color': [
        "[1.0, 1.0, 0.0]",  # RGB color: Yellow
        "[1.0, 1.0, 0.0]"   # RGB color: Yellow
    ]
}

# Create DataFrame
df = pd.DataFrame(data)

# Function to convert LINESTRING to GeoJSON
def wkt_to_geojson(wkt):
    # Strip the WKT string to get only the coordinates
    coords_str = wkt.replace("LINESTRING", "").strip().strip("()")
    # Split the coordinates into a list of tuples (lat, lon)
    coords = [tuple(map(float, coord.split())) for coord in coords_str.split(", ")]
    
    # Create GeoJSON format
    geojson_obj = {
        "type": "Feature",
        "geometry": {
            "type": "LineString",
            "coordinates": coords
        },
        "properties": {}
    }
    return geojson_obj

# Function to plot the map
def create_map(df):
    # Initialize the map with no base tiles and a white background
    m = folium.Map(location=[52.379189, 4.899431], zoom_start=10, tiles=None)
    folium.TileLayer(tiles='cartodb positron').add_to(m)

    # Iterate over the rows of the DataFrame to plot each line
    for _, row in df.iterrows():
        # Convert the WKT geometry to GeoJSON
        geojson_obj = wkt_to_geojson(row['geometry'])
        
        # Parse the color (RGB to hex)
        color = ast.literal_eval(row['color'])
        hex_color = "#{:02x}{:02x}{:02x}".format(int(color[0] * 255), int(color[1] * 255), int(color[2] * 255))

        # Plot the line using the GeoJSON object
        folium.GeoJson(
            geojson_obj,
            style_function=lambda x, color=hex_color: {
                'color': color,
                'weight': 2.5,
                'opacity': 1
            }
        ).add_to(m)

    return m

# Create the map with the GeoJSON lines
map_object = create_map(df)

# Display the map in Streamlit
import streamlit as st
st.title("Map with GeoJSON Lines")

# Display the map
st.components.v1.html(map_object._repr_html_(), height=600)