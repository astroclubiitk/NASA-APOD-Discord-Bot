## Author : Gurbaaz Singh Nandra (http://gurbaaz.me)

import discord
import os

from discord import channel
from utils import *
from dotenv import load_dotenv

load_dotenv()


client = discord.Client()
nasa_client = NasaApod()


@client.event
async def on_ready():
    print(f"{client.user} is now online")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    message_content = message.content.lower()

    if message.content.startswith(f"$help"):
        await message.channel.send(
            """Hello there! I\'m your NASA APOD bot.\nI fetch information from NASA APOD site, where each day a different image or photograph of our universe is featured, along with a brief explanation written by a professional astronomer."""
        )

    if message.content.startswith(f"$fetch"):
        (
            date,
            title,
            credit,
            credit_link,
            filename,
            status,
        ) = nasa_client.collect_info()

        await message.channel.send(
            f"""**Astronomy Picture of the Day - NASA** :camera_with_flash: 
**Date** - {date}
**Title** - {title}
**Image Credits** - {credit} [{credit_link}]"""
        )
        status = False
        if status:
            await message.channel.send(file=discord.File(filename))
        else:
            await message.channel.send("Could *not* load image!")
            await message.channel.send(file=discord.File("error.jpg"))


client.run(os.getenv("TOKEN"))
