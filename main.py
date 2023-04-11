import asyncio
import glob
import os
import re
import discord
from brains import thinking
from discord.ext import commands
from pytube import YouTube
from slugify import slugify
from youtubesearchpython import VideosSearch
from secrets import token

queues = {}
TOKEN = token
PREFIX = '!'  # You can choose any prefix you like

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


@bot.command(name='stop')
async def stop(ctx):
    voice_client = ctx.guild.voice_client

    if ctx.guild.id in queues:
        queues[ctx.guild.id].clear()

    if voice_client and voice_client.is_connected():
        if voice_client.is_playing():
            voice_client.stop()
            await asyncio.sleep(1)  # Wait for the player to stop before disconnecting and removing the file
            await voice_client.disconnect()
        else:
            await ctx.send("I'm not connected to a voice channel.")
            await mp3_cleaner(ctx)


@bot.command(name='play')
async def play(ctx, *, query: str):
    voice_channel = ctx.author.voice.channel
    if not voice_channel:
        await ctx.reply('You need to be in a voice channel to play music!')
        return

    url_pattern = re.compile(
        r"(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})"
    )
    is_url = url_pattern.match(query)
    if not is_url:
        # Search for YouTube link
        query = await search_youtube(query)

    # Add the song to the server-specific queue
    await add_to_queue(ctx.guild.id, query)

    voice_client = ctx.guild.voice_client
    if not voice_client or not voice_client.is_playing():
        await play_next(ctx)
    else:
        await ctx.reply(f'Added to queue: {query}')


async def play_next(ctx):
    if ctx.guild.id not in queues or not queues[ctx.guild.id]:
        await ctx.send("No more songs in the queue.")
        await mp3_cleaner(ctx)
        voice_client = ctx.guild.voice_client
        await voice_client.disconnect()
        return

    song_data = queues[ctx.guild.id].pop(0)
    url = song_data["url"]

    voice_channel = ctx.author.voice.channel
    voice_client = ctx.guild.voice_client
    if not voice_client:
        voice_client = await voice_channel.connect()

    try:
        player, filename = await YTDLSource.from_url(url, loop=bot.loop, guild_name=ctx.guild.name)
        while not os.path.isfile(filename):
            await asyncio.sleep(1)  # Wait for the file to be downloaded

        await ctx.reply(f'Now playing: {url}')

        def play_next_song(error):
            if error:
                print(f"An error occurred while playing the song: {error}")
            asyncio.run_coroutine_threadsafe(play_next(ctx), bot.loop)

        voice_client.play(player, after=play_next_song)

        while voice_client.is_playing():
            await asyncio.sleep(1)

    except Exception as e:
        print(e)
        await ctx.reply('https://tenor.com/view/mgs-metal-gear-fucky-wucky-uh-oh-gif-24704061')
        await voice_client.disconnect()

    await mp3_cleaner(ctx)


@bot.command(name='queue')
async def show_queue(ctx):
    voice_client = ctx.guild.voice_client
    if voice_client and voice_client.is_playing():
        current_song = voice_client.source.data["title"]
        message = f"Currently playing: {current_song}\n\n"
    else:
        message = ""

    if ctx.guild.id in queues and queues[ctx.guild.id]:
        queue = queues[ctx.guild.id]
        message += "Song queue:\n"
        for i, song_data in enumerate(queue, start=1):
            message += f"{i}. {song_data['title']}\n"
        await ctx.send(message)
    else:
        await ctx.send(f"{message}The song queue is empty.")


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data

    @classmethod
    async def from_url(cls, url, *, loop=None, guild_name=None):
        loop = loop or asyncio.get_event_loop()

        def pytube_extract_info():
            yt = YouTube(url)
            stream = yt.streams.filter(only_audio=True).first()
            sanitized_title = slugify(f"{yt.title}-{guild_name}-{yt.video_id}", max_length=100)
            # Append the server name to the filename
            filename = f"{sanitized_title}.mp3"
            if not stream:
                raise Exception("No audio stream found")
            if not stream.download(filename=filename):
                raise Exception("Unable to download audio stream")
            return {"url": filename, "title": yt.title, "id": yt.video_id}, filename

        data, filename = await loop.run_in_executor(None, pytube_extract_info)
        return cls(discord.FFmpegPCMAudio(filename), data=data), filename


async def add_to_queue(guild_id, url):
    yt = YouTube(url)
    song_data = {
        "title": yt.title,
        "url": url,
        "id": yt.video_id,
    }
    if guild_id in queues:
        queues[guild_id].append(song_data)
    else:
        queues[guild_id] = [song_data]


async def search_youtube(query):
    search_results = VideosSearch(query, limit=1).result()
    return search_results["result"][0]["link"]


async def mp3_cleaner(ctx):
    # Remove any MP3 files in the project directory
    for mp3_file in glob.glob("*.mp3"):
        try:
            os.remove(mp3_file)
        except PermissionError:
            await ctx.send(f"Couldn't remove {mp3_file} because it is being used by another process.")


bot.run(TOKEN)
