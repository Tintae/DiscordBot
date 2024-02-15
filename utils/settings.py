import discord
import json

# Load the Discord bot token securely
with open("data/token.json", "r") as token_file:
    token_data = json.load(token_file)
    TOKEN = token_data['token']

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '320',
    }],
    'defaultSearch': "ytsearch"
}

intents = discord.Intents.default()
intents.members = True
intents.typing = True
intents.presences = True
intents.message_content = True
