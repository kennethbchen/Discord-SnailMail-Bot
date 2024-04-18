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
            return
        print("Syncing Commands...")
        await self.tree.sync()


client = MyClient()


@client.event
async def on_ready():

    print(f'Logged in as {client.user}')


@client.tree.command(description="Register to start sending and receiving letters.")
async def register(interaction: discord.Interaction):

    if db.is_user_registered(interaction.user.name):
        await interaction.response.send_message("You are already registered.", ephemeral=True)
        return

    db.register_user(interaction.user.name)
    await interaction.response.send_message("Registered successfully.", ephemeral=True)


@client.tree.command(description="Check your mailbox for new mail.")
async def mailbox(interaction: discord.Interaction):

    if not db.is_user_registered(interaction.user.name):
        await interaction.response.send_message("You must register (/register) before you can view the mailbox.", ephemeral=True)
        return

    mail = db.get_mailbox_summary(interaction.user.name)

    if len(mail) == 0:
        await interaction.response.send_message("Your mailbox is empty.", ephemeral=True)
        return

    # Format response
    response = "Your mailbox contains letters from:\n"
    response += "\n".join([" (".join([str(item) for item in row]) + ")" for row in mail])

    await interaction.response.send_message(response, ephemeral=True)


@client.tree.command(description="Read the oldest unread letter from a user.")
@app_commands.describe(from_who="The user whose letter you want to read.")
async def read(interaction: discord.Interaction, from_who: str):

    if not db.is_user_registered(interaction.user.name):
        await interaction.response.send_message("You must register (/register) before you can send or receive mail.", ephemeral=True)
        return

    if not db.is_user_registered(from_who):
        await interaction.response.send_message("User does not exist or is unregistered.", ephemeral=True)
        return

    letter = db.get_oldest_unread_message_from(interaction.user.name, from_who)

    if not letter:
        await interaction.response.send_message("You do not have any unread letters from this user.", ephemeral=True)
        return

    await interaction.response.send_message(f"Letter from {letter[0]}:\n```{letter[1]}```", ephemeral=True)


@client.tree.command(description="Send a letter to someone.")
@app_commands.describe(recipient="The user that will receive this letter.", message="The message to send.")
async def send(interaction: discord.Interaction, recipient: str, message: str):

    if not db.is_user_registered(interaction.user.name):
        await interaction.response.send_message("You must register (/register) before you can send a letter.", ephemeral=True)
        return

    if not db.is_user_registered(recipient):
        await interaction.response.send_message("Recipient user does not exist or is unregistered.", ephemeral=True)
        return

    if not message:
        await interaction.response.send_message("Message cannot be empty.", ephemeral=True)
        return

    day = 86400  # 86400 seconds in a day

    if config["debug"]["enabled"]:
        # shorten delivery time to one minute for debug
        day = 10

    sender_id = db.get_user_id_from_username(interaction.user.name)
    receiver_id = db.get_user_id_from_username(recipient)
    send_datetime = int(time.time())
    delivery_datetime = int(time.time() + 3 * day)  # 3 Days after send time
    body = message

    db.send_message(sender_id, receiver_id, send_datetime, delivery_datetime, body=body)

    await interaction.response.send_message("Letter sent.", ephemeral=True)


client.run(config["discord_bot_token"])
