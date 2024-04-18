import json
import discord
from discord import app_commands
from db_interface import SnailMailDBInterface


config = json.load(open('config.json'))

db = SnailMailDBInterface()
print(db.is_user_registered("test0"))
exit()

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


@client.tree.command(description="Check your mailbox for unread mail.")
async def mailbox(interaction: discord.Interaction):
    await interaction.response.send_message("mailbox", ephemeral=True)


@client.tree.command(description="Register to start sending and receiving mail.")
async def register(interaction: discord.Interaction):
    await interaction.response.send_message("register", ephemeral=True)


@client.tree.command(description="Send mail to someone.")
async def send(interaction: discord.Interaction, user: str, message: str):
    await interaction.response.send_message("send", ephemeral=True)

client.run(config["discord_bot_token"])
