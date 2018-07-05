# -*- coding: utf-8 -*-

from datetime import datetime
from discord.ext import commands
import discord
import asyncio

class Nests:
    """Nests change every other Thursday, but which Thursday!?"""

    def __init__(self, bot):
        self.bot = bot

        bot.loop.create_task(self.migration_notifier())

    @commands.command(aliases=['migration'])
    async def migrating(self, ctx):
        """
        Says how long's left before the next nest migration
        """

        await ctx.send('{} {}'.format(ctx.author.mention, self.next_migration()))

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

    async def migration_notifier(self):
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            now = datetime.now()

            if now.weekday() == 3 and now.hour == 2 and now.minute == 17:
                await self.send_migration_alert(self.is_migration_week(now))

            await asyncio.sleep(60)

    async def send_migration_alert(self, is_migration_week):
        if is_migration_week:
            msg = 'Trainers, nesting species have migrated! The {} Global ' \
                    'Nest Migration has occured, and we need @everyone to ' \
                    'help report new nesting species to the <#{}> channel.' \
                    .format(self.config['events']['migrations'],
                            self.bot.channel_to_id('nests'))
        else:
            msg = '@everyone, Nests will migrate next week!'

        return await self.bot.get_channel('nests').send(msg)

def setup(bot):
    bot.add_cog(Nests(bot))
    print("Added nests cog")
