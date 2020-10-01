import discord
import os
import logging
import wikipedia
import random
from sender import sender
from conf import config
from discord.ext import commands
from tinydb import TinyDB, Query
from tinydb.operations import delete,increment

database = TinyDB('labels.json')
query = Query()
logger = logging.getLogger(config.logfile)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename=config.logfile, encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


bot = commands.Bot(command_prefix=config.prefix)
servers = []
# Print the user and guild name upon start up
# Write to the logfile upon startup 
@bot.event
async def on_ready():
    async for guild in bot.fetch_guilds(limit=150):
        servers.append(guild.name)
    print('------------------------------')
    print('We have logged in as {0}'.format(config.name))
    print('At server: {0}'.format(servers))
    print('------------------------------')
    logger.info('Logged in as {0} on server: {1}'.format(config.name, servers))
    for cog_name in config.cogs:
        try:
            cog_name = 'Cogs.' + cog_name
            bot.load_extension(cog_name)
        except Exception as e:
            logger.error('Failed to load extension ' + cog_name + ' with error ' + str(e))
        else:
            logger.info('Loaded extension ' + cog_name)

@bot.event
async def on_member_join(member):
    for channel in member.guild.channels:
        if str(channel) == "banter": # We check to make sure we are sending the message in the general channel
            with open('welcomemessages.txt') as file:
                welcome_messages = file.read().splitlines()
            random.seed(a=None)
            response = random.choice(welcome_messages)
            await channel.send('```{0}```'.format(response))
            logger.info("{0} has joined the server.".format(member))


#If there is an error, it will answer with an error
@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f'```Error. Try .help ({error})```')

bot.run(config.token)