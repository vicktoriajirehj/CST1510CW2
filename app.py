import streamlit as st
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(__file__))

st.set_page_config(page_title = "Multi-Domain Intelligence Platform")

st.title("Multi-Domain Intelligence Platform")
st.write("Use the sidebar to Navigate")
st.write("Please login first")