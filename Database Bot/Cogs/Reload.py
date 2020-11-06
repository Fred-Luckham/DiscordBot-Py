import discord
import os
import logging
import random
from conf import config
from discord.ext import commands
from sender import sender

logger = logging.getLogger(config.logfile)

class Reload(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='reload', 
        hidden=True)
    async def _reload(self, ctx, module : str):
        try:
            self.bot.unload_extension(module)
            self.bot.load_extension(module)
        except Exception as e:
            logger.error('Failed to reload extension ' + module + ' with error ' + str(e))
            return
        else:
            response = ('{0} reloaded'.format(module))
            logger.info('Reloaded extension {0}'.format(module))
            await sender(ctx, response)
            return
    
    @commands.command(
        name='load', 
        hidden=True)
    async def _load(self, ctx, module : str):
        try:
            self.bot.load_extension(module)
        except Exception as e:
            logger.error('Failed to load extension ' + module + ' with error ' + str(e))
            return
        else:
            response = ('{0} loaded'.format(module))
            logger.info('Loaded extension {0}'.format(module))
            await sender(ctx, response)
            return

def setup(bot):
    bot.add_cog(Reload(bot))
    # Adds the Basic commands to the bot
    # Note: The "setup" function has to be there in every cog file