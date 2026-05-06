import discord
import os
import time
from python_aternos import Client

# --- 1. Load Environment Variables ---
TOKEN = os.getenv('DISCORD_TOKEN')
# We now use only the session cookie
ATERNOS_SESSION = os.getenv('ATERNOS_SESSION')

# --- 2. Initialize Aternos (Cookie Method) ---
at_client = Client()

# This bypasses the Cloudflare login screen entirely!
at_client.set_session(ATERNOS_SESSION) 

# Fetch servers
at_servers = at_client.list_servers()
myserv = at_servers[0]

# ... rest of your Discord bot code ...

# --- 3. Initialize Discord ---
intents = discord.Intents.default()
intents.message_content = True 
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Use .lower() so '?HELLO' or '?Hello' both work
    user_message = message.content.lower()
    username = str(message.author).split('#')[0]

    if message.channel.name == 'aternos-server':
        
        if user_message == '?hello':
            await message.channel.send(f'Hello {username}!')

        elif user_message == '?server_start':
            await message.channel.send("Attempting to start the server...")
            myserv.start()
            
            # Polling loop to check status
            while True:
                # Update server info from Aternos
                myserv.fetch() 
                if myserv.status == 'online':
                    break
                elif myserv.status == 'loading' or myserv.status == 'starting':
                    time.sleep(10) # Wait 10 seconds before checking again
                else:
                    # If it's still offline or in queue, keep waiting
                    time.sleep(10)
            
            await message.channel.send("Server is now alive!!! You can join in 2-3 minutes.")

        elif user_message == '?server_stop':
            myserv.stop()
            await message.channel.send('Server stop signal sent.')

# --- 4. Run the Bot ---
if TOKEN:
    client.run(TOKEN)
else:
    print("Error: DISCORD_TOKEN not found in environment variables.")
