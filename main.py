import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import requests
import json
from bot.sora import Sora

load_dotenv()

api_key = os.getenv("API_KEY")
token = os.getenv("DISCORD_TOKEN")

bot = Sora(token, api_key)
bot.run()