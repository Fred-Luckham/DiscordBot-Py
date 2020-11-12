import discord
import os
import logging
import random
import re
import selenium
from urllib.request import *
from bs4 import BeautifulSoup
from conf import config
from discord.ext import commands
from sender import sender
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys


logger = logging.getLogger(config.logfile)


class Webscrapper(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.drop_links = ["/users/", ".zip", ".ZIP", "https://en.uesp.net#column-one", "https://en.uesp.net#searchInput", "en.uesp.nethttps:", "en.uesp.net/w/index.php", "https://en.uesp.net/wiki/UESPWiki:New_Page_Requests", "https://en.uesp.net/wiki/File:Disambig.png", "https://en.uesp.net/wiki/Help:Disambiguation"]
    
    @commands.command(
        name='UESP',
        description="Searches UESP for an article based on user input. ?uesp <search term> for search results, or ?uesp <uesp category : search term> for direct links")
    async def UESP(self, ctx, message):
        try:
            search_term = ctx.message.content
            search_term = search_term.replace(' ', '+')
            search_term = search_term.title()
            search_term = re.sub(r'!Uesp\+', '', search_term)

            if ':' not in search_term:
                url = ("https://en.uesp.net/w/index.php?title=Special:Search&search={0}".format(search_term))
                page = urlopen(url)
                html = page.read().decode("utf-8")
                soup = BeautifulSoup(html, "html.parser")
                data = soup.findAll('p',attrs={'class':'mw-search-nonefound'})
                if data:
                    response = "No results found"
                    await sender(ctx, response)
                else:
                    data = soup.findAll('div',attrs={'class':'mw-body-content'})
                    embed = discord.Embed(title="No direct results found. Did you mean any of the following?")	
                    link_list = []
                    for div in data:
                        links = div.findAll('a')
                        links = links[:13]
                        for a in links:
                            link = ("https://en.uesp.net" + a['href'])
                            if any(item in link for item in self.drop_links):
                                pass
                            else:
                                href_text = re.match(r'(https:\/\/en.uesp.net\/wiki\/)(.*)', link)
                                href_text = href_text.group(2)
                                link_list.append("[{0}]({1})".format(href_text, link))
                    link_list = (' - '.join(link_list))
                    embed.set_thumbnail(url="https://images.uesp.net/b/bc/Wiki.png")
                    embed.description = "{0}".format(link_list)   
                    await ctx.send(embed=embed)
    
            else:
                search_term = search_term.replace('+', '_')
                url = ("https://en.uesp.net/wiki/{0}".format(search_term))
                try:
                    page = urlopen(url)
                    html = page.read().decode("utf-8")
                    soup = BeautifulSoup(html, "html.parser")
                    response = ("https://en.uesp.net/wiki/" + search_term)
                    await sender(ctx, response)
                except:
                    response = "No results found"
                    await sender(ctx, response)
        except Exception as e:
            logger.error("failed to run UESP command with error" + str(e))

    @commands.command(
        name='MEDIA',
        description="Searches UESP for any media based on user input.")
    async def MEDIA(self, ctx, message):
        try:
            search_term = ctx.message.content
            search_term = search_term.replace(' ', '+')
            search_term = search_term.title()
            search_term = re.sub(r'!Media\+', '', search_term)    
            url = ("https://en.uesp.net/w/index.php?title=Special:Search&profile=images&fulltext=Search&search={0}".format(search_term))
            page = urlopen(url)
            html = page.read().decode("utf-8")
            soup = BeautifulSoup(html, "html.parser")
            data = soup.findAll('p',attrs={'class':'mw-search-nonefound'})
            if data:
                response = "No results found"
                await sender(ctx, response)
            else:
                data = soup.findAll('div',attrs={'class':'mw-body-content'})
                embed = discord.Embed(title="Did you mean any of the following?")	
                link_list = []
                for div in data:
                    links = div.findAll('a')
                    links = links[:15]
                    for a in links:
                        link = ("https://en.uesp.net" + a['href'])
                        if any(item in link for item in self.drop_links):
                            pass
                        else:
                            href_text = re.match(r'(https:\/\/en.uesp.net\/wiki\/)(.*)', link)
                            href_text = href_text.group(2)
                            link_list.append(link)

                link_list = (' - '.join(link_list))
                embed.set_thumbnail(url="https://images.uesp.net/b/bc/Wiki.png")
                embed.description = "{0}".format(link_list)   
                await ctx.send(embed=embed)
    
        except Exception as e:
            logger.error("failed to run UESP command with error" + str(e))

    @commands.command(
        name='TIL',
        description="Searches The Imperial Library for any results based on user input.")
    async def TIL(self, ctx, message):
        try:
            search_term = ctx.message.content
            search_term = search_term.replace(' ', '%20')
            search_term = search_term.lower()
            search_term = re.sub(r'!til%20', '', search_term)    
            url = ("https://www.imperial-library.info/search/node/{0}".format(search_term))
            page = urlopen(url)
            html = page.read().decode("utf-8")
            soup = BeautifulSoup(html, "html.parser")
            for item in soup.findAll('div', {'class': 'box-title'}):
                if "Your search yielded no results" in item.text:
                    print("found no result")
                    response = "No results found"
                    await sender(ctx, response)
                else:
                    data = soup.findAll('dl',attrs={'class':'search-results node-results'})
                    embed = discord.Embed(title="Did you mean any of the following?")	
                    link_list = []
                    for div in data:
                        links = div.findAll('a')
                        links = links[:15]
                        for a in links:
                            link = (a['href'])
                            if any(item in link for item in self.drop_links):
                                pass
                            else:
                                href_text = re.match(r'(https:\/\/www.imperial-library.info\/content\/)(.*)', link)
                                href_text = href_text.group(2)
                                link_list.append("[{0}]({1})".format(href_text, link))

                    link_list = (' - '.join(link_list))
                    embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/824042384920956928/PAHkXsoE.jpg")
                    embed.description = "{0}".format(link_list)   
                    await ctx.send(embed=embed)
    
        except Exception as e:
            logger.error("failed to run TIL command with error" + str(e))

        
    @commands.command(
        name='namegen',
        description='''game options: df, mw, ob, sr, postmw 
                        race options: altmer, argonian, bosmer, breton, dunmer, ashlander, imperial, khajiit, nord, orc, redguard
                        gender options: male, female, any'''
    )
    async def namegen(self, ctx, game, race, gender):
        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')
            driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', options = chrome_options)
            driver.get('https://name.modding-openmw.com/')
            game_option = Select(driver.find_element_by_id('game'))
            race_option = Select(driver.find_element_by_id('race'))
            generate = driver.find_element_by_css_selector("input[type='button'][value='Generate']")
            game_option.select_by_value('{0}'.format(game))
            race_option.select_by_value('{0}'.format(race))
            if gender == 'male':
                driver.find_element_by_css_selector("input[type='radio'][value='male']").click()
            elif gender == 'female':
                driver.find_element_by_css_selector("input[type='radio'][value='female']").click()
            elif gender == 'any':
                driver.find_element_by_css_selector("input[type='radio'][value='any']").click()

        except Exception as e:
            logger.error("failed to run namegen command with error" + str(e))
        else:
            embed = discord.Embed(title="Here you go")	
            generate.click()
            output = driver.find_element_by_id('output').text
            embed.description = "{0}".format(output)
            embed.set_thumbnail(url="https://media.alienwarearena.com/thumbnail_630x315/Morrowind-Moon-and-Star.png")
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Webscrapper(bot))
    # Adds the Basic commands to the bot
    # Note: The "setup" function has to be there in every cog file