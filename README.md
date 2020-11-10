# Hex
A Discord bot with a database function written in Python

This bot is designed to help in the organisation of projects managed via Discord. It allows user to set, update, and retrieve "labels". These are keys to dictionary values, which can be text, urls, images.
This system was built to meet the requirements set out by an ongoing game modding project. Currently versions of it are serving a user base of around 2000. The commands can be easily locked behind certain user roles to prevent spam. 
There are a number of Cogs which can be included as needed. The bot will remain as modular as possible.
The default prefix is: !
The ini file allows the admin to set their own paramters. 

Database Commands:
- !set    (sets a label with a value, ie. !set test "this is a test label")
- !get    (gets the stated label, ie. !get test would return "this is a test label")
- !update (updates the stated label with a new value.
- !remove (removes the stated label)

Misc Commands:
- !rules    (Displays server rules)
- !welcome  (Displays a welcome message)

UESP Commands:
- !uesp (Scrapes the UESP wiki for pages and attempts to return a link to a page, or a list of potential relevant results)
- !media (Scrapes the UESP wiki for media and attempts to return a list of potential relevant results)

Reload Commands (Default admin only and hidden):
- !reload path.filename  (reloads the specified Cog whilst the bot is running)
- !load path.filename    (loads the specified Cog whils the bot is running)

Backup Commands(Default admin only and hidden):
- !backup (backups the .json database files to the specified path in the ini)

Dependancies:
- TinyDb
- Discord.py
- BeautifulSoup
