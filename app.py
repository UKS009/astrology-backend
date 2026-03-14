import streamlit as st
import requests
import json
from geopy.geocoders import Nominatim

# --- CONFIGURATION ---
API_KEY = "AIzaSyD1dIJValIcbBhuKDljpQRj6lxn0AsbN-g"

# 2026 Stable Endpoint for Free Tier
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"

st.set_page_config(page_title="Vedic AI Astrologer", layout="wide")
st.title("✨ Agentic Vedic Astrologer")

with st.sidebar:
    st.header("Birth Details")
    name = st.text_input("Name")
    city = st.text_input("Birth City (e.g., Delhi, India)")
    submit = st.button("Generate Analysis")

def call_gemini(prompt):
    headers = {'Content-Type': 'application/json'}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Error: {response.status_code}. Please check if API Key is correct."
    except Exception as e:
        return f"Connection Error: {e}"

if submit and city:
    geolocator = Nominatim(user_agent="astro_2026")
    location = geolocator.geocode(city)
    if location:
        prompt = f"Act as a Vedic Astrologer. Analyze for {name} born in {city}. Provide Rashi and Nakshatra insights."
        with st.spinner("Reading the stars..."):
            st.markdown(call_gemini(prompt))
    else:
        st.error("City not found.")
