import requests
import openai
import pandas as pd
from typing import Tuple

# Transcription audio via Whisper (local)
def transcribe_audio(file_path: str) -> str:
    import whisper
    model = whisper.load_model("base")
    result = model.transcribe(file_path)
    return result["text"]

# Génération image via ClipDrop API
def generate_image(prompt: str) -> str:
    url = "https://clipdrop-api.co/text-to-image/v1"
    headers = {"x-api-key": "VOTRE_API_KEY"}
    response = requests.post(url, json={"prompt": prompt}, headers=headers)
    image_url = response.json()["image_url"]
    return image_url

# Détection émotion via LLM
def detect_emotion(text: str) -> str:
    prompt = f"Analyse ce rêve et donne-moi son ambiance émotionnelle (heureux, stressant, neutre): {text}"
    openai.api_key = "VOTRE_API_KEY"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

# Historisation dans CSV
def save_dream(text: str, emotion: str, image_url: str):
    df = pd.read_csv("dreams_history.csv")
    new_row = {"Rêve": text, "Emotion": emotion, "Image": image_url}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv("dreams_history.csv", index=False)
