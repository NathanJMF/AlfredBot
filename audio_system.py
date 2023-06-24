async def voice_channel_check(user_voice):
    try:
        voice_channel = user_voice.channel
    except Exception as error:
        print(f"User made a request without being in a voice channel!\n{error}")
        voice_channel = None
    return voice_channel
