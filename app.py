import streamlit as st
import google.generativeai as genai
from geopy.geocoders import Nominatim

# --- CONFIGURATION ---
API_KEY = "AIzaSyD1dIJValIcbBhuKDljpQRj6lxn0AsbN-g"

# Version error se bachne ke liye ye setup
try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Setup Error: {e}")

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
        # User agent change kiya taaki blocking na ho
        geolocator = Nominatim(user_agent="my_astro_app_v1")
        location = geolocator.geocode(city)
        
        if location:
            prompt = f"""
            Act as a Vedic Astrology Expert. 
            User Details: Name: {name}, DOB: {dob}, Time: {tob}, City: {city} (Lat: {location.latitude}, Lon: {location.longitude}).
            
            1. Calculate the approximate Lagna (Ascendant), Moon Sign (Rashi), and Nakshatra.
            2. Provide a brief Vedic interpretation.
            3. Give insights on Personality, Career, and Health.
            Format beautifully with bullet points.
            """
            
            with st.spinner("AI is calculating planetary positions..."):
                # Normal call without transport='rest' for stability
                response = model.generate_content(prompt)
                st.markdown(response.text)
        else:
            st.error("City not found. Please try again with 'City, Country'.")
    except Exception as e:
        # Agar model phir bhi na mile toh manual error handle
        if "404" in str(e):
            st.error("Model Error: Gemini is updating. Please try again in 2 minutes.")
        else:
            st.error(f"Something went wrong: {e}")

# --- CHAT ---
st.divider()
user_query = st.chat_input("Ask a follow-up question...")
if user_query:
    st.write(f"**You:** {user_query}")
    with st.spinner("Thinking..."):
        try:
            chat_response = model.generate_content(f"Answer this as an astrologer: {user_query}")
            st.write(f"**AI Astrologer:** {chat_response.text}")
        except:
            st.error("AI is busy, please wait.")
