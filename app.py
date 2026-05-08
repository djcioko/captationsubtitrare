import streamlit as st
import moviepy.editor as mp
import whisper
import os

# Configurare pagină
st.set_page_config(page_title="Santier Captions AI", page_icon="🏗️")

st.title("🏗️ Santier Captions - Subtitrare Automată")
st.write("Încarcă filmarea de pe șantier și generăm transcrierea.")

# 1. Upload fișier
uploaded_file = st.file_uploader("Încarcă video (MP4, MOV)", type=['mp4', 'mov', 'avi'])

if uploaded_file is not None:
    # Salvăm fișierul pe disc pentru a putea fi citit de Whisper/MoviePy
    video_path = "temp_video.mp4"
    with open(video_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.video(video_path)

    if st.button("🚀 Începe procesarea"):
        with st.spinner("👷 Se încarcă modelul AI și se procesează audio..."):
            try:
                # 2. Transcrierea cu Whisper
                # Folosim modelul 'tiny' sau 'base' pentru viteză pe Streamlit Cloud
                model = whisper.load_model("base")
                result = model.transcribe(video_path, language="ro")
                
                st.success("✅ Transcrierea este gata!")
                
                # 3. Afișare text pe ecran
                st.subheader("📝 Text extras:")
                full_text = ""
                for segment in result['segments']:
                    timestamp = f"{int(segment['start'])}s - {int(segment['end'])}s"
                    st.write(f"**{timestamp}**: {segment['text']}")
                    full_text += f"{segment['text']} "
                
                # Opțiune de download text
                st.download_button("Descarcă Transcrierea (TXT)", full_text, file_name="subtitrare_santier.txt")

                st.info("💡 Pentru a lipi textul direct pe video cu stil 'influencer', avem nevoie de ImageMagick configurat. Momentan ai textul sincronizat!")

            except Exception as e:
                st.error(f"A apărut o eroare: {e}")

# Curățenie (opțional)
if os.path.exists("temp_video.mp4") and uploaded_file is None:
    os.remove("temp_video.mp4")
