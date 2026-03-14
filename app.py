import streamlit as st
import requests
import json

# --- CONFIGURATION ---
# Apni key yahan daalein (Jo aapne pehle banayi thi)
API_KEY = "AIzaSyD1dIJValIcbBhuKDljpQRj6lxn0AsbN-g"

# Yeh model hamesha FREE hai, billing pop-up nahi aayega
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

st.set_page_config(page_title="Vedic AI", layout="centered")
st.title("✨ Final Try: Vedic AI")

# Simple Input
user_input = st.text_input("Apna sawal poochein (e.g. Meri kismat kaisi hai?):")
btn = st.button("Poochiye")

if btn and user_input:
    payload = {"contents": [{"parts": [{"text": user_input}]}]}
    headers = {'Content-Type': 'application/json'}
    
    with st.spinner("AI soch raha hai..."):
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
        
        if response.status_code == 200:
            ans = response.json()['candidates'][0]['content']['parts'][0]['text']
            st.success("Jawab mil gaya!")
            st.markdown(ans)
        else:
            # Agar abhi bhi error aaye toh asli wajah yahan dikhegi
            st.error(f"Error Code: {response.status_code}")
            st.write(response.text)
