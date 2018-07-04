#!/usr/bin/python3

import asyncio
import discord
import configparser
from datetime import datetime
from discord.ext import commands

class PgsBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        print('Loading...')

        self.load_admins()
        self.config = kwargs['config']

        super().__init__(command_prefix=commands.when_mentioned_or('!'), \
                *args, **kwargs)

        self.load_extension('cogs.misc')
        self.load_extension('cogs.community-day')

        self.bg_task = self.loop.create_task(self.bg_task())

    async def on_ready(self):
        print('Logged in as {0}.'.format(self.user))

        await self.change_presence(
                status = discord.status.online,
                activity = discord.Game(name='Pokémon GO'))

    def load_admins(self):
        self.admins = []

        try:
            with open('admins.txt') as f:
                for admin in f.read().splitlines():
                    self.add_admin(admin)

        except FileNotFoundError:
            print("admins.txt file does not exist. Admin commands won't run.")

        return bool(len(self.admins))

    def add_admin(self, admin):
        print('Adding ' + admin + ' to list of admins')

        self.admins.append(int(admin))

    async def is_admin(self, message, send_message=True):
        if message.author.id in self.admins:
            return True

        if send_message:
            await message.channel.send("Sorry {}, I can't do that :frowning:" \
                    .format(message.author.mention))

        return False

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

    def next_migration(self):
        now = datetime.now()

        if not self.is_migration_week(now):
            text = "Nests will migrate next Thursday.\n" \
                    "Looks like you're stuck with these for a while :worried:"
        elif now.day < 3:
            text = 'Nests will migrate this Thursday!'
        elif now.day > 3:
            text = 'Nests recently migrated. Get out there and start hunting, trainer!'
        elif now.hour < 1:
            text = 'Nests migrate in under an hour! Batteries charged?'
        elif now.hour > 3:
            text - 'Nests migrated today!'
        else:
            text = 'Nests *just* migrated. What are you waiting for!?'

        return text

    async def on_message(self, message):
        await super().on_message(message)

        print('<#{}> @{}: {}'.format(
                message.channel,
                message.author,
                message.content
        ))

        if message.author.id == self.user.id:
            return

        if message.content == '!migrating':
            await message.channel.send('{} {}'.format(message.author.mention, self.next_migration()))

        if message.content.lower() == 'repeat after me':
            if not await self.is_admin(message):
                return

            if type(message.channel) == DMChannel:
                await channel.send("Sorry, no can do. Try it from a real channel instead.")
                return

            what = await message.channel.send("Okay, I'm listening. What should I say?")

            def valid_response(m):
                return m.author == message.author

            reply = await self.wait_for('message', check=valid_response)

            where = await message.channel.send("Great! Where should I post it?")

            def valid_response(m):
                return m.author == message.author and len(m.channel_mentions) == 1

            channel_reply = await self.wait_for('message', check=valid_response)

            await channel_reply.channel_mentions[0].send(reply.content)
            sent = await message.channel.send("Message sent to {}: {}".format(
                channel_reply.content, reply.content))

            for ch in [channel_reply, where, reply, what, message]:
                await ch.delete()

            await asyncio.sleep(2)
            await sent.delete()

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
