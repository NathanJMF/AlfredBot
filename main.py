import discord
from discord.ext import commands

from brains import thinking
from secrets import token

TOKEN = token  # Replace this with your bots token
PREFIX = '!'  # You can choose any prefix you like

intents = discord.Intents.default()
intents.guilds = True
intents.presences = True
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user.name} is now online!')


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    mentioned = discord.utils.get(message.mentions, id=bot.user.id)
    prompt = message.content[len(f"<@!{bot.user.id}>"):]
    result = await thinking(prompt)
    result = result[len(prompt)+1:]
    if mentioned:
        await message.channel.send(f'{result}')
    else:
        await bot.process_commands(message)


bot.run(TOKEN)
