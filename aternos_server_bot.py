import discord
import os
import time
from python_aternos import Client

# 1. Load Secrets
TOKEN = os.getenv('DISCORD_TOKEN')
ATERNOS_SESSION = os.getenv('ATERNOS_SESSION')

print("Starting bot...")

# 2. Initialize Aternos
try:
    at_client = Client()
    at_client.set_session(ATERNOS_SESSION)
    at_servers = at_client.list_servers()
    myserv = at_servers[0]
    print(f"Connected to Aternos: {myserv.address}")
except Exception as e:
    print(f"Aternos Login Failed: {e}")
    exit(1) # This tells Render the app crashed intentionally

# 3. Initialize Discord
intents = discord.Intents.default()
intents.message_content = True 
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Discord Bot is Live as {client.user}')

# ... (Keep your on_message logic here) ...

if TOKEN:
    client.run(TOKEN)
else:
    print("Error: DISCORD_TOKEN is missing!")
