## Author : Gurbaaz Singh Nandra (http://gurbaaz.me)

import discord
from discord.ext import commands, tasks
import os

from utils import *
from dotenv import load_dotenv

load_dotenv()


bot = commands.Bot("$")
nasa_client = NasaApod()


@tasks.loop(hours=24)
async def called_once_a_day():
    ctx = bot.get_channel(int(os.getenv("TARGET_CHANNEL_ID")))
    (
        date,
        title,
        credit,
        credit_link,
        resource_link,
        status,
        tomorrows_picture,
        media_type,
        is_youtube_video,
    ) = nasa_client.collect_info()

    await ctx.send(
        f"""**Astronomy Picture of the Day - NASA** :camera_with_flash: [https://apod.nasa.gov/apod/astropix.html]
**Date** - {date}
**Title** - {title}
**{media_type} Credits** - {credit} [{credit_link}]
**Tomorrow's picture** - {tomorrows_picture}"""
    )

    if is_youtube_video:
        await ctx.send("{resource_link}")
    elif status:
        await ctx.send(file=discord.File(resource_link))
    else:
        await ctx.send("Could **not** load image!")
        await ctx.send(file=discord.File("error.jpg"))


@called_once_a_day.before_loop
async def before():
    await bot.wait_until_ready()
    print("Finished waiting ⌛")


@bot.event
async def on_ready():
    print(f"{bot.user} is now online 🚀")


@bot.command()
async def author(ctx):
    """Author of the project"""
    await ctx.send(
        """Gurbaaz [http://gurbaaz.me], as part of an initiative of Astronomy Club IIT Kanpur [https://astroclubiitk.github.io/]"""
    )


@bot.command()
async def fetch(ctx):
    """Fetches the NASA Astrophotography of the Day"""
    (
        date,
        title,
        credit,
        credit_link,
        resource_link,
        status,
        tomorrows_picture,
        media_type,
        is_youtube_video,
    ) = nasa_client.collect_info()

    await ctx.send(
        f"""**Astronomy Picture of the Day - NASA** :camera_with_flash: [https://apod.nasa.gov/apod/astropix.html]
**Date** - {date}
**Title** - {title}
**{media_type} Credits** - {credit} [{credit_link}]
**Tomorrow's picture** - {tomorrows_picture}"""
    )

    if is_youtube_video:
        await ctx.send("{resource_link}")
    elif status:
        await ctx.send(file=discord.File(resource_link))
    else:
        await ctx.send("Could **not** load image!")
        await ctx.send(file=discord.File("error.jpg"))


called_once_a_day.start()
bot.run(os.getenv("TOKEN"))
