import pandas as pd
import re
from pyproj import Transformer
import folium
import streamlit as st

# Sample data
df = pd.read_csv("data/PlotDataHeleWeek.csv")


# Function to extract coordinates from a geometry string and return a list of tuples
def extract_coords(geometry_str):
    # Regular expression to extract all coordinate pairs
    coords = re.findall(r'(-?\d+\.\d+)\s(-?\d+\.\d+)', geometry_str)
    # Convert to tuple of floats
    return [tuple(map(float, coord)) for coord in coords]

# Apply the function to extract coordinates once
df['coords'] = df['geometry'].apply(extract_coords)

# Precompute hex colors for efficiency
df['color_hex'] = df['color'].apply(lambda rgb: f'#{int(eval(rgb)[0]*255):02x}{int(eval(rgb)[1]*255):02x}{int(eval(rgb)[2]*255):02x}')

# Define the transformer to convert from UTM (EPSG:32631) to WGS84 (EPSG:4326) once
transformer = Transformer.from_crs("epsg:32631", "epsg:4326")

# Function to convert a list of UTM coordinates to lat/lon
def convert_coords_to_latlon(coords):
    x_vals, y_vals = zip(*coords)
    lat_vals, lon_vals = transformer.transform(x_vals, y_vals)
    return list(zip(lat_vals, lon_vals))

# Apply the transformation to all rows at once
df['latlon_coords'] = df['coords'].apply(convert_coords_to_latlon)

# Efficiently plot lines between consecutive coordinates
def draw_map():
    # Initialize the folium map centered on the first lat/lon pair
    m = folium.Map(location=df['latlon_coords'][0][0], zoom_start=12, control_scale=True, tiles='CartoDB positron')

    # Loop over each row to plot the lines
    for i, row in df.iterrows():
        latlon_coords = row['latlon_coords']
        color_hex = row['color_hex']

        # Plot lines between each consecutive pair of lat/lon coordinates
        folium.PolyLine(latlon_coords, color=color_hex, weight=2.5, opacity=1).add_to(m)

    return m._repr_html_()  # Return HTML map

# Main function for Streamlit
def main():
    st.title("Streamlit Map with Clean White-ish Background")

    # Draw the map and display it
    map_html = draw_map()
    st.components.v1.html(map_html, height=600)

# Run the app
if __name__ == "__main__":
    main()
