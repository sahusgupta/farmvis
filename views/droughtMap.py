import streamlit as st
import pydeck as pdk
from droughtData import fetch_drought_data

def display_drought_map():
    st.title("Drought Intensity Visualization")

    drought_data, drought_key = fetch_drought_data()

    if drought_data:
        polygons = prepare_data_for_pydeck(drought_data)

        polygon_layer = pdk.Layer(
            "PolygonLayer",
            data=polygons,
            get_polygon="coordinates",
            get_fill_color="color",
            get_line_color=[0, 0, 0],
            line_width_min_pixels=1,
            pickable=True,
            extruded=False,
        )

        view_state = pdk.ViewState(latitude=39.5, longitude=-98.35, zoom=4, bearing=0, pitch=0)

        r = pdk.Deck(
            layers=[polygon_layer],
            initial_view_state=view_state,
            tooltip={"text": "{label}"},
        )

        st.pydeck_chart(r)

    else:
        st.error("Failed to fetch drought data.")

def prepare_data_for_pydeck(drought_data):
    polygons = []
    for entry in drought_data:
        if entry["rings"]:
            if entry["rings"][0] != entry["rings"][-1]:
                entry["rings"].append(entry["rings"][0])

            color = [min(max(c, 0), 255) for c in entry["color"]]
            color.append(120)

            polygon_info = {
                "coordinates": entry["rings"],
                "color": color,
                "label": entry["label"],
            }
            polygons.append(polygon_info)

    return polygons

if __name__ == "__main__":
    display_drought_map()
