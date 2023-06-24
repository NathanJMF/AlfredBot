import asyncio
import glob
import os
import re
import discord
import requests
from audio_system import voice_channel_check
# from brains import thinking
from discord.ext import commands
from pytube import YouTube
from slugify import slugify
from secrets import token

queues = {}
TOKEN = token
PREFIX = '`'  # You can choose any prefix you like

intents = discord.Intents.default()
intents.guilds = True
intents.presences = True
intents.members = True
intents.message_content = True
intents.messages = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user.name} is now online!')


@bot.event
async def on_message(message):
    if bot.user.mentioned_in(message):
        user = message.author
        response = f'Hello, {user.mention}!'
        await message.channel.send(response)
    await bot.process_commands(message)


@bot.command(name="play")
async def play(ctx, *, query=None):
    # TODO
    #  Handle no query
    #  Handle user not in VC
    #  Handle differentiation between url and title
    #  Retrieve MP3 of desired youtube content
    # Handles the event where no query is provided by the user
    if not query:
        print("NO QUERY!")
        await ctx.send("Please provide either a song name or a YouTube URL")
        await ctx.send("https://tenor.com/view/dumbass-alert-roblox-arsenal-default-dance-ur-dumb-gif-19042964")
        return
    user_voice = ctx.author.voice
    user_voice_channel = await voice_channel_check(user_voice)
    if not user_voice_channel:
        return
    output = f"GUILD: {ctx.guild}\n" \
             f"AUTHOR: {ctx.author}\n" \
             f"VOICE: {user_voice}\n" \
             f"VC: {user_voice_channel}\n" \
             f"MESSAGE: {ctx.message}\n" \
             f"QUERY: {query}"
    print(output)
    voice_channel = ctx.author.voice.channel
    print(ctx.guild.voice_client)
    voice_client = ctx.guild.voice_client
    if not voice_client:
        voice_client = await voice_channel.connect()
        await voice_client.disconnect()

    url = f"https://api.duckduckgo.com/?q={query}+youtube+!&format=json"
    repsonse = requests.get(url, allow_redirects=True)
    print(repsonse.url)
    await ctx.send(output)


@bot.command(name="stop")
async def stop(ctx):
    voice = ctx.author.voice
    voice_channel = await voice_channel_check(voice)
    if not voice_channel:
        return
    voice_client = ctx.guild.voice_client
    await voice_client.disconnect()


@bot.command(name="queue")
async def queue(ctx):
    pass


@bot.command(name="skip")
async def skip(ctx):
    pass

#

#
bot.run(TOKEN)
