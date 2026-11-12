# To run the code, execute this line in a terminal: "streamlit run interfaz.py"

import streamlit as st
import pandas as pd
import numpy as np
import folium
import matplotlib.pyplot as plt
import plotly.express as px
from streamlit_folium import st_folium
from urllib.request import urlopen
import json
import os

# Page Configuration
st.set_page_config(page_title="Titan Boat", page_icon="⛵", layout="wide")

# ThingSpeak channel and read key come from environment variables,
# so no credentials are stored in the code.
READ_API_KEY = os.getenv("THINGSPEAK_READ_API_KEY")
CHANNEL_ID = os.getenv("THINGSPEAK_CHANNEL_ID")
if not READ_API_KEY or not CHANNEL_ID:
    st.error("Set the THINGSPEAK_CHANNEL_ID and THINGSPEAK_READ_API_KEY environment variables to load the sensor data.")
    st.stop()

TS = urlopen(f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json?api_key={READ_API_KEY}&results=100")
response = TS.read() #Request the url
df = json.loads(response) # Get the response of the web server
feeds = df["feeds"] # The data are here, check it.
df = pd.DataFrame(feeds)
df.rename(columns={"field1": "Turbidity", "field2": "pH", "field3": "Temperature"}, inplace=True)

# Application Title
st.title("Titan Boat - Group 9")

# Create example data for temperature
np.random.seed(0)
temperature_data_celsius = df[['Temperature']]

# Rename columns for x and y axes
temperature_data_celsius = temperature_data_celsius.rename(columns={'index': 'Time', 'Temperature': 'Temperature (C)'})

# Header with text "Temperature"
st.header("1. Temperature Sensor in Celsius")

# Slider to control the x-axis range
selected_time_temp_celsius = st.slider("Select time range (Celsius)", min_value=0, max_value=100, value=(0, 100), step=1, key="temp_celsius")

# Create a line chart with Plotly
fig_temp_celsius = px.line(temperature_data_celsius.iloc[selected_time_temp_celsius[0]:selected_time_temp_celsius[1]+1], x=temperature_data_celsius.index[selected_time_temp_celsius[0]:selected_time_temp_celsius[1]+1], y='Temperature (C)')
fig_temp_celsius.update_traces(line=dict(color='blue', width=2))  # Specify line color and width
fig_temp_celsius.update_xaxes(title_text='Time')
fig_temp_celsius.update_yaxes(title_text='Temperature (C)')
st.plotly_chart(fig_temp_celsius, use_container_width=True, width=800)  # Specify chart width

# Create example data for turbidity
np.random.seed(0)
turbidity_data = df[['Turbidity']]

# Rename columns for x and y axes
turbidity_data = turbidity_data.rename(columns={'index': 'Time', 'Turbidity': 'Turbidity (uT)'})

st.divider()

# Header with text "Turbidity"
st.header("2. Turbidity Sensor")

# Slider to control the x-axis range
selected_time_turbidity = st.slider("Select time range (Turbidity)", min_value=0, max_value=100, value=(0, 100), step=1, key="turbidity")

# Create a line chart with Plotly
fig_turbidity = px.line(turbidity_data.iloc[selected_time_turbidity[0]:selected_time_turbidity[1]+1], x=turbidity_data.index[selected_time_turbidity[0]:selected_time_turbidity[1]+1], y='Turbidity (uT)')
fig_turbidity.update_traces(line=dict(color='red', width=2))  # Specify line color and width
fig_turbidity.update_xaxes(title_text='Time')
fig_turbidity.update_yaxes(title_text='Turbidity (uT)')
st.plotly_chart(fig_turbidity, use_container_width=True, width=800)  # Specify chart width

# Create example data for pH
np.random.seed(0)
ph_data = df[['pH']]

# Rename columns for x and y axes
ph_data = ph_data.rename(columns={'index': 'Time', 'pH': 'pH'})

st.divider()

# Header with text "pH"
st.header("3. pH Sensor")

# Slider to control the x-axis range
selected_time_ph = st.slider("Select time range (pH)", min_value=0, max_value=100, value=(0, 100), step=1, key="ph")

# Create a line chart with Plotly
fig_ph = px.line(ph_data.iloc[selected_time_ph[0]:selected_time_ph[1]+1], x=ph_data.index[selected_time_ph[0]:selected_time_ph[1]+1], y='pH')
fig_ph.update_traces(line=dict(color='green', width=2))  # Specify line color and width
fig_ph.update_xaxes(title_text='Time')
fig_ph.update_yaxes(title_text='pH')
st.plotly_chart(fig_ph, use_container_width=True, width=800)  # Specify chart width

st.divider()

# Header with text "Location"
st.header("4. Location")

# Create interactive map
m = folium.Map(location=[43.304654, -2.009873], zoom_start=16)
folium.Marker([43.304654, -2.009873], icon=folium.Icon(color='red')).add_to(m)

st_data = st_folium(m, width=1600)

st.divider()

# Data History Section
st.header("5. Data History")

# Show the table in Streamlit with a custom width
st.dataframe(df[['Temperature', 'pH', 'Turbidity']], width=1600)

st.divider()

# Data Analysis Section
st.header("6. Data Analysis")

# Subheader
st.subheader("- pH Dispersion vs Turbidity with Linear Regression")

# Scatter plot with linear regression
scatter_fig = px.scatter(df, x='pH', y='Turbidity',                        
                         labels={'pH': 'pH', 'Turbidity': 'Turbidity (uT)'},
                         trendline='ols',  # Add a linear regression line (OLS)
                         width=1350, height=600)  # Adjust width and height of the plot

# Set point color to dark blue and no transparency
scatter_fig.update_traces(marker=dict(size=12, color='yellow', opacity=1))

# Set regression line color to red
scatter_fig.update_traces(line=dict(color='red'))

# Show the plot
st.plotly_chart(scatter_fig)
