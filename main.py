import streamlit as st
import openai as oa
import os
from views.prefs import farm_information_form

st.sidebar.title("Navigation")
options = st.sidebar.radio("Go to", ("Dashboard", "Preferences", "About"))

if options == "Dashboard":
    pass
elif options == "About":
    pass
elif options == "Preferences":
    farm_information_form()
    
    