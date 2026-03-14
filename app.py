import streamlit as st
import requests
import json
from geopy.geocoders import Nominatim

# --- CONFIGURATION ---
API_KEY = "AIzaSyD1dIJValIcbBhuKDljpQRj6lxn0AsbN-g"
# Direct API URL (v1 version is most stable in 2026)
API_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"

st.set_page_config(page_title="Vedic AI Astrologer", layout="wide")
st.title("✨ Agentic Vedic Astrologer")
st.subheader("AI-Powered Kundali Insights")

with st.sidebar:
    st.header("Birth Details")
    name = st.text_input("Name")
    dob = st.date_input("Date of Birth")
    tob = st.time_input("Time of Birth")
    city = st.text_input("Birth City (e.g., Delhi, India)")
    submit = st.button("Generate Analysis")

def call_gemini(prompt):
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        return f"Error: {response.status_code} - {response.text}"

if submit and city:
    try:
        geolocator = Nominatim(user_agent="astro_bot_2026")
        location = geolocator.geocode(city)
        
        if location:
            prompt = f"Vedic Astrology Expert: Analyze for {name}, Born {dob} at {tob} in {city}. Provide Lagna, Rashi, and life insights."
            with st.spinner("Connecting to Gemini 1.5..."):
                result = call_gemini(prompt)
                st.markdown(result)
        else:
            st.error("City not found.")
    except Exception as e:
        st.error(f"Error: {e}")

st.divider()
query = st.chat_input("Ask anything...")
if query:
    st.write(f"**You:** {query}")
    with st.spinner("Analyzing..."):
        st.write(call_gemini(query))
