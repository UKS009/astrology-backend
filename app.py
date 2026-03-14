import streamlit as st
import google.generativeai as genai
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from geopy.geocoders import Nominatim

# --- CONFIGURATION ---
API_KEY = "AIzaSyAjmm39t-FnC4Moq8gC2y47woxEFon0Uuw"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Vedic AI Astrologer", layout="wide")

# --- UI INTERFACE ---
st.title("✨ Agentic Vedic Astrologer")
st.subheader("Get precise Kundali calculations & AI insights")

with st.sidebar:
    st.header("Birth Details")
    name = st.text_input("Name")
    dob = st.date_input("Date of Birth")
    tob = st.time_input("Time of Birth")
    city = st.text_input("Birth City (e.g., Delhi, India)")
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    submit = st.button("Generate Kundali")

# --- CALCULATIONS ---
if submit and city:
    try:
        # Get Lat/Long
        geolocator = Nominatim(user_agent="v-astro")
        location = geolocator.geocode(city)
        
        if location:
            lat, lon = location.latitude, location.longitude
            
            # Vedic Chart Setup
            date_str = dob.strftime('%Y/%m/%d')
            time_str = tob.strftime('%H:%M')
            dt = Datetime(date_str, time_str, '+05:30') # Change offset if needed
            pos = GeoPos(lat, lon)
            chart = Chart(dt, pos)
            
            # Extract Data
            sun = chart.get(chart.SUN)
            moon = chart.get(chart.MOON)
            lagna = chart.get(chart.ASC)
            
            # Display Table
            st.write(f"### 🔮 Kundali for {name}")
            col1, col2, col3 = st.columns(3)
            col1.metric("Lagna (Ascendant)", f"{lagna.sign} {round(lagna.lon, 2)}°")
            col2.metric("Sun Sign", f"{sun.sign}")
            col3.metric("Moon Sign (Rashi)", f"{moon.sign}")
            
            # AI Analysis Prompt
            prompt = f"""
            Act as a professional Vedic Astrologer. Analyze this chart:
            - Name: {name}
            - Lagna: {lagna.sign} at {lagna.lon} degrees
            - Sun: In {sun.sign}
            - Moon: In {moon.sign}
            Provide a deep life analysis including Personality, Career, and Health. 
            Use a traditional yet encouraging tone.
            """
            
            with st.spinner("AI is reading your stars..."):
                response = model.generate_content(prompt)
                st.markdown("### 📜 AI Interpretation")
                st.write(response.text)
        else:
            st.error("City not found. Please try again.")
    except Exception as e:
        st.error(f"Error: {e}")

# --- CHAT INTERFACE ---
st.divider()
st.markdown("### 💬 Ask Follow-up Questions")
user_query = st.chat_input("Ask about your career, marriage, or health...")
if user_query:
    st.write(f"**You:** {user_query}")
    with st.spinner("Thinking..."):
        chat_response = model.generate_content(f"Based on Vedic Astrology, answer: {user_query}")
        st.write(f"**Astrologer:** {chat_response.text}")
