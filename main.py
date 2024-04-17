import json
import discord
from discord import app_commands

config = json.load(open('config.json'))

# https://github.com/Rapptz/discord.py/blob/v2.3.2/examples/app_commands/basic.py
class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):

        if config["debug"]["enabled"]:
            print("Copying commands to debug guild...")
            self.tree.copy_global_to(guild=discord.Object(id=config["debug"]["debug_guild_id"]))

        print("Syncing Commands...")
        await self.tree.sync()

client = MyClient()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.tree.command()
async def mailbox(interaction: discord.Interaction):
    await interaction.response.send_message("mailbox")

@client.tree.command()
async def register(interaction: discord.Interaction):
    await interaction.response.send_message("register")

@client.tree.command()
async def link(interaction: discord.Interaction):
    await interaction.response.send_message("link")

client.run(config["discord_bot_token"])
