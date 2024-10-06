import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import random
# ---------------------------
# Configuration and Constants
# ---------------------------

API_KEY = 'YOUR_OPENWEATHERMAP_API_KEY'  # Replace with your OpenWeatherMap API key

# Initialize Geolocator
geolocator = Nominatim(user_agent="streamlit_app")

@st.cache_data
def get_coordinates(city_name):
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
    # OpenWeatherMap API endpoint
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    
    # Fetch weather data
    weather_response = requests.get(weather_url)
    weather_data = weather_response.json()
    
    # Fetch AQI data
    aqi_response = requests.get(aqi_url)
    aqi_data = aqi_response.json()
    
    return weather_data, aqi_data

def display_donut_chart(title, probability):
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

def display_metrics(data, aqi):
    # Generate random probabilities
    flood_probability = round(random.uniform(0, 100), 2)
    drought_probability = round(random.uniform(0, 100), 2)
    
    # Create two columns: Left for Temperature and Humidity, Right for Flood and Drought Probabilities
    left_col, right_col = st.columns(2)
    
    with left_col:
        # Display Temperature, Humidity, Wind Speed, and AQI
        st.subheader("📈 Current Environmental Conditions")
        temp_col, humidity_col = st.columns(2)
        
        with temp_col:
            st.metric(label="🌡️ Temperature (°C)", value=data['main']['temp'])
        
        with humidity_col:
            st.metric(label="💧 Humidity (%)", value=data['main']['humidity'])
        
        wind_col, aqi_col = st.columns(2)
        
        with wind_col:
            wind_speed = data['wind']['speed'] if 'speed' in data['wind'] else 'N/A'
            st.metric(label="🌬️ Wind Speed (m/s)", value=wind_speed)
        
        with aqi_col:
            aqi_value = aqi['list'][0]['main']['aqi'] if 'list' in aqi and aqi['list'] else 'N/A'
            aqi_description = get_aqi_description(aqi_value) if isinstance(aqi_value, int) else 'N/A'
            st.metric(label="🌫️ Air Quality Index (AQI)", value=f"{aqi_value} ({aqi_description})")
    
    with right_col:
        # Display Flood and Drought Probability Donut Charts
        st.subheader("📊 Environmental Probabilities")
        display_donut_chart("🌊 Flood Probability", flood_probability)
        display_donut_chart("🌵 Drought Probability", drought_probability)

def get_aqi_description(aqi_value):
    """Convert AQI value to descriptive category."""
    descriptions = {
        1: "Good",
        2: "Fair",
        3: "Moderate",
        4: "Poor",
        5: "Very Poor"
    }
    return descriptions.get(aqi_value, "Unknown")

# ---------------------------
# Main Application
# ---------------------------

def main():
    
    # Title of the dashboard
    st.title("🌍 Environmental Metrics Dashboard")
    
    # Sidebar for user inputs
    st.sidebar.header("Location Input")
    
    # Location input method
    location_method = st.sidebar.radio("Select Location Input Method", ("Manual Entry", "Automatic Detection"))
    
    if location_method == "Manual Entry":
        city = st.sidebar.text_input("Enter Your City Name", value="New York")
    else:
        # Use ipinfo.io to get approximate location based on IP
        try:
            ip_response = requests.get("https://ipinfo.io/json")
            ip_data = ip_response.json()
            city = ip_data.get("city", "New York")
            st.sidebar.write(f"Detected City: **{city}**")
        except:
            st.sidebar.write("Could not detect location automatically. Please enter manually.")
            city = st.sidebar.text_input("Enter Your City Name", value="New York")
    
    # Fetch coordinates
    lat, lon = get_coordinates(city)
    
    if lat is None or lon is None:
        st.error("Could not geocode the provided city name. Please check and try again.")
        return
    
    # Fetch weather and AQI data
    weather_data, aqi_data = fetch_weather_data(lat, lon)
    
    # Check for successful data retrieval
    if weather_data.get('cod') != 200:
        st.error("Failed to fetch weather data. Please check the city name or try again later.")
        return
    
    if not aqi_data.get('list'):
        st.error("Failed to fetch AQI data. Please try again later.")
        return
    
    # Display metrics
    display_metrics(weather_data, aqi_data)

# ---------------------------
# Run the Application
# ---------------------------
if __name__ == "__main__":
    main()
