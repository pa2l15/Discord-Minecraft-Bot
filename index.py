import discord
from discord.ext import commands
import subprocess

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

opened_channel = None
server_running = False

@bot.event
async def on_ready():
    print(f'Bot started as {bot.user.name}')

@bot.command()
async def open(ctx):
    global opened_channel, server_running
    
    try:
        global server_running
        ruta_jar = r'Path to your .jar'
        comando = f'java -jar "{ruta_jar}"'
        await ctx.send('Starting server...')
        subprocess.Popen(comando, shell=True)
        await ctx.send('Minecraft server open!')
        
        opened_channel = ctx.channel
        server_running = True
        await update_bot_description()

    except Exception as e:
        await ctx.send(f'Failed to open the server: {e}')

async def update_bot_description():
    game_status = "Server open" if server_running else "Server closed"
    await bot.change_presence(activity=discord.Game(name=game_status))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)

@bot.command()
async def status(ctx):
    global server_running
    status_message = "Server is running" if server_running else "Server is not running"
    await ctx.send(status_message)

bot.run('YOUR_TOKEN')