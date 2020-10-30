# DiscordBot-Py
A Discord bot with a database function written in Python

This bot is designed to help in the orghnistion of projects managed via Discord. It allows user to set, update, and retrieve "labels". These are keys to dictionary values, which can be text, urls, images.
This system was built to meet the requirements set out by an ongoing game modding project. Currently versions of it are running on 3 Discord servers. The commands can be easily locked behind certain user roles to prevent spam. 

Database Commands:
- !set    (sets a label with a value, ie. !set test "this is a test label")
- !get    (gets the stated label, ie. !get test would return "this is a test label")
- !update (updates the stated label with a new value.
- !remove (removes the stated label)

Misc Commands:
- !rules  (Displays server rules)
- !welcome (Displays a welcome message)

Wiki Commands:
- !wiki (takes message content and sends it as a query in a wikipedia.summary search, and returns the results)

UESP Commands (Beta):
- !uesp (Scrapes the UESP wiki and attempts to return two sentences of the summary from the desired page)

Passive events:
- Bot sends a randomly selected message to the general channel when a new member joins
 (messages chosen from welcomemessage.txt)

Dependancies:
- TinyDb
- wikipedia
- Discord.py

To do:
- Implement label subclasses
- Implement timed reminders
