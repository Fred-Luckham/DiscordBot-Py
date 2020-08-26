import discord
import os
import logging
from discord.ext import commands
from conf import config
from tinydb import TinyDB, Query
from tinydb.operations import delete,increment

logger = logging.getLogger(config.logfile)

class Labels(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.database = TinyDB(config.database_labels)
        self.query = Query()


    @commands.command(
    name="set",
    description="sets a new entry in the database"
    )
    async def set(self, ctx, label, *, value):
        if self.database.contains(self.query.iid == label):
            await ctx.send('```Label already exists```')
        else:
            self.database.insert({'iid': label, 'url': value})
            await ctx.send('```Label set```')
            logger.info('{0} set the label {1} to {2}'.format(ctx.message.author.name, label, value))
            return

    @commands.command(name="get", 
    description="Gets an entry from the database"
    )
    async def get(self, ctx, label):
        if not self.database.contains(self.query.iid == label):
            await ctx.send('```Label not found```')
        else:
            label = self.database.get(self.query.iid == label)['url']
            await ctx.send(label)
            return
    
    @commands.command(name="update", 
    description="Updates an entry in the database"
    )
    async def update(self, ctx, label, *, value):
        if not self.database.contains(self.query.iid == label):
            self.database.contains({'url': value}, self.query.iid == label)
            await ctx.send('```Label not found```')
            return
        elif self.database.contains(self.query.iid == label):
            self.database.update({'url': value}, self.query.iid == label)
            await ctx.send('```Updated label```')
            logger.info('{0} updated the label {1} to {2}'.format(ctx.message.author.name, label, value))
            return

    @commands.command(name="remove",
    description="Removes an entry from the database"
    )
    async def remove(self, ctx, label):
        if not self.database.contains(self.query.iid == label):
            await ctx.send('```Label not found```')
        else:
            label = self.database.remove(self.query.iid == label)
            await ctx.send('```Label removed```')
            logger.info('{0} removed the label {1}'.format(ctx.message.author.name, label))
            return

def setup(bot):
    bot.add_cog(Labels(bot))
    # Adds the Basic commands to the bot
    # Note: The "setup" function has to be there in every cog file