
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
# ================================
# STREAMLIT USER INTERFACE
# ================================

def display_dashboard():
    st.image("NYC_sky.jpg")
    st.title("Exploring the New York Housing Market")
    st.write("New York’s housing scene can feel like a whole universe of its own, full of surprises, contradictions, "
             "and stories tucked into every block. This space gives you a laid-back chance to wander through "
             "that world at your own pace — no pressure, no jargon, just a clearer look at the city we’re all trying to make sense of. "
             "Enjoy the explore."
             )
    st.caption("We are using data from: https://www.kaggle.com/datasets/nelgiriyewithana/new-york-housing-market")
    st.write("Select the Options on the side bar to proceed")


def main():
    display_dashboard()

if __name__ == "__main__":
    main()

