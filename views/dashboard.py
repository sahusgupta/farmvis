import streamlit as st
import pandas as pd
import numpy as np
from streamlit_echarts import st_echarts  # Make sure to install streamlit-echarts

# Sample data for probabilities, temperature, and humidity
np.random.seed(42)
dates = pd.date_range(start="2023-01-01", periods=10, freq="M")

# Probability tables
flood_probabilities = pd.DataFrame({
    "Date": dates,
    "Flood Probability (%)": np.random.randint(10, 90, size=len(dates))
})

drought_probabilities = pd.DataFrame({
    "Date": dates,
    "Drought Probability (%)": np.random.randint(5, 70, size=len(dates))
})

# Temperature and humidity data
temperature_data = pd.DataFrame({
    "Date": dates,
    "Temperature (°C)": np.random.uniform(15, 35, size=len(dates))
})

humidity_data = pd.DataFrame({
    "Date": dates,
    "Humidity (%)": np.random.uniform(30, 90, size=len(dates))
})

# Streamlit App Layout
st.set_page_config(layout="wide", page_title="Environmental Factors Dashboard")
st.title("Environmental Factors Dashboard")

# Sidebar for filters
st.sidebar.header("Filters")
selected_date = st.sidebar.selectbox("Select Date:", dates)

# Main layout with different sections
col1, col2 = st.columns([2, 3])

# Probability Tables
with col1:
    st.subheader("Flood Probability Table")
    st.dataframe(flood_probabilities)

    st.subheader("Drought Probability Table")
    st.dataframe(drought_probabilities)

# Gauge charts for temperature and humidity
with col2:
    st.subheader("Environmental Factors")

    # Temperature gauge
    temperature_selected = temperature_data[temperature_data["Date"] == selected_date]["Temperature (°C)"].values[0]
    temp_gauge = {
        "tooltip": {"formatter": "{a} <br/>{c} °C"},
        "series": [
            {
                "name": "Temperature",
                "type": "gauge",
                "min": 0,
                "max": 50,
                "detail": {"formatter": "{value} °C"},
                "data": [{"value": temperature_selected, "name": "Temperature"}],
                "axisLine": {
                    "lineStyle": {
                        "width": 10,
                        "color": [[0.5, "#4CAF50"], [0.75, "#FFEB3B"], [1, "#F44336"]]
                    }
                }
            }
        ]
    }
    st_echarts(temp_gauge, height="300px")

    # Humidity gauge
    humidity_selected = humidity_data[humidity_data["Date"] == selected_date]["Humidity (%)"].values[0]
    humidity_gauge = {
        "tooltip": {"formatter": "{a} <br/>{c}%"},
        "series": [
            {
                "name": "Humidity",
                "type": "gauge",
                "min": 0,
                "max": 100,
                "detail": {"formatter": "{value}%"},
                "data": [{"value": humidity_selected, "name": "Humidity"}],
                "axisLine": {
                    "lineStyle": {
                        "width": 10,
                        "color": [[0.3, "#03A9F4"], [0.7, "#4CAF50"], [1, "#FF5722"]]
                    }
                }
            }
        ]
    }
    st_echarts(humidity_gauge, height="300px")

# Footer
st.markdown("---")
st.write("Developed for monitoring key environmental factors in a simple and intuitive way.")
