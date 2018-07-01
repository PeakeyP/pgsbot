#!/usr/bin/python3

import asyncio
import discord

class PgsBot(discord.Client):
    def __init__(self, *args, **kwargs):
        print('Loading...')

        super().__init__(*args, **kwargs)
        self.bg_task = self.loop.create_task(self.bg_task())

    async def on_ready(self):
        print('Logged in as {0}.'.format(self.user))

    async def on_message(self, message):
        print('<#{}> @{}: {}'.format(
                message.channel,
                message.author,
                message.content
        ))

        if message.author.id == self.user.id:
            return

        if message.content == '!ping':
            await message.channel.send('pong')

    async def bg_task(self):
        await self.wait_until_ready()

        print("Connected!")

client = PgsBot()
client.run('API_KEY')
