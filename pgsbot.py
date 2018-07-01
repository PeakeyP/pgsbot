#!/usr/bin/python3

import discord

class PgsBot(discord.Client):
    async def on_ready(self):
        print('Logged in as {0}.'.format(self.user))

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return

        await message.channel.send('Thanks for your message!')

client = PgsBot()
client.run('API_KEY')
