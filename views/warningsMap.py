# views/warningsMap.py

import streamlit as st
import pandas as pd
import pydeck as pdk
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from warningsData import main as get_warnings_data, INTERESTED_EVENTS
from views.dashboard import get_coordinates
import requests

def display_event_map(lat=None, lon=None):
    st.title("NASA Warning Events - Streamlit Map with Compact Legend")

    st.write("Fetching warning data...")

    event_properties, coordinates, labels = get_warnings_data()

    event_list = []
    for event_type, events in event_properties.items():
        for event in events:
            event_list.append({
                'latitude': event['latitude'],
                'longitude': event['longitude'],
                'event_type': event_type
            })

    df = pd.DataFrame(event_list)

    unique_event_types = INTERESTED_EVENTS
    num_event_types = len(unique_event_types)

    color_palette = [
        [255, 0, 0],     # Red
        [0, 255, 0],     # Bright green
        [0, 0, 255],     # Bright blue
        [255, 255, 0],   # Yellow
        [255, 165, 0],   # Orange
        [255, 0, 255],   # Magenta
        [0, 255, 255],   # Cyan
        [75, 0, 130],    # Indigo
        [255, 20, 147],  # Deep pink
        [0, 255, 127],   # Spring green
        [255, 105, 180]  # Hot pink
    ]

    event_type_colors = dict(zip(unique_event_types, color_palette))

    df['color'] = df['event_type'].map(event_type_colors)

    if lat is None or lon is None:
        lat, lon = 39.5, -98.35

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position='[longitude, latitude]',
        get_radius=6000,
        get_fill_color='color',
        pickable=True,
    )

    view_state = pdk.ViewState(
        latitude=lat, 
        longitude=lon,
        zoom=6,
        pitch=0
    )

    col1, col2 = st.columns([10, 4])

    with col1:
        st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))

    with col2:
        display_custom_legend(event_type_colors)

def display_custom_legend(event_type_colors):
    fig, ax = plt.subplots(figsize=(3, 2))

    legend_items = []
    for event_type, color in event_type_colors.items():
        hex_color = f"#{''.join([f'{x:02X}' for x in color])}"
        legend_items.append(mpatches.Patch(color=hex_color, label=event_type))

    ax.legend(handles=legend_items, title="Event Types", loc='center', fontsize='small', title_fontsize='small')
    ax.axis('off')
    st.pyplot(fig)

def main():
    st.title("Environmental Metrics and Warning Events")

    st.sidebar.header("Location Input")

    location_method = st.sidebar.radio("Select Location Input Method", ("Manual Entry", "Automatic Detection"))

    if location_method == "Manual Entry":
        city = st.sidebar.text_input("Enter Your City Name", value="New York")
    else:
        try:
            ip_response = requests.get("https://ipinfo.io/json")
            ip_data = ip_response.json()
            city = ip_data.get("city", "New York")
            st.sidebar.write(f"Detected City: **{city}**")
        except:
            st.sidebar.write("Could not detect location automatically. Please enter manually.")
            city = st.sidebar.text_input("Enter Your City Name", value="New York")

    lat, lon = get_coordinates(city)

    if lat is None or lon is None:
        st.error("Could not geocode the provided city name. Please check and try again.")
        return

    display_event_map(lat, lon)

if __name__ == "__main__":
    main()
