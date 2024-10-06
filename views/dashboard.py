import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import random
from dotenv import load_dotenv
import os

# ---------------------------
# Configuration and Constants
# ---------------------------

# Load environment variables from the .env file
load_dotenv()

# Fetch the API key from the environment variable
API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')

if not API_KEY:
    st.error("API Key for OpenWeatherMap is missing. Please set it in the .env file.")
    st.stop()

# Initialize Geolocator
geolocator = Nominatim(user_agent="streamlit_app")

# ---------------------------
# Helper Functions
# ---------------------------

@st.cache_data
def get_coordinates(city_name):
    """
    Convert a city name to its latitude and longitude.
    """
    try:
        location = geolocator.geocode(city_name, timeout=10)
        if location:
            return (location.latitude, location.longitude)
        else:
            return (None, None)
    except GeocoderTimedOut:
        return (None, None)

@st.cache_data
def fetch_weather_data(lat, lon):
    """
    Fetch current weather and AQI data from OpenWeatherMap APIs.
    """
    # OpenWeatherMap API endpoints
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    aqi_url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    
    # Fetch weather data
    weather_response = requests.get(weather_url)
    weather_data = weather_response.json()
    
    # Fetch AQI data
    aqi_response = requests.get(aqi_url)
    aqi_data = aqi_response.json()
    
    return weather_data, aqi_data

def display_donut_chart(title, probability):
    """
    Create and display a donut chart for a given probability.
    The remaining portion of the chart is blank without any labels.
    """
    fig = go.Figure(
        data=[go.Pie(
            labels=["Probability", ""],
            values=[probability, 100 - probability],
            hole=0.6,
            hoverinfo='label+percent',
            marker=dict(colors=["#FF6347", "rgba(0,0,0,0)"], line=dict(color='white', width=1))
        )]
    )
    
    fig.update_traces(
        textinfo='percent',
        textposition='inside',
        showlegend=False
    )
    
    fig.update_layout(
        title_text=title,
        annotations=[dict(text=f"{probability}%", x=0.5, y=0.5, font_size=20, showarrow=False)]
    )
    
    st.plotly_chart(fig, use_container_width=True)

def get_aqi_description(aqi_value):
    """
    Convert AQI numerical value to a descriptive category.
    """
    descriptions = {
        1: "Good",
        2: "Fair",
        3: "Moderate",
        4: "Poor",
        5: "Very Poor"
    }
    return descriptions.get(aqi_value, "Unknown")

def main():
    """
    Display vironmental metrics with specific layout:
    - First renow: Temperature, Humidity, Wind Speed, AQI (4 columns)
    - Second row: Flood Probability and Drought Probability (2 columns)
    """
    city = st.sidebar.text_input("City", value="New York", placeholder="Enter city name")
    coords = get_coordinates(city)
    weather_data, aqi_data = fetch_weather_data(coords[0], coords[1])
    # Generate random probabilities
    flood_probability = round(random.uniform(0, 100), 2)
    drought_probability = round(random.uniform(0, 100), 2)
    
    # First Row: Temperature, Humidity, Wind Speed, AQI
    st.markdown("## Environmental Conditions")
    env_cols = st.columns(4)
    
    with env_cols[0]:
        st.markdown("### 🌡️ Temperature (°C)")
        st.metric(label="", value=weather_data['main']['temp'])
    
    with env_cols[1]:
        st.markdown("### 💧 Humidity (%)")
        st.metric(label="", value=weather_data['main']['humidity'])
    
    with env_cols[2]:
        st.markdown("### 🌬️ Wind Speed (m/s)")
        wind_speed = weather_data['wind']['speed'] if 'speed' in weather_data['wind'] else 'N/A'
        st.metric(label="", value=wind_speed)
    
    with env_cols[3]:
        st.markdown("### 🌫️ Air Quality Index (AQI)")
        aqi_value = aqi_data['list'][0]['main']['aqi'] if 'list' in aqi_data and aqi_data['list'] else 'N/A'
        aqi_description = get_aqi_description(aqi_value) if isinstance(aqi_value, int) else 'N/A'
        st.metric(label="", value=f"{aqi_value} ({aqi_description})")
    
    st.markdown("---")
    
    # Second Row: Flood and Drought Probabilities
    st.markdown("## Environmental Probabilities")
    prob_cols = st.columns(2)
    
    with prob_cols[0]:
        st.markdown("### 🌊 Flood Probability")
        display_donut_chart("🌊 Flood Probability", flood_probability)
    
    with prob_cols[1]:
        st.markdown("### 🌵 Drought Probability")
        display_donut_chart("🌵 Drought Probability", drought_probability)
