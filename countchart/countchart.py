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

    @staticmethod
    async def create_chart(top, others, channel):
        plt.clf()
        sizes = [x[1] for x in top]
        labels = ["{} {:g}%".format(x[0], x[1]) for x in top]
        if len(top) >= 20:
            sizes = sizes + [others]
            labels = labels + ["Others {:g}%".format(others)]
        if len(channel.name) >= 19:
            channel_name = "{}...".format(channel.name[:19])
        else:
            channel_name = channel.name
        title = plt.title("Stats in #{}".format(channel_name), color="white")
        title.set_va("top")
        title.set_ha("center")
        plt.gca().axis("equal")
        colors = [
            "r",
            "darkorange",
            "gold",
            "y",
            "olivedrab",
            "green",
            "darkcyan",
            "mediumblue",
            "darkblue",
            "blueviolet",
            "indigo",
            "orchid",
            "mediumvioletred",
            "crimson",
            "chocolate",
            "yellow",
            "limegreen",
            "forestgreen",
            "dodgerblue",
            "slateblue",
            "gray",
        ]
        pie = plt.pie(sizes, colors=colors, startangle=0)
        plt.legend(
            pie[0],
            labels,
            bbox_to_anchor=(0.7, 0.5),
            loc="center",
            fontsize=10,
            bbox_transform=plt.gcf().transFigure,
            facecolor="#ffffff",
        )
        plt.subplots_adjust(left=0.0, bottom=0.1, right=0.45)
        image_object = BytesIO()
        plt.savefig(image_object, format="PNG", facecolor="#36393E")
        image_object.seek(0)
        return image_object
        
    @commands.command()
    async def countchart(self, ctx):
        """Generates a pie chart, representing all the messages in the countchart channel."""
        
        channel = ctx.guild.get_channel(771829982158389258)
        message_history = await self.config.guild(ctx.guild).guild_messages()

        await ctx.send("Gathering messages...")
        
        async for msg in channel.history():
            if not msg in message_history:
                message_history.append(msg)
                await asyncio.sleep(0.005)

        await ctx.send("All messages gathered!")
        
        #await self.config.guild(ctx.guild).guild_messages.set(message_history)

    @commands.command()
    async def sendcountchart(self, ctx):
        message_history = await self.config.guild(ctx.guild).guild_messages()
        async for msg in message_history:
            await ctx.send("{}".format(msg))
        
    @commands.command()
    async def emptycountchart(self, ctx):
        empty = []
        await self.config.guild(ctx.guild).guild_messages.set(empty)
		
		