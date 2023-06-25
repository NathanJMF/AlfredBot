import asyncio
import discord
from discord.ext import commands
from audio_system import voice_channel_check, YTDLSource, create_mp3_player
from helper import check_provided_song_query, download_mp3
from secrets import token

queues = {}
TOKEN = token
PREFIX = '`'

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
    # Handles the event where no query is provided by the user
    # TODO Add ability to insta kick people
    if not query:
        print("NO QUERY!")
        await ctx.send("Please provide either a song name or a YouTube URL")
        await ctx.send("https://tenor.com/view/dumbass-alert-roblox-arsenal-default-dance-ur-dumb-gif-19042964")
        return
    # Handles the event where user is not in a voice channel
    user_voice = ctx.author.voice
    user_voice_channel = await voice_channel_check(user_voice)
    if not user_voice_channel:
        return
    # Grabs the user's voice channel
    voice_channel = user_voice.channel
    voice_client = ctx.guild.voice_client
    if not voice_client:
        # Connect the bot to the voice channel if it is not already connected
        voice_client = await voice_channel.connect()
    # Will determine if the query is a URL, if not then it will search for and return the URL
    video_url = await check_provided_song_query(query)
    # Download the audio as a mp3 file
    player_helper_data, file_name = await download_mp3(video_url, ctx.guild.name)
    player = await create_mp3_player(file_name, player_helper_data)
    voice_client.play(player)
    await ctx.send(f"Now Playing:\n{video_url}")
    while voice_client.is_playing():
        await asyncio.sleep(1)
    await voice_client.disconnect()


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


bot.run(TOKEN)
