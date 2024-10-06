# main_app.py

import streamlit as st
from views.prefs import farm_information_form
from views.dashboard import main
from views.about import main as a_main
from views.warningsMap import display_event_map
from views.droughtMap import display_drought_map
# Sidebar navigation
st.sidebar.title("Navigation")
options = st.sidebar.radio("Go to", ("Dashboard", "Preferences", "About", "Maps"))  # Add "Heatmap" option

# Navigation logic
if options == "Dashboard":
    main()
elif options == "About":
    a_main()
elif options == "Preferences":
    farm_information_form()
elif options == "Maps":
    display_event_map()
    display_drought_map()
