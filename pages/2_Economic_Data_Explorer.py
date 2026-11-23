# Lab 3: API data page
# TODO: Rename this file to fit your page. Keep the number at the front, since it sets the
#       page's order in the sidebar (for example, 2_Pokedex.py).
#
# This page shows data from your API, processed with your own Python code. No AI on this page.
# It should have:
#   - at least 2 meaningful user inputs (for example st.selectbox, st.text_input, st.slider)
#   - at least 2 dynamic visuals that change based on the user's input: charts, displays of
#     images, or other visualizations (see the example website for examples!)

import requests
import streamlit as st


# Get data from WB
def get_api_data(url, params):
    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        return response.json()

    except (requests.RequestException, ValueError):
        return None


st.title("Economic Data Explorer")
st.write("Explore economic trends from countries around the world using real data from the World Bank! Choose a country and a time period to see how GDP growth has changed over time and compare its average GDP growth, inflation, and population growth rates!!")

# Get list of countries from WB
@st.cache_data
def get_countries():
    url = "https://api.worldbank.org/v2/country"

    response = requests.get(
        url,
        params={"format": "json", "per_page": 400},
        timeout=15
    )
    response.raise_for_status()
    data = response.json()

    country_codes = {}

    for country in data[1]:
        if country["region"]["id"] != "NA":
            country_codes[country["name"]] = country["id"]

    return country_codes


try:
    country_codes = get_countries()
except (requests.RequestException, ValueError, KeyError, IndexError, TypeError):
    st.error("Unable to load countries from the World Bank. Please try again.")
    st.stop()

if len(country_codes) == 0:
    st.warning("No countries were available.")
    st.stop()

countries = sorted(country_codes.keys())

selected_country = st.selectbox("Select a country", countries)


year_range = st.slider(
    "Select a year range",
    min_value=2000,
    max_value=2024,
    value=(2010, 2024)
)

# Get the selected country's code
country_code = country_codes[selected_country]

# GDP GI from WB
indicator = "NY.GDP.MKTP.KD.ZG"

# Get the selected starting & ending years
start_year = year_range[0]
end_year = year_range[1]

# Creates WB API URL
url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/{indicator}"

gdp_values = []
# Get GDP growth data from WB
data = get_api_data(
    url,
    {
        "format": "json",
        "date": f"{start_year}:{end_year}",
        "per_page": 100
    }
)


# Check if the data was retrieved
if isinstance(data, list) and len(data) > 1 and isinstance(data[1], list):
    # Pull GDP growth values and years
    years = []
    gdp_values = []

    for entry in data[1]:
        if entry["value"] is not None:
            years.append(entry["date"])
            gdp_values.append(entry["value"])

    # Organize data chronologically
    years.reverse()
    gdp_values.reverse()

    # Display GDP growth over time
    if len(years) > 0:
        st.subheader(f"GDP Growth Over Time: {selected_country}")

        chart_data = {
            "Year": years,
            "GDP Growth (%)": gdp_values
        }

        st.line_chart(chart_data, x="Year", y="GDP Growth (%)")
    else:
        st.warning("No GDP growth values available for the selected years.")
else:
    st.warning("GDP data could not be loaded from the World Bank.")



# More economic indicators
indicators = {
    "Inflation": "FP.CPI.TOTL.ZG",
    "Population Growth": "SP.POP.GROW"
}
# Store the average values
average_values = {}

for indicator_name, indicator_code in indicators.items():

    # Get data for this economic indicator
    indicator_url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/{indicator_code}"

    indicator_data = get_api_data(
        indicator_url,
        {
            "format": "json",
            "date": f"{start_year}:{end_year}",
            "per_page": 100
        }
    )

    # Check that the API returned usable data
    if isinstance(indicator_data, list) and len(indicator_data) > 1 and isinstance(indicator_data[1], list):

        values = []

        for entry in indicator_data[1]:
            if entry["value"] is not None:
                values.append(entry["value"])

        # Calculate the average for the selected years
        if len(values) > 0:
            average_values[indicator_name] = sum(values) / len(values)


# Get average economic indicators
if len(average_values) > 0:
    st.subheader(f"Average Economic Indicators: {selected_country}")

    # Include GDP growth in the comparison
    if len(gdp_values) > 0:
        average_values["GDP Growth"] = sum(gdp_values) / len(gdp_values)


    indicator_names = list(average_values.keys())
    indicator_averages = list(average_values.values())

    bar_chart_data = {
        "Indicator": indicator_names,
        "Average (%)": indicator_averages
    }

    # Display a horizontal bar chart
    st.bar_chart(
        bar_chart_data,
        x="Indicator",
        y="Average (%)",
        horizontal=True
    )

else:
    st.warning("No additional economic indicator data was available.")

