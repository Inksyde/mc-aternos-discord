import discord
import os
import time
from python_aternos import Client

# --- 1. Load Environment Variables ---
TOKEN = os.getenv('DISCORD_TOKEN')
ATERNOS_SESSION = os.getenv('ATERNOS_SESSION')

print("--- System: Initializing Bot ---")

# --- 2. Initialize Aternos Client (v3.0.0 fix) ---
try:
    print("System: Connecting to Aternos via Session Cookie...")
    
    # Correct way for v3.0.0 to handle sessions
    at_client = Client()
    at_client.atconn.session.cookies.set('ATERNOS_SESSION', ATERNOS_SESSION, domain='aternos.org')

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
    print("--- System: Monitoring #aternos-server ---")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    username = str(message.author).split('#')[0]
    user_message = message.content.lower().strip()
    channel = str(message.channel.name)
    
    if channel == 'aternos-server':
        print(f"User Log: {username} sent '{user_message}'")

        if user_message == '?hello':
            await message.channel.send(f'Hello {username}!')

        elif user_message == '?server_start':
            print(f"Action: Starting server {myserv.address}...")
            await message.channel.send("Attempting to start the server. I'll let you know when it's up!")
            
            try:
                myserv.start()
                while True:
                    myserv.fetch() 
                    print(f"Status Check: {myserv.status}")
                    if myserv.status == 'online':
                        break
                    time.sleep(15) 
                
                await message.channel.send(f"Server is now **LIVE**! 🚀\nAddress: ||{myserv.address}:{myserv.port}||")
                
            except Exception as e:
                print(f"Error during server start: {e}")
                await message.channel.send("Failed to start. Check logs.")

        elif user_message == '?server_stop':
            print("Action: Stopping server...")
            myserv.stop()
            await message.channel.send('Server stop signal sent. 🛑')

if TOKEN:
    print("System: Attempting to connect to Discord...")
    client.run(TOKEN)
else:
    print("Error: DISCORD_TOKEN not found.")
    exit(1)
