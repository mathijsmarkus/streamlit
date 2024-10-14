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
''

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

