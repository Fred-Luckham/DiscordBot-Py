import discord
import os
import logging
import re
from sender import sender
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
        ame="set",
        description="sets a new entry in the database"
    )
    async def set(self, ctx, label, *, value):
        try:
            label = label.lower()
            if self.database.contains(self.query.iid == label):
                response = ('Label already exists, you can !update the label with a new value')
                await sender(ctx, response)
            else:
                self.database.insert({'iid': label, 'url': value})
                response = ('Label set, you can !update the value or !remove the label')
                await sender(ctx, response)
                logger.info('{0} set the label {1} to {2}'.format(ctx.message.author.name, label, value))
                return
        except Exception as e:
            logger.error("!set command failed with error: " + str(e) + ", User: " + str(ctx.message.author) + ", Content: " + str(ctx.message.content))

    @commands.command(
        name="get", 
        description="Gets an entry from the database: aliases: show, get",
        aliases=["show"]
    )
    async def get(self, ctx, label):
        try:
            label = label.lower()
            if not self.database.contains(self.query.iid == label):
                response = ('Label not found, you can !set the label with a value')
                await sender(ctx, response)
            else:
                response = self.database.get(self.query.iid == label)['url']
                await sender(ctx, response)
                logger.info('{0} called the label {1}'.format(ctx.message.author.name, label))
                return
        except Exception as e:
            logger.error("!get command failed with error: " + str(e) + ", User: " + str(ctx.message.author) + ", Content: " + str(ctx.message.content))

    @commands.command(
        name="update", 
        description="Updates an entry in the database"
    )
    async def update(self, ctx, label, *, value):
        try:
            label = label.lower()
            if not self.database.contains(self.query.iid == label):
                self.database.contains({'url': value}, self.query.iid == label)
                response = ('Label not found')
                await sender(ctx, response)
                return
            elif self.database.contains(self.query.iid == label):
                self.database.update({'url': value}, self.query.iid == label)
                response = ('Updated label, you can !set the label with a value or !remove the label')
                await sender(ctx, response)
                logger.info('{0} updated the label {1} to {2}'.format(ctx.message.author.name, label, value))
                return
        except Exception as e:
            logger.error("!update command failed with error: " + str(e) + ", User: " + str(ctx.message.author) + ", Content: " + str(ctx.message.content))


    @commands.command(
        name="remove",
        description="Removes an entry from the database: aliases: remove, delete",
        aliases=["delete"]
    )
    async def remove(self, ctx, label):
        try:
            label = label.lower()
            if not self.database.contains(self.query.iid == label):
                response = ('Label not found, you can !set the label with a value')
                await sender(ctx, response)
            else:
                label = self.database.remove(self.query.iid == label)
                response = ('Label removed')
                await sender(ctx, response)
                logger.info('{0} removed the label {1}'.format(ctx.message.author.name, label))
                return
        except Exception as e:
            logger.error("!remove command failed with error: " + str(e) + ", User: " + str(ctx.message.author) + ", Content: " + str(ctx.message.content))

    @commands.command(
        name="labels",
        description="Shows all set labels in the database"
    )
    async def labels(self, ctx):
        try:
            embed = discord.Embed(title="All labels in the database")	
            dbdump = self.database.all()
            label_list = []
            for item in dbdump:
                label_value = re.match(r"(({'iid':\s')(.*?)')", str(item))
                label_list.append(label_value.group(3))
            label_list = sorted(label_list)
            label_list = (' - '.join(label_list))
            embed.description = "{0}".format(label_list) 
            await ctx.send(embed=embed)
        except Exception as e:
            logger.error("!labels command failed with error: " + str(e) + ", User: " + str(ctx.message.author))

def setup(bot):
    bot.add_cog(Labels(bot))
    # Adds the Basic commands to the bot
    # Note: The "setup" function has to be there in every cog file