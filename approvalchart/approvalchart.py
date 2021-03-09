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


class Approvalchart(commands.Cog):
    """Show approvals."""
    
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=13121312131213121312, force_registration=True)

    @staticmethod
    async def create_chart(top, channel):
        plt.clf()
        sizes = [x[1] for x in top]
        labels = ["{} {:g}%".format(x[0], x[1]) for x in top]
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
        """Generates a pie chart, representing all the approvals in the approvals channel."""
        
        channel = ctx.guild.get_channel(779971763999342653)
        messages = channel.history(limit = 1000000)
        
        authors = []
        
        msg_data = {"total count": 0, "users": {}}
        async for msg in messages:
            authors.append(str(msg.mentions[0].name))
            await asyncio.sleep(0.005)

        for author in authors:
            if author in msg_data["users"]:
                msg_data["users"][author]["msgcount"] += 1
                msg_data["total count"] += 1
            else:
                msg_data["users"][author] = {}
                msg_data["users"][author]["msgcount"] = 1
                msg_data["total count"] += 1

        top_ten = heapq.nlargest(
            20,
            [
                (x, msg_data["users"][x][y])
                for x in msg_data["users"]
                for y in msg_data["users"][x]
                if (y == "msgcount" and msg_data["users"][x][y] > 0)
            ]
        )
        chart = await self.create_chart(top_ten, channel)
        await ctx.send(file=discord.File(chart, "chart.png"))