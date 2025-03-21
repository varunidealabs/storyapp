import requests
import streamlit as st
import time
import os

class TTSGenerator:
    def __init__(self):
        self.TTS_ENDPOINT = st.secrets.get("AZURE_TTS_ENDPOINT", None)
        self.API_KEY = st.secrets.get("AZURE_OPENAI_API_KEY", None)

        if not self.TTS_ENDPOINT or not self.API_KEY:
            print("⚠️ Warning: Missing Azure TTS API credentials. Check `secrets.toml`.")

        # Ensure `output_audio/` directory exists
        self.audio_dir = "output_audio"
        os.makedirs(self.audio_dir, exist_ok=True)

    def generate_speech(self, text):
        """Convert story text to speech using Azure OpenAI TTS API and return the audio file path."""
        if not self.TTS_ENDPOINT or not self.API_KEY:
            return None  # Silent failure if missing keys

        headers = {
            "Content-Type": "application/json",
            "api-key": self.API_KEY,
        }

        payload = {
            "model": "tts-1",
            "input": text,
            "voice": "alloy",
            "response_format": "mp3",
            "speed": 1.0
        }

        try:
            response = requests.post(self.TTS_ENDPOINT, headers=headers, json=payload)
            response.raise_for_status()
            
            # Save audio file in `output_audio/` folder
            audio_filename = os.path.join(self.audio_dir, f"story_{int(time.time())}.mp3")
            with open(audio_filename, "wb") as audio_file:
                audio_file.write(response.content)

            return audio_filename

        except requests.exceptions.RequestException as e:
            print(f"⚠️ Azure OpenAI TTS Error: {e}")  # Silent failure
            return None
