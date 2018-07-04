# -*- coding: utf-8 -*-

from discord.ext import commands
import discord

class CommunityDay:
    """The description for CommunityDay goes here."""

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    @commands.command()
    async def community(self, ctx):
        comDay = self.config['community_day']

        await ctx.send('{} the next Community Day event will feature ' \
                '**{}** on {} **{}**'.format(ctx.author.mention,
                    comDay['pokemon'], comDay['day'], comDay['date']))

def setup(bot):
    bot.add_cog(CommunityDay(bot))
    print("Added community-day cog")
