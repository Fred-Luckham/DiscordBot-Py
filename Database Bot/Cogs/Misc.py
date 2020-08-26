import discord
import os
import logging
from conf import config
from discord.ext import commands

class Misc(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot


    @commands.command(
        name='rules',
        description='List of server rules'
    )
    async def rules(self, ctx):
        response=("``` **1:** Spamming, advertising (of paid services or content that is not related to the Elder Scrolls) or automated messages are forbidden.\n **2:** No harassment of other users. Threats, insults, abusive, inflammatory comments, and hate speech are forbidden and result in an immediate ban.\n **3:** Political discussion is not tolerated, this is a modding server.\n **4:** Sexual or illegal media/content is forbidden```")
        await ctx.send(response)
        return

    @commands.command(
        name='welcome',
        description='A welcome message'
    )
    async def welcome(self, ctx):
        await ctx.send("```Welcome! Thanks for joining. Please feel free to ask any project related questions in #general, and familiarise yourself with the rules (!rules)```")

    @commands.command(
        name='quarantine',
        description='Sends a message to HoTV quarantine'
    )
    async def quarantine(self, ctx, message):
        channel = self.bot.get_channel(740991480574902405)
        await channel.send(message)
        return


def setup(bot):
    bot.add_cog(Misc(bot))