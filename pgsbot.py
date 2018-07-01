#!/usr/bin/python3

import asyncio
import discord
import configparser
from datetime import datetime

class PgsBot(discord.Client):
    def __init__(self, *args, **kwargs):
        print('Loading...')
        self.config = kwargs['config']

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

        channel = self.get_channel(int(self.config['channel']['testing']))

        while not self.is_closed():
            now = datetime.now()
            nextCommunityDay = 8

            if now.day == nextCommunityDay and now.hour == 8 and now.minute == 0:
                await channel.send( '@everyone today is Community Day, ' \
                                    'make sure you\'re up early grabbing ' \
                                    'pinap berries and balls!!')

            if now.day == nextCommunityDay - 2 and now.hour == 10 and now.minute == 0:
                await channel.send( '@everyone Community Day is in 2 days! ' \
                                    'Make sure you\'re stocked up!')

            if now.day == nextCommunityDay - 7 and now.hour == 10 and now.minute == 0:
                await channel.send( '@everyone we have got a Community Day in a ' \
                        'week - Plenty of time to fill up your bag with goodies!')

            if now.weekday() == 3 and now.hour == 2 and now.minute == 17:
                if now.isocalendar()[1] % 2 == 0:
                    msg = 'Trainers, nesting species have migrated! The 57th Global ' \
                            'Nest Migration has occured, and we need @everyone to ' \
                            'help report new nesting species to the #nests channel.'
                else:
                    msg = '@everyone, Nests will migrate next week!'

                await channel.send(msg)

            await asyncio.sleep(60)

config = configparser.ConfigParser()
config.read('config.ini')

client = PgsBot(config=config)
client.run(config['bot']['token'])
