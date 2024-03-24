import discord
from discord.ext import commands
import requests
import json

class OpenRouterAPI:
    BASE_URL = "https://openrouter.ai/api/v1"

    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def chat_completion(self, messages, model):
        url = f"{self.BASE_URL}/chat/completions"
        data = {
            "model": model,
            "messages": messages
        }
        response = requests.post(url, headers=self.headers, data=json.dumps(data))
        return response

    def get_models(self):
        url = f"{self.BASE_URL}/models"
        response = requests.get(url, headers=self.headers)
        return response