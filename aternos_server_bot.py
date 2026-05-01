import discord
import os
import asyncio
from python_aternos import Client

# --- CONFIGURATION ---
TOKEN = os.environ.get('DISCORD_TOKEN')
ATERNOS_SESSION = os.environ.get('ATERNOS_SESSION')

# Initialize Discord Bot
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

def get_aternos_server():
    """Attempts to connect to Aternos and return the server object."""
    try:
        # Connect using the session cookie
        at = Client.from_cookies(ATERNOS_SESSION)
        
        # Get the list of servers
        at_servers = at.list_servers()
        
        if not at_servers:
            print("ERROR: No servers found on this Aternos account.")
            return None
            
        # Return the first server in the account
        return at_servers[0]
    except Exception as e:
        print(f"DEBUG: Aternos Connection Error: {e}")
        return None

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')

@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == client.user:
        return

    # Basic Hello Command
    if message.content.lower() == '?hello':
        await message.channel.send(f'Hello {message.author.display_name}! I am ready to manage the server.')

    # Server Start Command
    if message.content.lower() == '?server_start':
        await message.channel.send("⏳ Attempting to wake up the Aternos server...")
        
        # Try to connect
        myserv = get_aternos_server()
        
        if myserv:
            try:
                # Check current status first
                myserv.fetch() 
                if myserv.status == 'online':
                    await message.channel.send("✅ The server is already online!")
                elif myserv.status == 'starting':
                    await message.channel.send("⏳ The server is already starting up...")
                else:
                    # Actually start the server
                    myserv.start()
                    await message.channel.send("🚀 Start signal sent! I'll let you know if it needs confirmation.")
            except Exception as e:
                await message.channel.send(f"❌ Failed to start: `{str(e)}`")
        else:
            await message.channel.send("❌ Error: Could not connect to Aternos. Your session cookie may be invalid or blocked by Cloudflare.")

# Start the bot
if TOKEN:
    client.run(TOKEN)
else:
    print("ERROR: No DISCORD_TOKEN found in environment variables.")
