import discord
import os
import logging
import wikipedia
import random
from conf import config
from discord.ext import commands
from sender import sender

logger = logging.getLogger(config.logfile)

class Misc(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='rules',
        description='List of server rules'
    )
    async def rules(self, ctx):
        response = config.server_rules
        await sender(ctx, response)
        return

    @commands.command(
        name='welcome',
        description='A welcome message'
    )
    async def welcome(self, ctx):
        response = config.welcome_message
        await sender(ctx, response)

def setup(bot):
    bot.add_cog(Misc(bot))