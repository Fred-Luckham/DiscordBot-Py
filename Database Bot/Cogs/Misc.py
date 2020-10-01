import discord
import os
import logging
import wikipedia
import random
from conf import config
from discord.ext import commands
from sender import sender

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

    @bot.event()
    async def on_member_join(member):
        with open('welcommessages.txt') as file:
            welcome_messages = file.read().splitlines()
        random.seed(a=None)
        response = random.choice(welcome_messages)
        await sender(ctx, response)
        logger.info("{0} has joined the server.".format(member))

def setup(bot):
    bot.add_cog(Misc(bot))