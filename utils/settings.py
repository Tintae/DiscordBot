import discord
import json
import yt_dlp
# Load the Discord bot token securely
with open("data/token.json", "r") as token_file:
    token_data = json.load(token_file)
    TOKEN = token_data['token']

# ... other settings in your 'settings.py' file

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '190',
    }],
    'defaultSearch': "ytsearch",
    'outtmpl': 'C:\\Users\\liam\\PycharmProjects\\DiscordBot\\audio\\%(title)s.%(ext)s',
}



