# -*- coding: utf-8 -*-

from datetime import datetime
from discord.ext import commands
import discord
import asyncio

class CommunityDay:
    """
    Community Day is a monthly event in Pokemon GO.
    These commands will help you keep track!
    """

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

        bot.loop.create_task(self.comday_notifier())

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

    async def comday_notifier(self):
        await self.bot.wait_until_ready()

        channel = self.bot.get_channel('events')

        while not self.bot.is_closed():
            now = datetime.now()
            nextCommunityDay = 8

            if now.day == nextCommunityDay and now.hour == 8 and now.minute == 0:
                await channel.send( '@everyone Community Day starts in 2 hours!\n\n' \
                                    'Go get topped up on balls and berries!')

            if now.day == nextCommunityDay - 2 and now.hour == 10 and now.minute == 0:
                await channel.send( '@everyone Community Day is in 2 days! ' \
                                    'Make sure you\'re stocked up!')

            if now.day == nextCommunityDay - 7 and now.hour == 10 and now.minute == 0:
                await channel.send( '@everyone Community Day will be here in a ' \
                        'week. Plenty of time to fill up your bag with goodies!')

            await asyncio.sleep(60)

def setup(bot):
    bot.add_cog(CommunityDay(bot))
    print("Added community-day cog")
