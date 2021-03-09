import asyncio
import discord
import heapq
from io import BytesIO
from typing import Optional
import numpy as np

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
        self.config.register_guild(guild_messages = [], guild_authors = [])

    @staticmethod
    async def create_chart(top, others, channel):
        plt.clf()
        sizes = [x[1] for x in top]
        labels = ["{} {:g}%".format(x[0], x[1]) for x in top]
        if len(top) >= 20:
            sizes = sizes + [others]
            labels = labels + ["Others {:g}%".format(others)]
        title = plt.title("Counting  ", color="white", fontsize=15)
        title.set_va("top")
        title.set_ha("center")
        plt.gca().axis("equal")
        cmap = plt.cm.terrain
        colors = cmap(np.linspace(0., 1., 21))
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
        plt.subplots_adjust(left=0.0, bottom=0.0, right=0.52)
        image_object = BytesIO()
        plt.savefig(image_object, format="PNG", facecolor="#36393E")
        image_object.seek(0)
        return image_object
        
    @commands.command()
    async def countchart(self, ctx):
        """Generates a pie chart, representing all the messages in the countchart channel."""
        
        channel = ctx.guild.get_channel(771829982158389258)
        messages = channel.history(limit = 1000000)
        
        msg_data = {"total count": 0, "users": {}}
        async with self.config.guild(ctx.guild).guild_messages() as message_history:
            async with self.config.guild(ctx.guild).guild_authors() as authors:
                last_known_element = message_history[0]
                async for msg in messages:
                    text = msg.content
                    if last_known_element != text:
                        if ctx.guild.get_member_named(str(msg.author)) != None:
                            message_history.append(str(msg.content))
                            authors.append(str(msg.author))
                            await asyncio.sleep(0.005)
                    else:
                        break

                for author in authors:
                    if author in msg_data["users"]:
                        msg_data["users"][author]["msgcount"] += 1
                        msg_data["total count"] += 1
                    else:
                        msg_data["users"][author] = {}
                        msg_data["users"][author]["msgcount"] = 1
                        msg_data["total count"] += 1

        for usr in msg_data["users"]:
            pd = float(msg_data["users"][usr]["msgcount"]) / float(msg_data["total count"])
            msg_data["users"][usr]["percent"] = round(pd * 100, 1)

        top_ten = heapq.nlargest(
            20,
            [
                (x, msg_data["users"][x][y])
                for x in msg_data["users"]
                for y in msg_data["users"][x]
                if (y == "percent" and msg_data["users"][x][y] > 0)
            ],
            key=lambda x: x[1],
        )
        others = 100 - sum(x[1] for x in top_ten)
        chart = await self.create_chart(top_ten, others, channel)
        await ctx.send(file=discord.File(chart, "chart.png"))

    @commands.command()
    async def sendcountchart(self, ctx):
        async with self.config.guild(ctx.guild).guild_messages() as message_history:
            await ctx.send("Total messages: {}".format(str(len(message_history))))
        
    @commands.command()
    async def emptycountchart(self, ctx):
        empty = []
        await self.config.guild(ctx.guild).guild_messages.set(empty)
        await self.config.guild(ctx.guild).guild_authors.set(empty)