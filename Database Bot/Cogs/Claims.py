import discord
import os
import logging
import json
import re
from discord.ext import commands
from conf import config
from tinydb import TinyDB, Query
from tinydb.operations import delete,increment

logger = logging.getLogger(config.logfile)
claims = ["wg_01", "wg_02", "wg_03", "wg_04", "wg_05", "wg_06", "wg_07", "wg_08", "wg_09"]

class Claims(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.database = TinyDB(config.database_claims)
        self.query = Query()


    @commands.command(
    name="set_claim",
    description="Allows devs to set new claims. The correct format is (set_claim region-number), for example: set_claim wg_01"
    )
    @commands.has_any_role('Lead Dev', 'Developer')
    async def set_claim(self, ctx, label):
        value = ctx.message.author.name
        if label in claims:
            if self.database.contains(self.query.claim == label):
                await ctx.send('```Claim already exists```')
            else:
                self.database.insert({'claim': label, 'dev': value})
                await ctx.send('```Claimed```')
                logger.info('{0} claimed {1}'.format(value, label))
                return
        else:
            await ctx.send('```Not a valid claim. The correct format is (claim region-number), for example claim wg_01```')
            return
    
    @commands.command(
    name="update_claim",
    description="Allows devs to update claims. The correct format is (update_claim region-number), for example: update_claim wg_01. This will set the claim to whoever called the command."
    )
    @commands.has_any_role('Lead Dev', 'Developer')
    async def update_claim(self, ctx, label):
        value = ctx.message.author.name
        if label in claims:
            if not self.database.contains(self.query.claim == label):
                self.database.contains({'dev': value}, self.query.claim == label)
                await ctx.send('```Claim not found```')
                return
            elif self.database.contains(self.query.claim == label):
                self.database.update({'dev': value}, self.query.claim == label)
                await ctx.send('```Updated claim```')
                logger.info('{0} updated the claim {1}'.format(value, label))
                return
        else:
            await ctx.send('```Not a valid claim. The correct format is (update_claim region-number), for example update_claim wg_01```')
            return

    @commands.command(
    name="drop_claim",
    description="Allows devs to drop claims. The correct format is (drop_claim region-number), for example: drop_claim wg_01"
    )
    @commands.has_any_role('Lead Dev', 'Developer')
    async def drop_claim(self, ctx, label):
        value = ctx.message.author.name
        if self.database.contains(self.query.dev == value):
            if label in claims:
                if not self.database.contains(self.query.claim == label):
                    await ctx.send('```Claim is not set```')
                    return
                else:
                    label = self.database.remove(self.query.claim == label)
                    await ctx.send('```Claim dropped```')
                    logger.info('{0} dropped claim {1}'.format(value, label))
                    return
            else:
                await ctx.send('```Not a valid claim. The correct format is (drop_claim region-number), for example drop_claim wg_01```')
                return
        else:
            await ctx.send('```You do not own this claim or it is not yet set```')

    @commands.command(
        name="show_claims",
        description="Shows all the current claims in the database"
    )
    async def show_claims(self, ctx):
        items = self.database.all()
        indented = (json.dumps(items, indent=4))
        formatted = re.sub('\[|\]|\{|\}|\,|\"|\'', '', indented)
        await ctx.send('```{0}```'.format(formatted))

def setup(bot):
    bot.add_cog(Claims(bot))
    # Adds the Basic commands to the bot
    # Note: The "setup" function has to be there in every cog file