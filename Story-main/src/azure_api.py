import requests
import streamlit as st

class AzureOpenAI:
    def __init__(self):
        self.API_ENDPOINT = st.secrets["AZURE_OPENAI_API_ENDPOINT"]
        self.API_KEY = st.secrets["AZURE_OPENAI_API_KEY"]

    def generate_response(self, prompt: str, max_tokens: int = 300):
        """Send request to Azure OpenAI API"""
        headers = {
            "Content-Type": "application/json",
            "api-key": self.API_KEY,
        }
        payload = {
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": 0.7,
            "top_p": 1,
        }
        try:
            response = requests.post(self.API_ENDPOINT, headers=headers, json=payload)
            response.raise_for_status()
            return response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
        except requests.exceptions.RequestException as e:
            st.error(f"API Request failed: {e}")
            return None
