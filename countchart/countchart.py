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
        self.config = Config.get_conf(self, 1312131213121312, force_registration=True)

        default_guild = {"guild_messages": []}

        self.config.register_guild(**default_guild)
"""
    @staticmethod
    async def create_chart(top, others):
        channel = discord.get_channel(id=771829982158389258)
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
"""
    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.channel)
    @commands.max_concurrency(1, commands.BucketType.channel)
    async def countchart2(self, ctx):
        """
        Generates a pie chart, representing all the messages in the countchart channel.
        """
        channel = discord.get_channel(id=771829982158389258)
        messages = 1000000

        e = discord.Embed(description="This might take a while...", colour=await self.bot.get_embed_colour(location=channel))
        em = await ctx.send(embed=e)

        message_history = await self.config.guild(ctx.guild).guild_messages()
        history_counter = 0

        async for msg in channel.history(limit=messages):
            if not msg in message_history:
                message_history.append(msg)
                history_counter += 1
                await asyncio.sleep(0.005)
                if history_counter % 250 == 0:
                    new_embed = discord.Embed(
                        description=f"This might take a while...\n{history_counter}/{messages} messages gathered",
                        colour=await self.bot.get_embed_colour(location=channel),
                    )
                    try:
                        await em.edit(embed=new_embed)
                    except discord.NotFound:
                        pass # for cases where the embed was deleted preventing the edit
                        
        await self.config.guild(ctx.guild).guild_messages.set(message_history)
"""
        msg_data = {"total count": 0, "users": {}}
        for msg in message_history:
            if len(msg.author.display_name) >= 20:
                short_name = "{}...".format(msg.author.display_name[:20]).replace("$", "\\$")
            else:
                short_name = msg.author.display_name.replace("$", "\\$").replace("_", "\\_ ").replace("*", "\\*")
            whole_name = "{}#{}".format(short_name, msg.author.discriminator)
            if msg.author.bot:
                pass
            elif whole_name in msg_data["users"]:
                msg_data["users"][whole_name]["msgcount"] += 1
                msg_data["total count"] += 1
            else:
                msg_data["users"][whole_name] = {}
                msg_data["users"][whole_name]["msgcount"] = 1
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

        try:
            await em.delete()
        except discord.NotFound:
            pass
        await ctx.send(file=discord.File(chart, "chart.png"))"""