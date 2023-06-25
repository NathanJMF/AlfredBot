import asyncio
import discord
from pytube import YouTube
from slugify import slugify


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


async def voice_channel_check(user_voice):
    try:
        voice_channel = user_voice.channel
    except Exception as error:
        print(f"User made a request without being in a voice channel!\n{error}")
        voice_channel = None
    return voice_channel


async def create_mp3_player(file_name, player_helper_data):
    return player_system(discord.FFmpegPCMAudio(file_name), data=player_helper_data)


class player_system(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
