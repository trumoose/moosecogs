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
    async def create_approvalchart(top):
        plt.clf()
        sizes = []
        labels  = []
        for x in top:
            usr = x[0] + " (" + str(x[1]) + ")"
            labels.append(usr)
            sizes.append(x[1])
        title = plt.title("Approvals  ", color="white", fontsize=15)
        title.set_va("top")
        title.set_ha("center")
        plt.gca().axis("equal")
        cmap = plt.cm.turbo
        reversed_cmap = cmap.reversed()
        colors = reversed_cmap(np.linspace(0., 1., 21))
        pie = plt.pie(sizes, colors=colors, startangle=0)
        plt.legend(
            pie[0],
            labels,
            bbox_to_anchor=(0.7, 0.5),
            loc="center",
            fontsize=8,
            bbox_transform=plt.gcf().transFigure,
            facecolor="#ffffff",
        )
        plt.subplots_adjust(left=0.0, bottom=0.0, right=0.52)
        image_object = BytesIO()
        plt.savefig(image_object, format="PNG", facecolor="#36393E")
        image_object.seek(0)
        return image_object
        
    @commands.command()
    async def approvals(self, ctx):
        """Generates a pie chart, representing all the approvals in the approvals channel."""
        
        channel1 = ctx.guild.get_channel(779971763999342653)
        messages = channel1.history(limit = 1000000)
        
        authors = []
        count = 0
        users = {}
        await ctx.channel.trigger_typing()
        async for msg in messages:
            usr = (msg.content).split()[0]
            usr2 = re.sub('[^0-9]','', usr)
            usr3 = discord.utils.get(ctx.guild.members, id=int(usr2))
            if usr3 is not None:
                authors.append(usr3.name)
            await asyncio.sleep(0.005)

        for author in authors:
            if author in users:
                users[author] += 1
            else:
                users[author] = 1
                
        top = sorted(users.items(), key=lambda x: x[1], reverse=True)
        chart = await self.create_approvalchart(top)
        await ctx.send(file=discord.File(chart, "chart.png"))
        
    @commands.command()
    async def bans(self, ctx):
        """Generates a pie chart, representing all the bans in the modlog channel."""
        
        channel1 = ctx.guild.get_channel(774884417746501633)
        messages = channel1.history(limit = 2)
        
        authors = []
        count = 0
        users = {}
        #await ctx.channel.trigger_typing()
        print("Hello 1")
        async for msg in messages:
            print("Hello 2")
            embeds = msg.embeds
            for embed in embeds:
                print(embed.to_dict())
            #usr = (msg.content).split()[0]
            #usr2 = re.sub('[^0-9]','', usr)
            #usr3 = discord.utils.get(ctx.guild.members, id=int(usr2))
            #if usr3 is not None:
                #authors.append(usr3.name)
            await asyncio.sleep(0.005)

        #for author in authors:
            #if author in users:
                #users[author] += 1
            #else:
                #users[author] = 1
                
        #top = sorted(users.items(), key=lambda x: x[1], reverse=True)
        #chart = await self.create_approvalchart(top)
        #await ctx.send(file=discord.File(chart, "chart.png"))