import requests
import pydeck as pdk
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import json

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

def write_to_file(data, file_name):
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4)

def extract_centroid(rings):
    x_coords = [point[0] for ring in rings for point in ring]
    y_coords = [point[1] for ring in rings for point in ring]
    centroid = {
        "longitude": sum(x_coords) / len(x_coords),
        "latitude": sum(y_coords) / len(y_coords)
    }
    return centroid

def fetch_drought_data():
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        features = data.get('features', [])
        drought_categories = {
            'd0': {'color': [255, 255, 0], 'label': 'D0 (Abnormally Dry)'},
            'd1': {'color': [255, 165, 0], 'label': 'D1 (Moderate Drought)'},
            'd2': {'color': [255, 0, 0], 'label': 'D2 (Severe Drought)'},
            'd3': {'color': [139, 0, 0], 'label': 'D3 (Extreme Drought)'},
            'd4': {'color': [128, 0, 128], 'label': 'D4 (Exceptional Drought)'},
        }
        processed_data = []
        for feature in features:
            attributes = feature.get('attributes', {})
            geometry = feature.get('geometry', {})
            rings = geometry.get('rings', [])
            centroid = extract_centroid(rings) if rings else {"longitude": None, "latitude": None}
            processed_data.append({
                "OBJECTID": attributes.get("OBJECTID"),
                "period": attributes.get("period"),
                "dm": attributes.get("dm"),
                "centroid": centroid,
                "rings": rings,
                "area": attributes.get("Shape__Area"),
                "length": attributes.get("Shape__Length"),
                "color": drought_categories.get(f'd{attributes.get("dm")}', {}).get("color", [128, 128, 128]),
                "label": drought_categories.get(f'd{attributes.get("dm")}', {}).get("label", "Unknown")
            })
        write_to_file(processed_data, "processed_drought_data.json")
        return processed_data, drought_categories
    else:
        print(f"Error fetching data: {response.status_code}")
        return [], {}

def plot_with_matplotlib(polygons):
    fig, ax = plt.subplots(figsize=(10, 6))
    for polygon in polygons:
        for ring in polygon["rings"]:
            xs, ys = zip(*ring)
            ax.fill(xs, ys, facecolor=[c / 255 for c in polygon["color"]], edgecolor="black", alpha=0.5)
    ax.set_title('Drought Polygons - Matplotlib')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    return fig

def display_drought_map():
    st.title("Drought Intensity Visualization")
    drought_data, drought_key = fetch_drought_data()

    if drought_data:
        polygons = [
            {
                "rings": entry["rings"], 
                "color": entry["color"],
                "label": entry["label"]
            }
            for entry in drought_data if entry["rings"]
        ]
        write_to_file(polygons, "polygons_for_pydeck.json")

        polygon_layer = pdk.Layer(
            "PolygonLayer",
            data=polygons,
            get_polygon="rings",
            get_fill_color="[color[0], color[1], color[2], 80]",
            get_line_color=[0, 0, 0],
            pickable=True,
            auto_highlight=True,
        )

        view_state = pdk.ViewState(
            latitude=0,
            longitude=0,
            zoom=1,
            bearing=0, 
            pitch=0
        )

        r = pdk.Deck(
            layers=[polygon_layer],
            initial_view_state=view_state,
            tooltip={"text": "{label}"}
        )

        col1, col2 = st.columns([1, 1])

        with col1:
            st.pydeck_chart(r)

        fig = plot_with_matplotlib(polygons)
        with col2:
            st.pyplot(fig)

    else:
        st.error("Failed to fetch drought data.")

def display_custom_legend(drought_key):
    fig, ax = plt.subplots(figsize=(3, 2))
    legend_items = []
    for category, data in drought_key.items():
        hex_color = f"#{''.join([f'{int(x):02X}' for x in data['color']])}"
        legend_items.append(mpatches.Patch(color=hex_color, label=data['label']))
    ax.legend(handles=legend_items, title="Drought Intensity", loc='center', fontsize='small', title_fontsize='small')
    ax.axis('off')
    st.pyplot(fig)

if __name__ == "__main__":
    display_drought_map()
