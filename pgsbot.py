#!/usr/bin/python3

import asyncio
import discord
from datetime import datetime

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

        if message.content == '!invite':
            inviteLink = 'https://Discord.me' \
                         '/PokemonGoSomerset :+1:'

            await message.channel.send(inviteLink)

        if message.content == '!community':
            communityText = 'Hi @everyone,\n' \
                            'Today is Community Day so dont forget ' \
                            'to get out and catch some shiny pokemon!'

            await message.channel.send(communityText)

    async def bg_task(self):
        await self.wait_until_ready()

        print("Connected!")

        channel = self.get_channel(CHANNEL_ID)

        while not self.is_closed():
            now = datetime.now()
            nextCommunityDay = 8

            if now.day == nextCommunityDay and now.hour == 8 and now.minute == 0:
                await channel.send( '@everyone today is Community Day, ' \
                                    'make sure you\'re up early grabbing ' \
                                    'pinap berries and balls!!')

            await asyncio.sleep(60)

client = PgsBot()
client.run('API_KEY')
