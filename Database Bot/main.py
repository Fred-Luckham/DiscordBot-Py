import discord
import os
import time
import asyncio
import random
from conf import config
from discord.ext import commands
from tinydb import TinyDB, Query
from tinydb.operations import delete,increment

database = TinyDB('labels.json')
query = Query()
# Seperate the token from the main bot

# Use '!' as a command prefix
bot = commands.Bot(command_prefix=config.prefix)

# Print the user and guild name upon start up
@bot.event
async def on_ready():
    print('------------------------------')
    print('We have logged in as {0}'.format(config.name))
    print('------------------------------')
    for cog_name in config.cogs:
        try:
            cog_name = 'Cogs.' + cog_name
            bot.load_extension(cog_name)
        except Exception as e:
            print('Failed to load extension ' + cog_name + ' with error ' + str(e))
        else:
            print('Loading extension ' + cog_name)


#If there is an error, it will answer with an error
@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f'```Error. Try .help ({error})```')

bot.run(config.token)