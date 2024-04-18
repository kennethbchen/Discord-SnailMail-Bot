import json
import discord
import time
from discord import app_commands
from db_interface import SnailMailDBInterface

config = json.load(open('config.json'))

db = SnailMailDBInterface()


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


@client.tree.command(description="Register to start sending and receiving mail.")
async def register(interaction: discord.Interaction):

    if db.is_user_registered(interaction.user.name):
        await interaction.response.send_message("You are already registered.", ephemeral=True)
        return

    db.register_user(interaction.user.name)
    await interaction.response.send_message("Registered Successfully.", ephemeral=True)


@client.tree.command(description="Check your mailbox for unread mail.")
async def mailbox(interaction: discord.Interaction):

    if not db.is_user_registered(interaction.user.name):
        await interaction.response.send_message("You must register (/register) before you can view the mailbox.",
                                                ephemeral=True)
        return

    mail = db.get_unread_messages(interaction.user.name)

    response = "\n\n".join([":\n".join(msg) for msg in mail])
    await interaction.response.send_message(response, ephemeral=True)


@client.tree.command(description="Send mail to someone.")
@app_commands.describe(recipient="The user that will receive this message.", message="The message to send.")
async def send(interaction: discord.Interaction, recipient: str, message: str):

    if not db.is_user_registered(interaction.user.name):
        await interaction.response.send_message("You must register (/register) before you can send mail.", ephemeral=True)
        return

    if not db.is_user_registered(recipient):
        await interaction.response.send_message("Recipient user does not exist or is unregistered.", ephemeral=True)
        return

    if not message:
        await interaction.response.send_message("Message cannot be empty.", ephemeral=True)
        return

    day = 86400  # 86400 seconds in a day

    if config["debug"]["enabled"]:
        # shorten delivery time for debug
        day = 30

    sender_id = db.get_user_id_from_username(interaction.user.name)
    receiver_id = db.get_user_id_from_username(recipient)
    send_datetime = int(time.time())
    delivery_datetime = int(time.time() + 3 * day)  # 3 Days after send time
    body = message

    db.send_message(sender_id, receiver_id, send_datetime, delivery_datetime, body=body)

    await interaction.response.send_message("Mail Sent.", ephemeral=True)


client.run(config["discord_bot_token"])
