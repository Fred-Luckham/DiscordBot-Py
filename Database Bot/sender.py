# Import Modules 
import discord
import os
import logging
import wikipedia
from conf import config
from discord.ext import commands

# Define Logger
logger = logging.getLogger(config.logfile)

''' 
This function handles all messages sent by the bot to the relevant channel. 
It formats text into code blocks, and sends links / mentions with no formatting so as not to break them . 
'''

@commands.command(
    hidden=True
)
async def sender(ctx, response):
    # Check for forbidden charcters from config list
    split_forbidden_char = config.forbidden_char.split(',')
    # If any. send with no formatting
    if any(item in response for item in split_forbidden_char):
        await ctx.send(response)
    # If none. format in code blocks
    else:
        await ctx.send('```{0}```'.format(response))
    return
