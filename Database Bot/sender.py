import discord
import os
import logging
import wikipedia
from conf import config
from discord.ext import commands

logger = logging.getLogger(config.logfile)

@commands.command(
    hidden=True
)
async def sender(ctx, response):
    if 'http' in response:
        await ctx.send(response)
    else:
        await ctx.send('```{0}```'.format(response))
    return
