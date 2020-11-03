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
        self.drop_links = ["https://en.uesp.net#column-one", "https://en.uesp.net#searchInput", "en.uesp.nethttps:", "en.uesp.net/w/index.php", "https://en.uesp.net/wiki/UESPWiki:New_Page_Requests", "https://en.uesp.net/wiki/File:Disambig.png", "https://en.uesp.net/wiki/Help:Disambiguation"]

    @commands.command(
        name='UESP',
        aliases=["uesp"],
        description="Searches UESP for an article based on user input")
    async def UESP(self, ctx, message):
        search_term = ctx.message.content
        search_term = search_term.replace(' ', '+')
        search_term = search_term.title()
        search_term = re.sub(r'!Uesp\+', '', search_term)

        if ':' not in search_term:
            url = ("https://en.uesp.net/w/index.php?title=Special:Search&search={0}".format(search_term))
            page = urlopen(url)
            html = page.read().decode("utf-8")
            soup = BeautifulSoup(html, "html.parser")
            data = soup.findAll('div',attrs={'class':'mw-body-content'})
            await sender (ctx, 'No direct results found. Did you mean any of the following?')
            for div in data:
                links = div.findAll('a')
                links = links[:13]
                for a in links:
                    link = ("https://en.uesp.net" + a['href'])
                    if any(item in link for item in self.drop_links):
                        pass
                    else: 
                        await sender(ctx, "<{0}>".format(link))
        else:
            search_term = search_term.replace('+', '_')
            response = ("https://en.uesp.net/wiki/" + search_term)
            await sender(ctx, response)

def setup(bot):
    bot.add_cog(UESP(bot))
    # Adds the Basic commands to the bot
    # Note: The "setup" function has to be there in every cog file