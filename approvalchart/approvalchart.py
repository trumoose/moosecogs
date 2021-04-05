import asyncio
import discord
import heapq
from io import BytesIO
from typing import Optional
import numpy as np
import re

import matplotlib

matplotlib.use("agg")
import matplotlib.pyplot as plt

plt.switch_backend("agg")

from redbot.core import checks, commands, Config


class Approvalchart(commands.Cog):
    """Show approvals."""
    
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=131243481312, force_registration=True)

    @staticmethod
    async def create_approvalchart(top, channel):
        plt.clf()
        sizes = []
        labels  = []
        for x, y in top[0].items():
            labels.append(x)
            sizes.append(y)
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
    async def approvalchart(self, ctx):
        """Generates a pie chart, representing all the approvals in the approvals channel."""
        
        channel = ctx.guild.get_channel(779971763999342653)
        messages = channel.history(limit = 1000000)
        
        authors = []
        count = 0
        users = {}
        await channel.trigger_typing()
        async for msg in messages:
            usr = (msg.content).split()[0]
            usr2 = re.sub('[^0-9]','', usr)
            usr3 = discord.utils.get(ctx.guild.members, id=int(usr2))
            if usr3 is not None:
                authors.append(usr3.name)
            await asyncio.sleep(0.0025)

        for author in authors:
            if author in users:
                users[author] += 1
            else:
                users[author] = 1

        print(users)
        
        #top_ten = heapq.nlargest(20, users.items(), key=lambda i: i[1])
        #chart = await self.create_approvalchart(top_ten, channel)
        #await ctx.send("generated")
        #await ctx.send(file=discord.File(chart, "chart.png"))