import streamlit as st
import requests
import json
from geopy.geocoders import Nominatim

# --- CONFIGURATION ---
# Apni Nayi API Key yahan daalein
API_KEY = "AIzaSyD1dIJValIcbBhuKDljpQRj6lxn0AsbN-g"

# Hamare pas 2 option hain, agar pehla fail ho toh dusra chale
MODELS = ["gemini-1.5-flash", "gemini-pro"]

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

def call_gemini_direct(prompt):
    # Hum bari-bari models try karenge
    for model_name in MODELS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={API_KEY}"
        headers = {'Content-Type': 'application/json'}
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        
        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            if response.status_code == 200:
                return response.json()['candidates'][0]['content']['parts'][0]['text']
        except:
            continue
            
    return "Error: Dono models (Flash aur Pro) ne jawab nahi diya. Check karein ki API Key 'Enabled' hai ya nahi."

if submit and city:
    try:
        geolocator = Nominatim(user_agent="astro_v3_agent")
        location = geolocator.geocode(city)
        
        if location:
            prompt = f"""
            Act as a professional Vedic Astrologer. 
            User: {name}, Date: {dob}, Time: {tob}, City: {city}.
            1. Calculate Lagna, Rashi and Nakshatra.
            2. Give 3 points for Personality, 3 for Career, and 1 important remedy.
            Keep it clear and formatted with Markdown.
            """
            with st.spinner(f"Consulting the stars via {MODELS[0]}..."):
                result = call_gemini_direct(prompt)
                st.markdown(result)
        else:
            st.error("City nahi mili. Please 'City, Country' format try karein.")
    except Exception as e:
        st.error(f"Kuch galat hua: {e}")

st.divider()
query = st.chat_input("Apni kismat ke baare mein poochiye...")
if query:
    st.write(f"**You:** {query}")
    with st.spinner("Analyzing..."):
        st.write(call_gemini_direct(query))
