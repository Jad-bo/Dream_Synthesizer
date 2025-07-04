import streamlit as st
from dream_utils import transcribe_audio, generate_image, detect_emotion, save_dream
import pandas as pd

st.set_page_config(page_title="Synthétiseur de Rêves")

st.title("🌙 Synthétiseur de Rêves")
st.write("Racontez votre rêve et voyez-le se transformer en image.")

# Upload
audio_file = st.file_uploader("🎙️ Uploadez votre rêve (WAV/MP3)", type=["wav", "mp3"])

if audio_file:
    with open("temp_audio.wav", "wb") as f:
        f.write(audio_file.read())
    st.audio("temp_audio.wav")

    if st.button("Transcrire et générer"):
        with st.spinner("Transcription en cours..."):
            texte_reve = transcribe_audio("temp_audio.wav")
        st.subheader("📝 Votre rêve transcrit :")
        st.write(texte_reve)

        with st.spinner("Analyse de l'ambiance..."):
            emotion = detect_emotion(texte_reve)
        st.success(f"Ambiance détectée : **{emotion}**")

        with st.spinner("Génération de l'image..."):
            image_url = generate_image(texte_reve)
        st.image(image_url, caption="Interprétation du rêve")

        save_dream(texte_reve, emotion, image_url)

st.subheader("📜 Historique des rêves")
try:
    df = pd.read_csv("dreams_history.csv")
    st.dataframe(df)
except FileNotFoundError:
    st.write("Aucun rêve enregistré pour le moment.")
