import discord
import os
import time
from python_aternos import Client

# --- 1. Load Environment Variables ---
# Ensure these are set in the Render "Environment" tab
TOKEN = os.getenv('DISCORD_TOKEN')
ATERNOS_SESSION = os.getenv('ATERNOS_SESSION')

print("--- System: Initializing Bot ---")

# --- 2. Initialize Aternos Client ---
try:
    print("System: Connecting to Aternos via Session Cookie...")
    at_client = Client()
    at_client.set_session(ATERNOS_SESSION)
    
    at_servers = at_client.list_servers()
    if not at_servers:
        print("Error: No servers found on this Aternos account.")
        exit(1)
        
    myserv = at_servers[0]
    print(f"System: Successfully linked to server: {myserv.address}")
except Exception as e:
    print(f"Error during Aternos Login: {e}")
    exit(1)

# --- 3. Initialize Discord Client ---
intents = discord.Intents.default()
intents.message_content = True 
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'System: Discord Bot is Live! Logged in as: {client.user}')
    print("--- System: Ready for Commands ---")

@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == client.user:
        return

    # Basic Logging for the Console
    username = str(message.author).split('#')[0]
    user_message = message.content.lower()
    channel = str(message.channel.name)
    
    # Only process commands in the specific channel
    if channel == 'aternos-server':
        print(f"User Log: {username} sent '{user_message}' in #{channel}")

        if user_message == '?hello':
            await message.channel.send(f'Hello {username}!')

        elif user_message == '?server_start':
            print(f"Action: Starting server {myserv.address}...")
            await message.channel.send("Attempting to start the server. I'll let you know when it's up!")
            
            try:
                myserv.start()
                
                # Polling loop to check status
                while True:
                    myserv.fetch() # Refresh server data from Aternos
                    print(f"Status Check: Server is currently {myserv.status}")
                    
                    if myserv.status == 'online':
                        break
                    elif myserv.status in ['loading', 'starting']:
                        time.sleep(15) # Wait 15 seconds between checks
                    else:
                        # Handles 'offline' or 'queue'
                        time.sleep(15)
                
                await message.channel.send(f"Server is now **LIVE**! 🚀\nAddress: ||{myserv.address}:{myserv.port}||")
                print("Action: Server start sequence complete.")
                
            except Exception as e:
                print(f"Error during server start: {e}")
                await message.channel.send("Failed to start the server. Check my logs for details.")

        elif user_message == '?server_stop':
            print("Action: Stopping server...")
            myserv.stop()
            await message.channel.send('Server stop signal sent. 🛑')

# --- 4. Launch Bot ---
if TOKEN:
    print("System: Attempting to connect to Discord...")
    client.run(TOKEN)
else:
    print("Error: DISCORD_TOKEN not found in Environment Variables.")
    exit(1)
