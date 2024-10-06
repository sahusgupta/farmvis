# main_app.py

import streamlit as st
from views.prefs import farm_information_form
from views.dashboard import main
from views.about import main as a_main
from views.warningsMap import display_event_map, display_event_key
from views.droughtMap import display_drought_map, display_drought_key
from views.soilMoistureMap import embed_arcgis_map

st.sidebar.title("Navigation")
options = st.sidebar.radio("Go to", ("Dashboard", "Preferences", "About", "Maps"))

if options == "Dashboard":
    main()
elif options == "About":
    a_main()
elif options == "Preferences":
    farm_information_form()
elif options == "Maps":
    st.subheader("Choose a Map to Display")

    map_options = st.radio("Select Map", ("Event Map", "Drought Map", "Soil Moisture Map"))

    if map_options == "Event Map":
        display_event_map()
        display_event_key()
        
        st.markdown("This map shows live weather warnings for hazardous events.")
    elif map_options == "Drought Map":
        display_drought_map()
        display_drought_key()
        st.markdown("This map shows live levels of drought conditions.")
        
    elif map_options == "Soil Moisture Map":
        embed_arcgis_map()
        st.markdown("This map shows soil moisture levels.")
