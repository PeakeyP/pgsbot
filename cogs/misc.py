# -*- coding: utf-8 -*-

from discord.channel import DMChannel
from discord.ext import commands
import discord

class Misc:
    """General bot commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        '''
        Checks whether the bot is responding
        '''

        await ctx.send('Pong!')

    @commands.command()
    async def invite(self, ctx):
        """
        Gives you a link to use for inviting your friends
        """

        inviteLink = 'https://Discord.me/PokemonGoSomerset :+1:'

        await ctx.send(inviteLink)

def setup(bot):
    bot.add_cog(Misc(bot))
    print("Added misc cog")
