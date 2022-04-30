import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

bot= commands.Bot('&')

bot.load_extension('manager')
bot.load_extension('commands.talks')
bot.load_extension('music.music')

TOKEN = os.getenv('TOKEN')
bot.run(TOKEN)

