import discord
import os
from python_aternos import Client
import time
from flask import Flask
from threading import Thread

# --- KEEP ALIVE SECTION FOR RENDER ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run_web_server():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_web_server)
    t.start()
# -------------------------------------

# Environment Variables
TOKEN = os.environ.get("DISCORD_TOKEN")
# We use the session cookie now to bypass the login screen
ATERNOS_SESSION = os.environ.get("ATERNOS_SESSION")

client = discord.Client()

# Connect to Aternos using the Session Cookie
try:
    # This bypasses the username/password login page
    aternos = Client.from_cookies(ATERNOS_SESSION)
    atservers = aternos.servers
    myserv = atservers[0]
    print("Successfully connected to Aternos via Session!")
except Exception as e:
    print(f"Aternos Connection Error: {e}")
    myserv = None

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.channel.name == 'start-stop-server':
        user_message = message.content.lower()
        
        if user_message == '?hello':
            await message.channel.send(f'Hello {message.author.display_name}!')

        elif user_message == '?server_start':
            if myserv is None:
                await message.channel.send("Error: Bot isn't connected to Aternos. Check the session cookie!")
                return
                
            myserv.start()
            await message.channel.send("Attempting to start... checking status.")
            
            while True:
                ping = str(os.popen('mcstatus fridayssmpnew.aternos.me status | grep description').read())
                if "offline" in ping.lower():
                    time.sleep(5)
                else:
                    break
            
            await message.channel.send("Server is now alive!!! Join at: ||fridayssmpnew.aternos.me:62220||")

        elif user_message == '?server_stop':
            if myserv:
                myserv.stop()
                await message.channel.send('Server stopped.')
            else:
                await message.channel.send("Error: Not connected to Aternos.")

# Start the web server
keep_alive()

# Start the Discord Bot
client.run(TOKEN)
