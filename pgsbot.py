#!/usr/bin/python3

import asyncio
import discord
import configparser
from datetime import datetime
from discord.ext import commands

class PgsBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        print('Loading...')

        self.config = kwargs['config']

        super().__init__(command_prefix=commands.when_mentioned_or('!'),
                description="I'm a home-made Discord bot built especially for Pokemon GO Somerset!" \
                        "\n\nHere's a list of commands you can use:", *args, **kwargs)

        self.load_extension('cogs.admin')
        self.load_extension('cogs.misc')
        self.load_extension('cogs.nests')
        self.load_extension('cogs.community-day')

        self.bg_task = self.loop.create_task(self.bg_task())

    async def on_ready(self):
        print('Logged in as {0}.'.format(self.user))

        await self.change_presence(
                status = discord.status.online,
                activity = discord.Game(name='Pokémon GO'))

    def test_mode(self):
        return config['bot'].getboolean('test_mode')

    def channel_to_id(self, channel):
        return int(self.config['channels'][channel])

    def get_channel(self, channel=None):
        if self.test_mode():
            channel = 'testing'
        else:
            if not channel:
                channel = 'default'

            if not isinstance(channel, int):
                channel = self.channel_to_id(channel)

        return super().get_channel(self, channel)

    def is_migration_week(self, date):
        return date.isocalendar()[1] % 2 == 0

    async def on_message(self, message):
        await super().on_message(message)

        print('<#{}> @{}: {}'.format(
                message.channel,
                message.author,
                message.content
        ))

        if message.author.id == self.user.id:
            return

    async def bg_task(self):
        await self.wait_until_ready()

        print("Connected!")

        channel = self.get_channel('events')

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
                if self.is_migration_week(now):
                    msg = 'Trainers, nesting species have migrated! The {} Global ' \
                            'Nest Migration has occured, and we need @everyone to ' \
                            'help report new nesting species to the <#{}> channel.' \
                            .format(self.config['events']['migrations'],
                                    self.channel_to_id('nests'))
                else:
                    msg = '@everyone, Nests will migrate next week!'

                await self.get_channel('nests').send(msg)

            await asyncio.sleep(60)

config = configparser.ConfigParser()
config.read('config.ini')

bot = PgsBot(config=config)
bot.run(config['bot']['token'])
