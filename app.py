import streamlit as st
import requests
import json
from geopy.geocoders import Nominatim

# --- 1. CONFIGURATION ---
# Apni Google AI Studio wali API Key yahan paste karein
API_KEY = "AIzaSyD1dIJValIcbBhuKDljpQRj6lxn0AsbN-g"

# Purani line: API_URL = f".../gemini-1.5-flash:generateContent?..."
# Nayi line ye try karein (jo standard hai):
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"

st.set_page_config(page_title="Vedic AI Astrologer", layout="wide", page_icon="✨")

# --- 2. UI HEADER ---
st.title("✨ Agentic Vedic Astrologer")
st.markdown("---")

# --- 3. SIDEBAR INPUTS ---
with st.sidebar:
    st.header("🌙 Birth Details")
    name = st.text_input("Name", placeholder="Enter your name")
    dob = st.date_input("Date of Birth")
    tob = st.time_input("Time of Birth")
    city = st.text_input("Birth City", placeholder="e.g. Delhi, India")
    submit = st.button("Generate Kundali Analysis")
    st.info("Note: This uses AI to calculate approximate planetary positions.")

# --- 4. CORE LOGIC ---
def call_gemini(prompt):
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"❌ Server Error: {response.status_code}\n{response.text}"
    except Exception as e:
        return f"❌ Connection Error: {str(e)}"

if submit and city:
    try:
        # Step A: Get Coordinates
        geolocator = Nominatim(user_agent="astro_app_v1")
        location = geolocator.geocode(city)
        
        if location:
            lat, lon = location.latitude, location.longitude
            
            # Step B: Create Prompt
            astro_prompt = f"""
            Act as a highly experienced Vedic Astrologer. 
            Analyze the following birth details:
            Name: {name}
            Date: {dob}
            Time: {tob}
            Location: {city} (Lat: {lat}, Lon: {lon})

            Please provide:
            1. **Basic Details**: Approximate Lagna (Ascendant), Moon Sign (Rashi), and Nakshatra.
            2. **Personality**: 3 key personality traits based on the Moon sign.
            3. **Career & Wealth**: Insights into professional life.
            4. **Health & Remedies**: One practical Vedic remedy (Upaya).

            Format the response using beautiful Markdown with headings and emojis.
            """
            
            # Step C: Call AI
            with st.spinner("🌌 Reading the cosmic alignments..."):
                analysis = call_gemini(astro_prompt)
                st.markdown(analysis)
        else:
            st.error("City not found! Please enter 'City, Country' (e.g., Mumbai, India).")
            
    except Exception as e:
        st.error(f"Something went wrong: {e}")

# --- 5. CHAT SECTION ---
st.markdown("---")
st.subheader("💬 Ask a Follow-up Question")
user_query = st.chat_input("Ask about marriage, career, or luck...")

if user_query:
    st.write(f"**You:** {user_query}")
    with st.spinner("Consulting the stars..."):
        chat_prompt = f"As a Vedic Astrologer, answer this: {user_query}"
        response = call_gemini(chat_prompt)
        st.write(f"**AI Astrologer:** {response}")
