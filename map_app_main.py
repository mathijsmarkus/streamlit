import streamlit as st
import folium
import pandas as pd
import re
from pyproj import Proj, transform
from io import BytesIO

# Define the projection for your coordinates (UTM Zone 31N for the Netherlands)
in_proj = Proj(init='epsg:32631')  # UTM projection for the Netherlands
out_proj = Proj(init='epsg:4326')  # WGS84 (lat/lon)

# Sample data with geometry strings
df = pd.read_csv("data/PlotDataHeleWeek.csv")

# Function to extract first and last coordinates using regex
def extract_first_last_coords(geometry_str):
    # Regular expression to extract all coordinate pairs
    coords = re.findall(r'(-?\d+\.\d+)\s(-?\d+\.\d+)', geometry_str)
    
    # Extract the first and last coordinates
    first_coord = tuple(map(float, coords[0]))
    last_coord = tuple(map(float, coords[-1]))
    
    return first_coord, last_coord

# Apply the function to extract first and last coordinates
df[['first_coord', 'last_coord']] = pd.DataFrame(df['geometry'].apply(extract_first_last_coords).tolist(), index=df.index)

# Drop the original 'geometry' column as it's no longer needed
df = df.drop(columns=['geometry'])

# Function to convert projected coordinates to lat/lon
def convert_to_latlon(x, y):
    lon, lat = transform(in_proj, out_proj, x, y)
    return lat, lon

# Function to draw a line on the map between coordinates and color them
def draw_map():
    # Convert the first set of coordinates to lat/lon for map centering
    first_coord = df['first_coord'][0]
    first_coord_latlon = convert_to_latlon(first_coord[0], first_coord[1])
    
    # Initialize a folium map centered on the first converted coordinate (lat/lon)
    m = folium.Map(location=first_coord_latlon, zoom_start=12, control_scale=True)

    # Add white background using custom tile layer
    folium.TileLayer('cartodb positron').add_to(m)

    # Iterate over the rows and add lines
    for i, row in df.iterrows():
        # Convert first and last coordinates to lat/lon
        first_coord_latlon = convert_to_latlon(row['first_coord'][0], row['first_coord'][1])
        last_coord_latlon = convert_to_latlon(row['last_coord'][0], row['last_coord'][1])

        # Convert the RGB color to a hex string for folium
        color_rgb = eval(row['color'])  # Convert the string '[1.0, 1.0, 0.0]' to a list [1.0, 1.0, 0.0]
        color_hex = f'#{int(color_rgb[0]*255):02x}{int(color_rgb[1]*255):02x}{int(color_rgb[2]*255):02x}'

        # Draw a line between the coordinates (lat/lon) with the specified color
        folium.PolyLine([first_coord_latlon, last_coord_latlon], color=color_hex, weight=2.5, opacity=1).add_to(m)

    # Save the map as an HTML string
    map_html = m._repr_html_()
    
    # Display the map using Streamlit's HTML renderer
    st.write("Map with Lines")
    st.components.v1.html(map_html, height=600)

# Main function for Streamlit
def main():
    st.title("Streamlit Map with Lines between Coordinates")
    
    # Draw the map with lines
    draw_map()

# Run the app
if __name__ == "__main__":
    main()
