"""
-----------------------------------------------------------------------
Problem: Project documents need organising, and finding relevant info is hard
Target Users: Modding project members
Target System: GNU/Linux, Windows, Mac
Interface: Command-line
Functional Requirements: Store data, retreive data, message users, webscrape from relevant sites
Testing: Testing on test version and server
Maintainer: frederickluckham@gmail.com

-----------------------------------------------------------------------

HEX is a Discord Bot written in Python, using the Discord.py library.
This bot is designed to help in the organisation of projects managed via Discord. 
It allows user to set, update, and retrieve "labels". These are keys to dictionary values, 
which can be text, urls, images. This system was built to meet the 
requirements set out by an ongoing game modding project. 

Currently versions of it are serving a user base of around 2000. 
The commands can be easily locked behind certain user roles to prevent spam. 
There are a number of Cogs which can be included as needed. 
The bot will remain as modular as possible. 
The default prefix is: ! The ini file allows the admin to set their own paramters.

-----------------------------------------------------------------------
Core Modules:
    Database Commands:
    !set (sets a label with a value, ie. !set test "this is a test label")
    !get (gets the stated label, ie. !get test would return "this is a test label")
    !update (updates the stated label with a new value.
    !remove (removes the stated label)

    Misc Commands:
    !rules (Displays server rules)
    !welcome (Displays a welcome message)

    Webscrapper Commands:
    !uesp (Scrapes the UESP wiki for pages and attempts to return a link to a page, or a list of potential relevant results)
    !media (Scrapes the UESP wiki for media and attempts to return a list of potential relevant results)
    !til (Scrapes the Imperial Library for results based on user input)
    !namegen (Uses the TES name generator hosted on OpenMW-Modding to return randomly generated names)

    Reload Commands (Default admin only and hidden):
    !reload path.filename (reloads the specified Cog whilst the bot is running)
    !load path.filename (loads the specified Cog whils the bot is running)

    Backup Commands(Default admin only and hidden):
    !backup (backs up the .json database files to the specified path in the ini)

-----------------------------------------------------------------------
"""

# Import modules here
import discord
import os
import logging
import random
from sender import sender
from conf import config
from discord.ext import commands
from tinydb import TinyDB, Query
from tinydb.operations import delete,increment

# Define core aspects:
# - Database
database = TinyDB('labels.json')
query = Query()
# - Logger
logger = logging.getLogger(config.logfile)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename=config.logfile, encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
# - Bot
bot = commands.Bot(command_prefix=config.prefix, case_insensitive=True)
bot.help_command = commands.DefaultHelpCommand(dm_help=True)
# - Server List
servers = []


# Check servers the bot is on and populate server list
@bot.event
async def on_ready():
    async for guild in bot.fetch_guilds(limit=150):
        servers.append(guild.name)
    # Print status to console
    print('------------------------------')
    print('We have logged in as {0}'.format(config.name))
    print('At server: {0}'.format(servers))
    print('------------------------------')
    # Log if succesful
    logger.info('Logged in as {0} on server: {1}'.format(config.name, servers))
    # Load cogs from list in config
    for cog_name in config.cogs:
        try:
            cog_name = 'Cogs.' + cog_name
            bot.load_extension(cog_name)
        except Exception as e:
            # Log if error
            logger.error('Failed to load extension ' + cog_name + ' with error ' + str(e))
        else:
            # Log if succesful
            logger.info('Loaded extension ' + cog_name)


#If there is an error, react with emoji
@bot.event
async def on_command_error(ctx, message):
    user = ctx.message.author
    message = ctx.message.content
    if message.count(config.prefix) >= 2:
        pass
    else:
        emoji = '❓'
        await ctx.message.add_reaction(emoji)
        logger.info(str(user) + ' tried to use the command ' + str(message) + ' but it does not exist.')

bot.run(config.token)
