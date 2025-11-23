"""
Name: Beashagnya Chalasani
CS230:8
Data: New york housing market
URL: https://www.kaggle.com/datasets/nelgiriyewithana/new-york-housing-market/data
Description:
This website is gives the user an idea of prices of real estate property wheter its a house or co-op or a townhome.
The user will be able to select the area that they are looking to invest in by county and anf by the specift property.
The website will then generate a bar graph that shows the average price in the specifisc boroigh that the user selects
and will aslo genetrate a pie chart that shows distributions of properties in that specific borough.

Refrences:
https://streamlit.io/components?category=maps
https://docs.streamlit.io/develop/api-reference/media/st.image
https://stackoverflow.com/questions/62593913/plotting-a-pie-chart-out-of-a-dictionary
https://discuss.streamlit.io/t/tooltip-and-labels-in-pydeck-chart/1727
https://matplotlib.org/stable/api/ticker_api.html
https://pandas.pydata.org/docs/reference/api/pandas.Series.html
"""

import streamlit as st
import pandas as pd
import pydeck as pdk

df = pd.read_csv("NY_House_Dataset.csv")


# [FUNC2P] Function with 2+ parameters, one with default
def filter_listings(df, borough, max_price=5000):
    """
    Filter the dataframe by borough and a maximum price.
    """
    filtered = df[
        (df["LOCALITY"] == borough) &
        (df["PRICE"] <= max_price)
    ]
    return filtered

#Types of borough
def get_unique_borough(df):
    '''
    return the unique boroughs.
    '''
    type_of_borough = df["LOCALITY"].unique()
    return type_of_borough


# ================================
# STREAMLIT USER INTERFACE
# ================================
st.image("NYC_sky.jpg")
st.title("Exploring the New York Housing Market")
st.caption("Data Source: https://www.kaggle.com/datasets/nelgiriyewithana/new-york-housing-market")
st.write("Use the sidebar to filter the data and explore charts and maps.")

# -------------------------
# SIDEBAR FILTERS (WIDGETS)
# -------------------------

st.sidebar.header("Filters")

#[ST0] Dropdown
borough_choice = st.sidebar.selectbox(
    " Select Borough",
    get_unique_borough(df)
)


# [ST2] Slider
MAX_SLIDER_CAP = 25000000
max_price_choice = st.sidebar.slider(
    "Maximum Price",
    min_value=int(df["PRICE"].min()),
    max_value=MAX_SLIDER_CAP,
    value=5000
)

filtered_df = filter_listings(df, borough_choice, max_price_choice)  # [FUNCCALL2]



# ================================
# [MAP] CUSTOM PYDECK MAP
# ================================

st.header("Map of Listings")
map_df = filtered_df.dropna(subset=["LATITUDE", "LONGITUDE"])

if  not map_df.empty:
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=map_df,
        get_position='[LONGITUDE, LATITUDE]',
        get_radius=60,
        get_color=[200, 30, 0, 160],
        pickable=True
    )

    view_state = pdk.ViewState(
        latitude=float(map_df["LATITUDE"].mean()),
        longitude=float(map_df["LONGITUDE"].mean()),
        zoom=10
    )

    tooltip_config = {
        "html":"<b>Address:</b> {ADDRESS}<br><b>Price:</b>${PRICE}<br>",
    }
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state,tooltip = tooltip_config))
else:
    st.warning("No listings found")



# ================================
# END
# ================================