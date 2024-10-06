import streamlit as st
import openai as oa
import os
from views.prefs import farm_information_form
from views.dashboard import main
st.sidebar.title("Navigation")
options = st.sidebar.radio("Go to", ("Dashboard", "Preferences", "About"))

if options == "Dashboard":
    main()
elif options == "About":
    pass
elif options == "Preferences":
    farm_information_form()
    
    