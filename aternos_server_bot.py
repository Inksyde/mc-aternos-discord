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
    # Render uses port 8080 or 10000 usually; 0.0.0.0 makes it public
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_web_server)
    t.start()
# -------------------------------------

# Environment Variables
TOKEN = os.environ.get("DISCORD_TOKEN")
aternos_user = os.getenv('ATERNOS_USER')
aternos_pass = os.getenv('ATERNOS_PASS')

client = discord.Client()

# Connect to Aternos
aternos = Client(aternos_user, password=aternos_pass)
atservers = aternos.servers
myserv = atservers[0]

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    
    if message.author == client.user:
        return

    # Check for the specific channel
    if message.channel.name == 'start-stop-server':
        
        if user_message.lower() == '?hello':
            await message.channel.send(f'Hello {username}!')

        elif user_message.lower() == '?server_start':
            myserv.start()
            await message.channel.send("Attempting to start... checking status.")
            
            # Note: This while loop might block the bot for a long time. 
            # In a busy bot, you'd use an async loop, but for a private server this works.
            while True:
                # Optimized ping check
                ping = str(os.popen('mcstatus fridayssmpnew.aternos.me status | grep description').read())
                if "offline" in ping.lower():
                    time.sleep(5) # Increased sleep to avoid spamming the shell
                else:
                    break
            
            await message.channel.send("Server is now alive!!! Join at: ||fridayssmpnew.aternos.me:62220||")

        elif user_message.lower() == '?server_stop':
            myserv.stop()
            await message.channel.send(f'Server stopped.')

# Start the web server first
keep_alive()

# Start the Discord Bot
client.run(TOKEN)
