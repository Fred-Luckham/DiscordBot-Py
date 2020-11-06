import shutil
import logging
import discord
from discord.ext import commands
from conf import config
from sender import sender

logger = logging.getLogger(config.logfile)


class Backup(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.claims_original = config.database_claims
        self.claims_target = config.db_claims_backup
        self.labels_orginal = config.database_labels
        self.labels_target = config.db_labels_backup

    @commands.command(
        name='backup',
        hidden=True
    )
    @commands.has_permissions(
        administrator=True
    )
    async def backup(self, ctx):
        try:
            shutil.copyfile(self.claims_original, self.claims_target)
            shutil.copyfile(self.labels_orginal, self.labels_target)
        except Exception as e:
            logger.error("failed to run backup command with error" + str(e))
        else:
            response = "Backup succesful"
            await sender(ctx, response)


def setup(bot):
    bot.add_cog(Backup(bot))
    # Adds the Basic commands to the bot
    # Note: The "setup" function has to be there in every cog file