import streamlit as st
import google.generativeai as genai
from geopy.geocoders import Nominatim

# --- CONFIGURATION ---
API_KEY = "AIzaSyAjmm39t-FnC4Moq8gC2y47woxEFon0Uuw"
genai.configure(api_key=API_KEY, transport='rest')
model = genai.GenerativeModel(model_name='gemini-pro')

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

if submit and city:
    try:
        geolocator = Nominatim(user_agent="v-astro")
        location = geolocator.geocode(city)
        
        if location:
            # AI logic for Calculation + Analysis
            prompt = f"""
            Act as a Vedic Astrology Expert. 
            User Details: Name: {name}, DOB: {dob}, Time: {tob}, City: {city} (Lat: {location.latitude}, Lon: {location.longitude}).
            
            1. Calculate the Lagna (Ascendant), Moon Sign (Rashi), and Nakshatra for this data.
            2. Provide a brief analysis of the current Mahadasha based on general transit.
            3. Give insights on Personality, Career, and Health.
            Format the output beautifully with headings and bullet points.
            """
            
            with st.spinner("AI is calculating planetary positions..."):
                response = model.generate_content(prompt)
                st.markdown(response.text)
        else:
            st.error("City not found.")
    except Exception as e:
        st.error(f"Something went wrong: {e}")

# --- CHAT ---
st.divider()
user_query = st.chat_input("Ask a follow-up question...")
if user_query:
    st.write(f"**You:** {user_query}")
    chat_response = model.generate_content(f"Answer this as an astrologer: {user_query}")
    st.write(f"**AI Astrologer:** {chat_response.text}")
