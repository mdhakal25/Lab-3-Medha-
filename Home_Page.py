import streamlit as st

# Title of App
st.title("Global Growth Tracker")

# Assignment Data
# TODO: Fill out your team number, section, and team members

st.header("CS 1301")
st.subheader("Team 60, Web Development - Section A")
st.subheader("Medha Dhakal, John Michael Houlihan")

# TODO (optional): Add a group photo to the images folder and show it here, for example:
# st.image("images/group_photo.jpg")


# Introduction
# TODO: Write a quick description for all of your pages in this lab below, in the form:
#       1. **Page Name**: Description
#       2. **Page Name**: Description
#       3. **Page Name**: Description

st.write("""
Welcome to Global Growth Tracker! This app makes it easy to explore and compare economic trends in countries around the world. Using real data from the World Bank, you can look at factors like GDP growth, inflation, population growth, and unemployment to better understand how different economies are changing over time.

You can explore the app using the pages in the sidebar:

1. **Economic Data Explorer:** Choose countries, economic indicators, and time periods to compare economic trends through interactive charts.

2. **Economics Chatbot:** Chat with our AI assistant to learn more about economic concepts and discuss global economic trends.

3. **Economic Data Assistant (Lab 4):** Ask questions about specific countries and their economic data using information from the World Bank. This feature will be added in Lab 4.
""")
