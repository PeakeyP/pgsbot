#!/usr/bin/python3

import discord

class PgsBot(discord.Client):
    async def on_ready(self):
        print('Logged in as {0}.'.format(self.user))

client = PgsBot()
client.run('API_KEY')
