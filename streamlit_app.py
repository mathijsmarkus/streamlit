import streamlit as st
import pandas as pd
import math
from pathlib import Path
import numpy as np
import pydeck as pdk

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='NS Train Capacity',
    page_icon=':earth_americas:', # This is an emoji shortcode. Could be a URL too.
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

@st.cache_data
def get_gdp_data():
    """Grab GDP data from a CSV file.

    This uses caching to avoid having to read the file every time. If we were
    reading from an HTTP endpoint instead of a file, it's a good idea to set
    a maximum age to the cache with the TTL argument: @st.cache_data(ttl='1d')
    """

    # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
    DATA_FILENAME = Path(__file__).parent/'data/train_data.csv'
    raw_gdp_df = pd.read_csv(DATA_FILENAME, sep=";")

    MIN_YEAR = 2020
    MAX_YEAR = 2022
    gdp_df = raw_gdp_df.melt(
        ['Maand'],
        'Maand',
        'Aantal_check_ins',
    )

    return raw_gdp_df

@st.cache_data
def get_ranstad_data():
    """Grab GDP data from a CSV file.

    This uses caching to avoid having to read the file every time. If we were
    reading from an HTTP endpoint instead of a file, it's a good idea to set
    a maximum age to the cache with the TTL argument: @st.cache_data(ttl='1d')
    """

    # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
    DATA_FILENAME = Path(__file__).parent/'data/Randstad.csv'
    raw_gdp_df = pd.read_csv(DATA_FILENAME)

    return raw_gdp_df

gdp_df = get_gdp_data()

stations = get_ranstad_data()
# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.

# :earth_americas: GDP dashboard

'''Browse NS data from the [World Bank Open Data](https://data.worldbank.org/) website. As you'll
notice, the data only goes to 2022 right now, and datapoints for certain years are often missing.
But it's otherwise a great (and did I mention _free_?) source of data.
'''

# Add some spacing
''
stations_randstad=stations[stations['Randstad']==1]
stations_outside=stations[stations['Randstad']==0]
st.map(stations_randstad[['Lat-coord', 'Lng-coord']].rename(columns={'Lat-coord': 'lat', 'Lng-coord': 'lon'}))
st.map(stations_outside[['Lat-coord', 'Lng-coord']].rename(columns={'Lat-coord': 'lat', 'Lng-coord': 'lon'}))


''
''
data = {
    'Station': ["Test Station 1", "Test Station 2"],
    'Lat-coord': [52.379189, 51.9225],  # Coordinates for Amsterdam, Rotterdam
    'Lng-coord': [4.899431, 4.47917],
    'Randstad': [0.0, 1.0]  # Use Randstad values 0.0 and 1.0 for testing 
}

stations = pd.DataFrame(data)
MAPBOX_API_KEY = "pk.eyJ1IjoibWF0aGlqc21hcmt1cyIsImEiOiJjbTIxa2V2aTUwcndwMmpyMXNlNTV3eDVvIn0.DfgcGtpDWwXyEB5nsQmeHA"

# Clean data: remove any NaN or infinite values (if any)
stations = stations.replace([float('inf'), float('-inf')], pd.NA).dropna(subset=['Lat-coord', 'Lng-coord'])

# Define color mapping for Randstad
def get_fill_color(randstad):
    if randstad == 0.0:
        return [0, 0, 255]  # Blue for Randstad 0.0
    else:
        return [255, 0, 0]  # Red for Randstad 1.0

# Apply fill color mapping
stations['fill_color'] = stations['Randstad'].apply(get_fill_color)

# Debugging: print to check data
st.write("Data Preview:")
st.write(stations)

# Create pydeck ScatterplotLayer
layer = pdk.Layer(
    'ScatterplotLayer',
    data=stations,
    get_position=['Lng-coord', 'Lat-coord'],  # Pass as list of column names
    get_fill_color='fill_color',  # Use get_fill_color instead of deprecated get_color
    get_radius=5000,  # Larger radius for visibility
    pickable=True,
    filled=True
)

# View State (Center map around the Netherlands)
view_state = pdk.ViewState(
    latitude=52.0,
    longitude=5.0,
    zoom=7,
    pitch=0
)

# Render the map with pydeck
st.pydeck_chart(pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    #map_style='mapbox://styles/mapbox/light-v9'
    map_style='mapbox://styles/mapbox/streets-v11'
))

''
''
'''
years = gdp_df['Jaar'].unique()

if not len(years):
   st.warning("Select at least one country")
selected_year = st.selectbox(
    'Which year would you like to view?',
    years)

df_sum = gdp_df.groupby(['Jaar', 'Maand'])['Aantal_check_ins'].sum().reset_index()
df_sum_sel = df_sum[df_sum['Jaar']==selected_year]

st.header('Check-ins over time', divider='gray')

''

st.line_chart(
    df_sum_sel,
    x='Maand',
    y='Aantal_check_ins',
    #color='Jaar',
)

x = st.slider('x')  # 👈 this is a widget
st.write(x, 'squared is', x * x)

map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [52, 5],
    columns=['lat', 'lon'])

st.map(map_data)

if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
       np.random.randn(20, 3),
       columns=['a', 'b', 'c'])

    chart_data


df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
    })

option = st.selectbox(
    'Which number do you like best?',
     df['first column'])

'You selected: ', option

left_column, right_column = st.columns(2)
# You can use a column just like st.sidebar:
left_column.button('Press me!')

# Or even better, call Streamlit functions inside a "with" block:
with right_column:
    chosen = st.radio(
        'Sorting hat',
        ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
    st.write(f"You are in {chosen} house!")

'''