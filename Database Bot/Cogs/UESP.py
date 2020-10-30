import discord
import os
import logging
import random
import re
from urllib.request import *
from bs4 import BeautifulSoup
from conf import config
from discord.ext import commands
from sender import sender

logger = logging.getLogger(config.logfile)

class UESP(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='UESP',
        aliases=["uesp"],
        description="Preface your search term with one of the following: Lore:, Morrowind:, Tes3Mod:, Skyrim:, Oblivion:, Online:, Redgaurd:, Arena:, Daggerfall:, Battlespire:, TES_Travels:, Legends:, Blades:")
    async def UESP(self, ctx, message):
        search_term = ctx.message.content
        search_term = search_term.replace('!UESP ', '')
        search_term = search_term.replace('!uesp ', '')
        search_term = search_term.title()
        search_term = search_term.replace("'", "%27")
        search_term = search_term.replace(" ", "_")
        search_term = search_term.replace("The", "the")
        if "Tamriel_Rebuilt" not in search_term:
            search_term = search_term.replace("Tes3Mod:", "Tes3Mod:Tamriel_Rebuilt/")
        
        try:
            url = ("https://en.uesp.net/wiki/{0}".format(search_term))
            page = urlopen(url)
            html = page.read().decode("utf-8")
            soup = BeautifulSoup(html, "html.parser")
            soup.prettify()
            pTag = soup.p
            response = pTag.get_text()
            response = re.sub(r"[\[].*?[\]]", "", response)
            await sender(ctx, response)
            
        except:
            response = ('Sorry, I was not able to find anything. The command is still in beta, some results will not work as expected')
            await sender(ctx, response)
            logger.error('Unable to get results for {} from UESP'.format(search_term))




def setup(bot):
    bot.add_cog(UESP(bot))
    # Adds the Basic commands to the bot
    # Note: The "setup" function has to be there in every cog file