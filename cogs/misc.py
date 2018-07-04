# -*- coding: utf-8 -*-

from discord.channel import DMChannel
from discord.ext import commands
import discord

class Misc:
    """General bot commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='commands')
    async def _commands(self, ctx):
        mention = ctx.author.mention

        helptext = 'Hi there, {}!' \
                "\nHeard you could use a hand, so here's a list of commands you can use:" \
                '\n\n`!commands`: Sends you this message in a DM' \
                '\n`!ping`: Check if the bot is working' \
                '\n`!invite`: Get an invite link to send to your friends' \
                '\n`!community`: Find out information about the next Community Day' \
                '\n`!migrating`: Check when the next nest migration is due' \
                '\n\nHappy Hunting!'.format(mention)

        await ctx.author.send(helptext)

        if type(ctx.channel) != DMChannel:
            await ctx.send('{} I\'ve sent the command list to your DMs.'.format(mention))

    @commands.command()
    async def ping(self, ctx):
        '''
        Check whether the bot is responding
        '''

        await ctx.send('Pong!')

    @commands.command()
    async def invite(self, ctx):
        inviteLink = 'https://Discord.me' \
                     '/PokemonGoSomerset :+1:'

        await ctx.send(inviteLink)

def setup(bot):
    bot.add_cog(Misc(bot))
    print("Added misc cog")
