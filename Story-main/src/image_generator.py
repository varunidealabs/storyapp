import requests
import streamlit as st
import time

class ImageGenerator:
    def __init__(self):
        self.DALLE_API_ENDPOINT = st.secrets.get("DALLE_API_ENDPOINT", None)
        self.API_KEY = st.secrets.get("AZURE_OPENAI_API_KEY", None)

    def generate_image(self, genre: str, topic: str, keywords: str):
        """Generate an image using DALL·E with error handling and retry mechanism."""
        if not self.DALLE_API_ENDPOINT or not self.API_KEY:
            print("⚠️ Warning: Missing Azure DALL·E API credentials.")
            return None

        headers = {
            "Content-Type": "application/json",
            "api-key": self.API_KEY,
        }

        # Improved prompt to avoid common rejection issues
        prompt = (
            f"A detailed, high-quality {genre.lower()} scene inspired by the story topic: '{topic}'. "
            f"The scene should include {keywords}, rendered in a cinematic, visually stunning style."
        )

        payload = {
            "prompt": prompt,
            "model": "dall-e-3",
            "size": "1024x1024"
        }

        for attempt in range(2):  # Retry once if first attempt fails
            try:
                response = requests.post(self.DALLE_API_ENDPOINT, headers=headers, json=payload)
                response.raise_for_status()
                return response.json().get("data", [{}])[0].get("url")
            except requests.exceptions.HTTPError as e:
                print(f"⚠️ DALL·E Error (Attempt {attempt+1}): {e}")
                time.sleep(1)  # Short delay before retrying

        return None  # Return None if all attempts fail
