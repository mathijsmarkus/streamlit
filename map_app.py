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
df = pd.read_csv("data/PlotDataHeleWeek.csv")



# Function to extract first and last coordinate pair from LINESTRING
def extract_first_last_coords(wkt):
    # Strip the WKT string to get only the coordinates part
    coords_str = wkt.replace("LINESTRING", "").strip().strip("()")
    # Split the coordinates into a list of tuples (lat, lon)
    coords = [tuple(map(float, coord.split())) for coord in coords_str.split(", ")]
    # Return first and last coordinate pair
    return coords[0], coords[-1]

# Apply the function to each row
df['first_last_coords'] = df['geometry'].apply(extract_first_last_coords)
