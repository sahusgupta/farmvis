import requests
import folium
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium
import json

# Base URL for US Drought Current (ID: 3)
url = "https://services9.arcgis.com/RHVPKKiFTONKtxq3/arcgis/rest/services/US_Drought_Intensity_v1/FeatureServer/3/query"

params = {
    'where': '1=1',
    'outFields': '*',
    'returnGeometry': 'true',
    'returnCentroid': 'true',
    'f': 'json',
    'resultRecordCount': 1000,
    'outSR': 4326
}

def fetch_drought_data():
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        features = data.get('features', [])
        drought_categories = {
            'd0': {'color': '#FFFF00', 'label': 'D0 (Abnormally Dry)'},
            'd1': {'color': '#FFA500', 'label': 'D1 (Moderate Drought)'},
            'd2': {'color': '#FF0000', 'label': 'D2 (Severe Drought)'},
            'd3': {'color': '#8B0000', 'label': 'D3 (Extreme Drought)'},
            'd4': {'color': '#800080', 'label': 'D4 (Exceptional Drought)'},
        }
        processed_data = []
        for feature in features:
            attributes = feature.get('attributes', {})
            geometry = feature.get('geometry', {})
            rings = geometry.get('rings', [])
            processed_data.append({
                "OBJECTID": attributes.get("OBJECTID"),
                "period": attributes.get("period"),
                "dm": attributes.get("dm"),
                "rings": rings,
                "label": drought_categories.get(f'd{attributes.get("dm")}', {}).get("label", "Unknown")
            })
        return processed_data, drought_categories
    else:
        print(f"Error fetching data: {response.status_code}")
        return [], {}

def create_choropleth_map(drought_data, drought_key):
    df = pd.DataFrame(drought_data)


    m = folium.Map(location=[39.5, -98.35], zoom_start=4)

    geojson_features = []
    for entry in drought_data:
        geojson_features.append({
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": entry["rings"]
            },
            "properties": {
                "OBJECTID": entry["OBJECTID"],
                "drought_level": entry["dm"]
            }
        })

    geojson_data = {
        "type": "FeatureCollection",
        "features": geojson_features
    }

    folium.Choropleth(
        geo_data=geojson_data,
        name='choropleth',
        data=df,
        columns=['OBJECTID', 'dm'], 
        key_on='feature.properties.OBJECTID',  
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Drought Intensity'
    ).add_to(m)

    return m

def display_drought_map():
    st.title("Drought Intensity Visualization")
    drought_data, drought_key = fetch_drought_data()

    if drought_data:
        
        m = create_choropleth_map(drought_data, drought_key)
        st_folium(m, width=700, height=500)

    else:
        st.error("Failed to fetch drought data.")

def display_drought_key():
    st.sidebar.title("Drought Intensity Legend")


    with st.sidebar.expander("D0 - Abnormally Dry", expanded=False):
        st.write("""
            **Description:** Abnormally Dry  
            **Possible Impacts:** Going into drought: short-term dryness slows growth of crops/pastures.
            Coming out of drought: some lingering water deficits; crops/pastures not fully recovered.
        """)
    
    with st.sidebar.expander("D1 - Moderate Drought", expanded=False):
        st.write("""
            **Description:** Moderate Drought  
            **Possible Impacts:** Some damage to crops/pastures; streams, reservoirs, or wells are low with some
            water shortages developing or imminent; voluntary water-use restrictions requested.
        """)
    
    with st.sidebar.expander("D2 - Severe Drought", expanded=False):
        st.write("""
            **Description:** Severe Drought  
            **Possible Impacts:** Crop/pasture losses are likely; water shortages are common and water restrictions are imposed.
        """)
    
    with st.sidebar.expander("D3 - Extreme Drought", expanded=False):
        st.write("""
            **Description:** Extreme Drought  
            **Possible Impacts:** Major crop/pasture losses; widespread water shortages or restrictions.
        """)
    
    with st.sidebar.expander("D4 - Exceptional Drought", expanded=False):
        st.write("""
            **Description:** Exceptional Drought  
            **Possible Impacts:** Exceptional and widespread crop/pasture losses; shortages of water in reservoirs, streams, and wells creating water emergencies.
        """)
        
if __name__ == "__main__":
    display_drought_map()
