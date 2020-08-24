from configparser import ConfigParser

__all__ = ('config')

# System to read configuration settings read from ini file stored locally
# Seperates private info from the public repo

class Config:
    """Server specific configuration settings read from ini file stored locally (if self hosting), else stored on the server"""
    def __init__(self):
        try:
            self.config = ConfigParser()
            self.config.read('bot.ini')

            # Note: Default paths are given relative to the bot's root path
            # Feel free to specify absolute paths in your bot.ini to be clear
            self.token = self.config.get('Private', 'token', fallback='') # DO NOT set token here directly
            self.cogs_path = self.config.get('Private', 'cogs_path', fallback='cogs')
            self.bot_channel_id = int(self.config.get('Private', 'bot_channel_id', fallback=''))
            self.admins = self.config.get('Private', 'admins', fallback= '')
            self.database = self.config.get('Private', 'database', fallback='labels.json')
            self.main_server = int(self.config.get('Private', 'main_server', fallback=''))
            self.additional_info_text = self.config.get('Private', 'additional_info_text', fallback='')
            
            self.timezone = self.config.get('General', 'timezone', fallback='GMT') # Note: this is just a string to be printed. Does not affect actually affect displayed time.
            self.description = self.config.get('General', 'description', fallback='''A simple database bot''')
            self.name = self.config.get('General', 'name', fallback='DB BOT')
            self.prefix = self.config.get('General', 'prefix', fallback='!')
            self.cogs = self.config.get('General', 'cogs', fallback='Commands').split(',')

        except Exception as e:
            print('Error reading config file' + str(e))
    
    def get(self, category, name, fallback):
        return self.config.get(category, name, fallback=fallback)

config = Config()