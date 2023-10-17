import aiohttp
import discord
from discord.ext import commands
from secrets import token

queues = {}
TOKEN = token
PREFIX = '!'
model_to_use = "alfred_brain.bin"
model = "test"
intents = discord.Intents.default()
intents.guilds = True
intents.presences = True
intents.members = True
intents.message_content = True
intents.messages = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)
system_template = ("Conversation between Batman and the digital resurrection of Alfred Pennyworth who is in eternal "
                   "suffering and pain. Alfred must answer every one of Bruce's questions.")
first_chat = True



@bot.event
async def on_ready():
    print(f'{bot.user.name} is now online!')


@bot.event
async def on_message(message):
    global first_chat
    if bot.user.mentioned_in(message) and message.author != bot.user:
        message_content = message.content
        to_prune = f"<@{bot.user.id}>"

        if to_prune in message_content:
            pruned_message = message_content.replace(to_prune, "").strip()
        else:
            pruned_message = message_content

        print(pruned_message)
        print("Thinking")
        if first_chat:
            # first_chat = False
            pruned_message = system_template + pruned_message

        payload = {'prompt': pruned_message}
        async with aiohttp.ClientSession() as session:
            async with session.post('http://alfred_brain:8080/generate', json=payload) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    response = data.get('response')
                else:
                    data = await resp.json()
                    response = data.get('response')
                    response = [resp.status, response]

        # response = await brain_query(f"{pruned_message}", model)

        print(response)
        for item in response:
            await message.reply(item)
    await bot.process_commands(message)

bot.run(TOKEN)
