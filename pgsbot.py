#!/usr/bin/python3

import discord
import configparser
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

config = configparser.ConfigParser()
config.read('config.ini')

bot = PgsBot(config=config)
bot.run(config['bot']['token'])
