import json
import discord
from discord.ext import commands

config = json.load(open('config.json'))

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents, client=discord.Client(intents=intents))

@bot.event
async def on_ready():

    print("Syncing bot commands...")
    commands = await bot.tree.sync()
    print("Synced Commands:", commands)

    print(f'Logged in as {bot.user}')

@bot.hybrid_command()
async def test(ctx):
    await ctx.send("test command")

bot.run(config["discord_bot_token"])
