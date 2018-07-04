# -*- coding: utf-8 -*-

from discord.ext import commands
import discord

class CommunityDay:
    """
    Community Day is a monthly event in Pokemon GO.
    These commands will help you keep track!
    """

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    @commands.command()
    async def community(self, ctx):
        """
        Gets details for the next Community Day

        Forgotten the next Community Day? This command will
        let you know the day, date and shiny Pokemon that'll
        be spawning during the 3 hour event window.
        """

        comDay = self.config['community_day']

        await ctx.send('{} the next Community Day event will feature ' \
                '**{}** on {} **{}**'.format(ctx.author.mention,
                    comDay['pokemon'], comDay['day'], comDay['date']))

def setup(bot):
    bot.add_cog(CommunityDay(bot))
    print("Added community-day cog")
