# -*- coding: utf-8 -*-

from datetime import datetime
from discord.ext import commands
import discord

class Nests:
    """Nests change every other Thursday, but which Thursday!?"""

    def __init__(self, bot):
        self.bot = bot
        self.is_migration_week = bot.is_migration_week

    @commands.command(aliases=['migration'])
    async def migrating(self, ctx):
        """
        Says how long's left before the next nest migration
        """

        await ctx.send('{} {}'.format(ctx.author.mention, self.next_migration()))

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

def setup(bot):
    bot.add_cog(Nests(bot))
    print("Added nests cog")
