import discord
import os
import logging
from conf import config
from discord.ext import commands

logger = logging.getLogger(config.logfile)

@commands.command(
    hidden=True
)
async def sender(ctx, response):
    split_forbidden_char = config.forbidden_char.split(',')
    if any(item in response for item in split_forbidden_char):
        await ctx.send(response)
    else:
        await ctx.send('```{0}```'.format(response))
    return
