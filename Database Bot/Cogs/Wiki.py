import discord
import os
import logging
import wikipedia
from sender import sender
from conf import config
from discord.ext import commands

class Wiki(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='wiki',
        description='Grabs whatever it finds from Wikipedia'
    )
    async def wiki(self, ctx, message):
        searchterm = ctx.message.content
        response = wikipedia.summary(searchterm, sentences=2)
        await sender(ctx, response)
        return


def setup(bot):
    bot.add_cog(Wiki(bot))