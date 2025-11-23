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
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import random

df = pd.read_csv("NY_House_Dataset.csv")
#print(df.head())

# [FUNC2P][Filter 2] Function with 2+ parameters, one with default, filter with two conditions
def filter_listings(df, borough, max_price=5000):
    """
    Filter the dataframe by borough and a maximum price.
    """
    filtered = df[
        (df["LOCALITY"] == borough) &
        (df["PRICE"] <= max_price)
    ]
    return filtered


# [FUNCRETURN2][FILTER2][MAX&MIN] Function returning 2 values and filter 2 an
def get_price_range(df,borough_choice,type_property):
    """
    Return the minimum and maximum price values.
    """
    filtered_df = df[(df["LOCALITY"] == borough_choice) & (df["TYPE"] == type_property)]
    if filtered_df.empty:
        return None, None

    min_price = filtered_df["PRICE"].min()
    max_price = filtered_df["PRICE"].max()
    return min_price, max_price


# [LISTCOMP][ITRLOOP] List comprehension for unique Types of borough
def get_unique_borough(df):
    '''
    return the unique boroughs as a list.
    '''
    type_of_borough = [ t for t in df["LOCALITY"].unique()]
    return type_of_borough

# [FILTER1] Filtering based on locality
'''
Returns types of propoerties in a selcted borough as a dataframe.
'''
def get_unique_properties_boroughs(df, type_of_borough):
    filtered_df = df[df["LOCALITY"] == type_of_borough]
    type_of_properties = filtered_df["TYPE"].unique()
    return type_of_properties

# [DICTMETHOD] Dictionary method example inside a function
def count_by_borough(df,borough):
    """
    Use dictionary get() to track counts.
    and returns a dictionalry with property counts
    """
    filtered_df = df[df["LOCALITY"] == borough]
    type_counts = {}
    for index, row in filtered_df.iterrows():
        b = row["TYPE"]
        type_counts[b] = type_counts.get(b, 0) + 1
    return type_counts


# [LAMBDA][COLOUMS] Add calculated column: price per sqft
def add_price_per_sqft(df):
    """
    Add a new column calculating price per square foot using lambda.
    """
    df["PRICE_PER_SQFT"] = df.apply(
        lambda row: row["PRICE"] / row["PROPERTYSQFT"]
        if row["PROPERTYSQFT"] > 0 else None,
        axis=1
    )
    return df
#[COOL]:hexcode geenrator for color
def random_color():

    return '#{:06x}'.format(random.randint(0, 0xFFFFFF))


# ================================
# STREAMLIT USER INTERFACE
# ================================
#[ST3]
st.image("NYC_sky.jpg")
st.title("Exploring the New York Housing Market")
st.caption("Data Source: https://www.kaggle.com/datasets/nelgiriyewithana/new-york-housing-market")
st.write("Use the sidebar to filter the data and explore charts and maps.")


# -------------------------
# SIDEBAR FILTERS (WIDGETS)
# -------------------------

st.sidebar.header("Filters")

#[ST1] Dropdown
st.sidebar.write("Select a borough option to know the average price range")
raw_options = get_unique_borough(df) # fucntion call
PLACEHOLDER = "Select a Borough"
drop_down  = [PLACEHOLDER] + raw_options
borough_choice = st.sidebar.selectbox(
    " Select Borough",
    drop_down,
    index = 0
)

# [ST3] Radio buttion
st.sidebar.write("Choose type of property to know the Price Statistics")
type_property = st.sidebar.radio(
    "Type of property",
    get_unique_properties_boroughs(df, borough_choice)
)

# [ST2] Slider
st.sidebar.write("Move the slider to change the Price Range")
MAX_SLIDER_CAP = 25000000
max_price_choice = st.sidebar.slider(
    "Maximum Price",
    min_value=int(df["PRICE"].min()),
    max_value=MAX_SLIDER_CAP,
    value=5000
)








# ================================
# [CHART1] BAR CHART — AVERAGE PRICE BY TYPE
# ================================
#[DICTMETHOD]
st.header(f"Average Price by Housing Type in {borough_choice}") # Removed extra newlines
filtered_df_borough = df[df["LOCALITY"] == borough_choice]
avg_prices_series = filtered_df_borough.groupby("TYPE")["PRICE"].mean()
avg_prices_sorted = avg_prices_series.sort_values(ascending=False)
types = avg_prices_sorted.index
prices = avg_prices_sorted.values
plt.figure(figsize=(10, 6))
plt.bar(types, prices, color=random_color())
plt.xlabel("Type of property", fontsize=14)
plt.ylabel("Average Price (USD)", fontsize=14)
plt.title(f"Average Price by Type of Property in {borough_choice}\n\n") # Removed extra newlines
plt.xticks(rotation=45, ha="right")

def millions_formatter(x, pos): #this part of the code is based on the response from Google's Gemini. Take a look at accompaniying document
    # Divide the value by 1 million (1e6) and format to one decimal place
    return f'${x * 1e-6:.1f}M'
plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(millions_formatter))
plt.tight_layout() # Crucial to prevent labels from being cut off
st.pyplot(plt)


# ================================
# SHOW BASIC STATS
# ================================

st.header("Price Statistics")
st.write(f"Please Select the type of property to know the Minimum and Maximum Price in {borough_choice}")

min_price, max_price = get_price_range(df,borough_choice,type_property)  # [FUNCCALL2]

if min_price is None:
    st.write(" ❗**You haven't selected a borough** matching your current filters")
else:
    st.write(f"💵**Lowest Price of {type_property} in {borough_choice}:** ${min_price:,.0f}")
    st.write(f"💵💵💵**Highest Price of {type_property} in {borough_choice}:** ${max_price:,.0f}")

# ================================
# [CHART2] PIE CHART FOR PROPERTY DISTRIBUTION IN GIVER BOROUGH
# ================================

st.header(f"Property Distribution in {borough_choice}")

data = count_by_borough(df,str(borough_choice)) #funtion call
data_table = pd.Series(data).sort_values(ascending=True)
df_display = data_table.reset_index()
df_display.columns = ['Borough', 'Count']
st.subheader(f"Borough Distribution in {borough_choice}")
st.table(data_table)
#[DICTMETHOD]: .keys() and .values() nmethods
labels = list(data.keys())
values = list(data.values())
plt.figure(figsize=(10,10))
plt.pie(values,labels=labels,rotatelabels=True)
plt.legend(
    labels,
    title="Property Type",
    loc="lower left",
    bbox_to_anchor=(1.05,0)
)
plt.title("Property Distribution in selected Borough\n\n")
plt.axis('equal')
plt.tight_layout()
st.pyplot(plt)


st.title("Listing filtered by Borough and Price range")
st.write("Use the sidebar to filter the data table.")
# ================================
# DATA TABLE
# FILTER DATA USING FUNCTION
# ADDING PRICE PER SQ FT
# ================================
df = add_price_per_sqft(df)
filtered_df = filter_listings(df, borough_choice, max_price_choice)
st.write(filtered_df)


# ================================
# END
# ================================