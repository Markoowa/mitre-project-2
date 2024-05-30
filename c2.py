import discord
from discord.ext import commands
import os
import certifi

# Ensure the SSL_CERT_FILE environment variable is set correctly
os.environ['SSL_CERT_FILE'] = certifi.where()

intents = discord.Intents.default()
intents.message_content = True  # Enable the message content intent

bot = commands.Bot(command_prefix='!', intents=intents)

# Channel ID where the bot should read messages
TARGET_CHANNEL_ID = 11111111111111111111111111111  # Replace with your channel ID

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')

@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return
    
    # Check if the message is in the target channel
    if message.channel.id == TARGET_CHANNEL_ID:
        code = message.content
        
        # Create a local scope to execute the code
        local_scope = {}

        try:
            # Execute the code
            exec(code, {}, local_scope)
            # Optionally, send back the result if there is any output in local_scope
            result = local_scope.get('result', 'Code executed successfully')
            await message.channel.send(f'Result: {result}')
        except Exception as e:
            await message.channel.send(f'Error: {e}')

    # Process commands
    await bot.process_commands(message)

# Run the bot
bot.run('TOKENTOKENTOKENTOKENTOKENTOKENTOKENTOKENTOKENTOKENTOKENTOKENTOKENTOKENTOKEN')
