## Author : Gurbaaz Singh Nandra (http://gurbaaz.me)
## Updated: Adit Jain (https://github.com/jadit19)

import os
import discord
from discord.ext import tasks
from dotenv import load_dotenv

from scrapper import NasaApod
from utils import *

load_dotenv()
APOD_TOKEN = os.getenv('APOD_TOKEN')
APOD_CHANNEL_ID = int(os.getenv('APOD_CHANNEL_ID'))

intents = discord.Intents.default()
intents.message_content = True
intents.presences = True
intents.guild_messages = True

client = discord.Client(intents=intents)
bot = NasaApod()

async def fetcher(ctx, url=bot.daily_url, msg=None):
    print("Fetcher function called!")
    (date, title, explanation, credit, credit_link, resource_link, status, tomorrows_picture, media_type, is_linkable_video) = bot.collect_info("360p", url)
    send_str = f"""**Astronomy Picture of the Day - NASA** :camera_with_flash: [https://apod.nasa.gov/apod/astropix.html]
**Date** - {date}
**Title** - {title.title()}
**{media_type} Credits** - {credit} [{credit_link}]
**Explanation** - {explanation}
**Tomorrow's picture** - {tomorrows_picture.title()}"""
    
    if msg == None:
        await ctx.send(send_str)
    else:
        await msg.reply(send_str)
    if is_linkable_video:
        if "youtu" in resource_link:
            id = resource_link.split("/")[-1]
            await ctx.send(f"https://youtu.be/{id}")
        else:
            await ctx.send(f"{resource_link}")
    elif status:
        await ctx.send(file=discord.File(resource_link))
    else:
        await ctx.send(f"Could **not** load {media_type.lower()}!")
        await ctx.send(file=discord.File("assets/error.jpg"))
        
@tasks.loop(hours=24)
async def apod_display():
    # print("=" * 40)
    # print("⏰ Daily cycle repeats!")
    ctx = client.get_channel(APOD_CHANNEL_ID)
    await fetcher(ctx, bot.daily_url)
    # print("=" * 40)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    activity = discord.Game(bot.prefix + " help")
    await client.change_presence(
        status = discord.Status.online,
        activity = activity
    )
    apod_display.start()
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith(bot.prefix):
        msg = message.content.split(" ")[1:]
        if msg[0] == 'help':
            help_embed = discord.Embed(
                title = 'NASA APOD Help',
                description = introduction + "\n\n" + help_content,
                color = 0x11213f
            )
            help_embed.add_field(name="--help", value="To open this menu")
            help_embed.add_field(name="dd/mm/yy", value="To show the APOD at that day (January 1, 2015 onwards)")
            await message.reply(embed=help_embed)
        elif len(msg[0].split("/")) == 3:
            date_numbers = msg[0].split("/")
            if len(date_numbers[0]) == 1:
                date_numbers[0] = "0" + date_numbers[0]
            if len(date_numbers[1]) == 1:
                date_numbers[1] = "0" + date_numbers[1]
            date_numbers[2] = str(int(date_numbers[2]) % 100)
            extend_url = "ap" + date_numbers[2]+date_numbers[1]+date_numbers[0] + ".html"
            if check_validity(bot.daily_url + extend_url):
                await fetcher(message.channel, url=bot.daily_url+extend_url, msg=message)
            else:
                not_found_embed = discord.Embed(
                    title='Not Found',
                    description = f'APOD on {msg[0]} was not found. Please check the date and try again.',
                    color = 0x11213f
                )
                await message.reply(embed=not_found_embed)
                
client.run(APOD_TOKEN)