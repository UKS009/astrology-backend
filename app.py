import streamlit as st
import google.generativeai as genai
from geopy.geocoders import Nominatim

# --- CONFIGURATION ---
# Note: Security ke liye apni key ko baad mein Streamlit Secrets mein daalna
API_KEY = "AIzaSyD1dIJValIcbBhuKDljpQRj6lxn0AsbN-g"
genai.configure(api_key=API_KEY)

# Use the latest stable model name
model = genai.GenerativeModel(model_name='gemini-1.5-flash')

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
        geolocator = Nominatim(user_agent="v-astro-agent")
        location = geolocator.geocode(city)
        
        if location:
            # AI logic for Calculation + Analysis
            prompt = f"""
            Act as a Vedic Astrology Expert. 
            User Details: Name: {name}, DOB: {dob}, Time: {tob}, City: {city} (Lat: {location.latitude}, Lon: {location.longitude}).
            
            1. Provide the approximate Lagna (Ascendant), Moon Sign (Rashi), and Nakshatra.
            2. Give a brief Vedic interpretation based on these positions.
            3. Give insights on Personality, Career, and Health.
            Format the output beautifully with headings and bullet points.
            """
            
            with st.spinner("AI is reading the stars..."):
                response = model.generate_content(prompt)
                st.markdown(response.text)
        else:
            st.error("City not found. Please type City name and Country (e.g., Mumbai, India).")
    except Exception as e:
        st.error(f"Something went wrong: {e}")

# --- CHAT ---
st.divider()
user_query = st.chat_input("Ask a follow-up question about your destiny...")
if user_query:
    st.write(f"**You:** {user_query}")
    with st.spinner("Consulting the cosmos..."):
        try:
            chat_response = model.generate_content(f"Based on Vedic Astrology principles, answer: {user_query}")
            st.write(f"**AI Astrologer:** {chat_response.text}")
        except Exception as e:
            st.error(f"Chat Error: {e}")
