import discord
import os
import time
import asyncio
import random
import json
from discord.ext import commands
from datetime import datetime as d
from random import randint
from tinydb import TinyDB, Query
from tinydb.operations import delete,increment


# New - The Cog class must extend the commands.Cog class
class Commands(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.database = TinyDB('labels.json')
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
            return

            
def setup(bot):
    bot.add_cog(Commands(bot))
    # Adds the Basic commands to the bot
    # Note: The "setup" function has to be there in every cog file