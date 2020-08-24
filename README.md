# DiscordBot-Py
A Discord bot with a database function written in Python

This bot is designed to help in the orghnistion of projects managed via Discord. It allows user to set, update, and retrieve "labels". These are keys to dictionary values, which can be text, urls, images.
This system was built to meet the requirements set out by an ongoing game modding project. Currently versions of it are running on 3 Discord servers. The commands can be easily locked behind certain user roles to prevent spam. 

Commands:
- !set    (sets a label with a value, ie. !set test "this is a test label")
- !get    (gets the stated label, ie. !get test would return "this is a test label")
- !update (updates the stated label with a new value.

The bot makes use of TinyDB, as it is functional and lightweight enough for the scope of the bot.

To do:
- Implement label subclasses
- Implement timed reminders
- Implement multiple databases
