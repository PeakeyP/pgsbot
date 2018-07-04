# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import asyncio

class Admin:
    """These commands can only be run by an admin."""

    def __init__(self, bot):
        self.bot = bot
        self.load_admins()

    async def on_message(self, message):
        if message.content == 'repeat after me':
            if type(message.channel) == discord.DMChannel:
                await message.channel.send("Sorry, no can do. Try it from a real channel instead.")
                return

            what = await message.channel.send("Okay, I'm listening. What should I say?")

            def valid_response(m):
                return m.author == message.author

            reply = await self.bot.wait_for('message', check=valid_response)

            where = await message.channel.send("Great! Where should I post it?")

            def valid_response(m):
                return m.author == message.author and len(m.channel_mentions) == 1

            channel = await self.bot.wait_for('message', check=valid_response)

            sent = await self.say_to(message, channel.channel_mentions[0],
                    reply.content, [channel, where, reply, what, message])

    @commands.command(hidden=True)
    async def say(self, ctx, channel: discord.TextChannel, *, message):
        await self.say_to(ctx, channel, message, [ctx.message])

    async def say_to(self, ctx, channel, message, deletes = []):
        if not await self.is_admin(ctx):
            return

        if type(ctx.channel) == discord.DMChannel:
            await ctx.channel.send("Sorry, no can do. Try it from a real channel instead.")
            return

        await channel.send(message)

        sent = await ctx.channel.send("Message sent to {}: {}".format(channel, message))

        for msg in deletes:
            await msg.delete()

        await asyncio.sleep(3)
        await sent.delete()

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

    async def is_admin(self, ctx, send_message=True):
        if ctx.author.id in self.admins:
            return True

        if send_message:
            await ctx.send("Sorry {}, I can't do that :frowning:" \
                    .format(ctx.author.mention))

        return False

def setup(bot):
    bot.add_cog(Admin(bot))
    print("Added admin cog")
