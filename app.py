import streamlit as st
import moviepy.editor as mp
import whisper
import os

st.set_page_config(page_title="Santier Captions AI", layout="centered")

st.title("🏗️ Santier Captions - Subtitrare Automată")
st.write("Încarcă clipul de pe șantier și lasă AI-ul să facă treaba.")

# 1. Încărcare fișier
uploaded_file = st.file_uploader("Alege un video (mp4, mov)", type=['mp4', 'mov', 'avi'])

if uploaded_file is not None:
    # Salvăm fișierul temporar
    with open("temp_video.mp4", "wb") as f:
        f.write(uploaded_file.read())
    
    st.video("temp_video.mp4")

    if st.button("Generează Subtitrări"):
        with st.spinner("👷 Se lucrează... Transcriem audio-ul..."):
            
            # 2. Încărcăm modelul Whisper (Base e rapid și bun pentru 1 min)
            model = whisper.load_model("base")
            
            # 3. Transcriem
            result = model.transcribe("temp_video.mp4", language="ro")
            
            st.success("Transcrierea e gata!")
            
            # Afișăm textul extras pentru verificare
            for segment in result['segments']:
                st.write(f"[{segment['start']}s]: {segment['text']}")

            # NOTĂ: Pentru a "lipi" subtitrarea pe video (Hardcode) 
            # e nevoie de librăria ImageMagick instalată pe server/PC.
            st.info("Următorul pas: Exportul video cu textul aplicat stilizat.")
