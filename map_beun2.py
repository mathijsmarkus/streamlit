import pandas as pd
import re
from pyproj import Transformer
import folium
import streamlit as st

# Load the CSV data for multiple line sets
@st.cache_data
def load_data():
    # Load multiple datasets
    df_hele_week = pd.read_csv("data/PlotDataHeleWeek.csv")
    df_monday = pd.read_csv("data/PlotDataMonday.csv")
    df_tuesday = pd.read_csv("data/PlotDataTuesday.csv")  
    df_wednesday = pd.read_csv("data/PlotDataWednesday.csv")
    df_thursday = pd.read_csv("data/PlotDataThursday.csv")
    df_friday = pd.read_csv("data/PlotDataFriday.csv")
    df_saturday = pd.read_csv("data/PlotDataSaturday.csv")
    df_sunday = pd.read_csv("data/PlotDataSunday.csv")
    stations = pd.read_csv("data/Randstad-0.csv")
    return df_hele_week, df_monday, df_tuesday, df_wednesday, df_thursday, df_friday, df_saturday, df_sunday, stations

# Extract coordinates function with error handling for missing data
def extract_coords(geometry_str):
    coords = re.findall(r'(-?\d+\.\d+)\s(-?\d+\.\d+)', geometry_str)
    if not coords:  # If no coordinates are found, return an empty list
        return []
    return [tuple(map(float, coord)) for coord in coords]

# Precompute data processing for lines
@st.cache_data
def process_line_data(df):
    df['coords'] = df['geometry'].apply(extract_coords)
    
    # Check if 'color' column exists, if not use a default color
    if 'color' in df.columns:
        df['color_hex'] = df['color'].apply(lambda rgb: f'#{int(eval(rgb)[0]*255):02x}{int(eval(rgb)[1]*255):02x}{int(eval(rgb)[2]*255):02x}')
    else:
        df['color_hex'] = '#3388ff'  # Default to a blue color

    transformer = Transformer.from_crs("epsg:32631", "epsg:4326")
    
    def convert_coords_to_latlon(coords):
        if not coords:  # If there are no coordinates, return an empty list
            return []
        x_vals, y_vals = zip(*coords)  # Safely unpack the values
        lat_vals, lon_vals = transformer.transform(x_vals, y_vals)
        return list(zip(lat_vals, lon_vals))
    
    df['latlon_coords'] = df['coords'].apply(convert_coords_to_latlon)
    return df

# Efficiently plot lines and stations
@st.cache_data
def draw_map(initial_center, initial_zoom):
    # Use initial center and zoom level to keep map state
    m = folium.Map(location=initial_center, zoom_start=initial_zoom, control_scale=True, tiles='CartoDB positron')
    return m

# Add lines to the map
def add_lines_to_map(m, df):
    for _, row in df.iterrows():
        latlon_coords = row['latlon_coords']
        if not latlon_coords:  # Skip if no lat/lon coordinates
            continue
        color_hex = row['color_hex']
        folium.PolyLine(latlon_coords, color=color_hex, weight=2.5, opacity=1).add_to(m)
    return m

# Main function for Streamlit
def main():
    st.title("Intensity of Rail Use")
    st.write("The map below shows the intensity of each piece of rail in The Netherlands. The map is adjustable. \
              Different station types can be selected, as well as different transport operators.")

    # Load and process data
    df_hele_week, df_monday, df_tuesday, df_wednesday, df_thursday, df_friday, df_saturday, df_sunday, stations = load_data()

    # Add a dropdown to select the day
    day_choice = st.sidebar.selectbox(
        "Select the day:",
        options=['Hele Week', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        index=0  # Default to 'Hele Week'
    )

    # Process the selected day's data
    if day_choice == 'Hele Week':
        df_selected_day = df_hele_week
    elif day_choice == 'Monday':
        df_selected_day = df_monday
    elif day_choice == 'Tuesday':
        df_selected_day = df_tuesday
    elif day_choice == 'Wednesday':
        df_selected_day = df_wednesday
    elif day_choice == 'Thursday':
        df_selected_day = df_thursday
    elif day_choice == 'Friday':
        df_selected_day = df_friday
    elif day_choice == 'Saturday':
        df_selected_day = df_saturday
    elif day_choice == 'Sunday':
        df_selected_day = df_sunday

    df_selected_day = process_line_data(df_selected_day)

    # Safely get the initial center (handle empty or invalid coordinate lists)
    if not df_selected_day['latlon_coords'].empty and df_selected_day['latlon_coords'].iloc[0]:
        initial_center = df_selected_day['latlon_coords'].iloc[0][0]  # First valid coordinate
    else:
        # Fallback center if no valid coordinates are found
        initial_center = [52.3676, 4.9041]  # Default to the center of Amsterdam

    initial_zoom = 7

    # Draw the initial map
    folium_map = draw_map(initial_center, initial_zoom)

    # Add the selected day's data to the map
    folium_map = add_lines_to_map(folium_map, df_selected_day)

    # Display the map in Streamlit
    st.components.v1.html(folium_map._repr_html_(), height=600)

# Run the app
if __name__ == "__main__":
    main()
