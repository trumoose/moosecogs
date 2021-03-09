import asyncio
import discord
import heapq
from io import BytesIO
from typing import Optional

import matplotlib

matplotlib.use("agg")
import matplotlib.pyplot as plt

plt.switch_backend("agg")

from redbot.core import checks, commands, Config


class Countchart(commands.Cog):
    """Show activity."""
    
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1312131213121312, force_registration=True)
        self.config.register_guild(guild_messages = [])

    
        
    @commands.command()
    async def countchart(self, ctx):
        """Generates a pie chart, representing all the messages in the countchart channel."""
        
        channel = discord.utils.get(guild.text_channels, id=771829982158389258)
        #messages = 1000000
        await ctx.send("{}".format(channel.name))
        #message_history = await self.config.guild(ctx.guild).guild_messages()

        #async for msg in channel.history(limit=messages):
            #if not msg in message_history:
                #message_history.append(msg)
                #await asyncio.sleep(0.005)

        #await self.config.guild(ctx.guild).guild_messages.set(message_history)