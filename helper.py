import re
import requests
from pytube import YouTube
from slugify import slugify


async def check_provided_song_query(query):
    url_pattern = re.compile(
        r"(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})"
    )
    is_url = url_pattern.match(query)
    video_url = query
    if not is_url:
        video_url = await search_youtube(query)
    return video_url


async def search_youtube(query):
    url = f"https://api.duckduckgo.com/?q={query}+youtube+!&format=json"
    response = requests.get(url, allow_redirects=True)
    return response.url


async def download_mp3(video_url, guild_name):
    yt = YouTube(video_url)
    stream = yt.streams.filter(only_audio=True).first()
    sanitized_title = slugify(f"{yt.title}-{guild_name}-{yt.video_id}", max_length=100)
    # Append the server name to the filename
    filename = f"{sanitized_title}.mp3"
    if not stream:
        raise Exception("No audio stream found")
    if not stream.download(filename=filename):
        raise Exception("Unable to download audio stream")
    return {"url": filename, "title": yt.title, "id": yt.video_id}, filename


async def add_song_to_queue():
    pass
