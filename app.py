"""
    Used Streamlit to create a simple web application to demonstrate my A* path finding API.
"""

import subprocess
import time
import requests
import streamlit as st
import atexit
import folium
from streamlit_folium import st_folium

# API server URL and URI
api_url = "http://localhost:8000"
api_uri = api_url + "/findPath"

# Check if the API server is running
@st.cache_data(show_spinner=False)
def check_api_health():
    try:
        response = requests.get(api_url)
        return response.status_code == 200
    except:
        return False

# Start the API server if it is not running
if "api_process" not in st.session_state:
    st.session_state.api_process = None
    if not check_api_health():
        st.session_state.api_process = subprocess.Popen(
            ["uvicorn", "src:app", "--reload"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        time.sleep(5)  

# Cleanup function to stop the API server
def cleanup():
    if st.session_state.api_process is not None:
        st.session_state.api_process.terminate()

atexit.register(cleanup)

st.title("Route Finder with A* Algorithm")
st.caption("This application only supports locations from João Pessoa, Paraíba, Brazil.")
st.caption("The path is based on all network types, so it does not consider the streets orientations.")

if "start_location" not in st.session_state:
    st.session_state.start_location = "Terceirão"
if "end_location" not in st.session_state:
    st.session_state.end_location = "Busto de Tamandaré"
if "route_data" not in st.session_state:
    st.session_state.route_data = None

st.session_state.start_location = st.text_input(label="Start Location", value=st.session_state.start_location)
st.session_state.end_location = st.text_input(label="End Location", value=st.session_state.end_location)

# Calculate the route if the button is clicked
if st.button("Calculate Route"):
    try:
        # Call the API to calculate the route and retrieve the data
        response = requests.get(
            url=api_uri,
            params={
                "start_loc": st.session_state.start_location,
                "end_loc": st.session_state.end_location,
            },
        )
        if response.status_code == 200:
            # In success, store the retrived data in the session
            st.session_state.route_data = response.json()  
        else:
            st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
    except Exception as e:
        st.error(f"Failed to connect to the API: {e}")

if st.session_state.route_data:
    data = st.session_state.route_data

    st.text(f"Total Distance: {data['cost']:.2f} meters")

    coordinates = data["path"]

    map_center = coordinates[0]
    route_map = folium.Map(location=map_center, zoom_start=13)

    folium.PolyLine(coordinates, color="blue", weight=5, opacity=0.8).add_to(route_map)

    folium.Marker(coordinates[0], tooltip="Start", icon=folium.Icon(color="green")).add_to(route_map)
    folium.Marker(coordinates[-1], tooltip="End", icon=folium.Icon(color="red")).add_to(route_map)

    st_folium(route_map, width=700, height=400)