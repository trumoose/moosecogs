import asyncio
import discord
from redbot.core import commands
from redbot.core.utils.common_filters import filter_mass_mentions


class PressX(commands.Cog):
    """Pay some respects."""

    async def red_delete_data_for_user(self, **kwargs):
        """ Nothing to delete """
        return

    def __init__(self, bot):
        self.bot = bot
        self.channels = {}

    @commands.command()
    @commands.bot_has_permissions(add_reactions=True)
    async def pressx(self, ctx, *, user: discord.User = None):
        """Pay respects by pressing F"""
        if str(ctx.channel.id) in self.channels:
            return await ctx.send(
                "Oops! I'm still doubting in this channel, you'll have to wait until I'm done."
            )
        self.channels[str(ctx.channel.id)] = {}

        if user:
            answer = user.display_name
        else:
            await ctx.send("What do you want to doubt?")

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            try:
                pressf = await ctx.bot.wait_for("message", timeout=120.0, check=check)
            except asyncio.TimeoutError:
                del self.channels[str(ctx.channel.id)]
                return await ctx.send("You took too long to reply.")

            answer = pressf.content[:1900]

        message = await ctx.send(
            f"Press x to doubt **{filter_mass_mentions(answer)}**."
        )
        await message.add_reaction(":doubt:855722126186119208")
        self.channels[str(ctx.channel.id)] = {"msg_id": message.id, "reacted": []}
        await asyncio.sleep(120)
        try:
            await message.delete()
        except (discord.errors.NotFound, discord.errors.Forbidden):
            pass
        amount = len(self.channels[str(ctx.channel.id)]["reacted"])
        word = "person has" if amount == 1 else "people have"
        await ctx.send(f"**{amount}** {word} doubted **{filter_mass_mentions(answer)}**.")
        del self.channels[str(ctx.channel.id)]

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        print(str(reaction.emoji))
        if str(reaction.message.channel.id) not in self.channels:
            return
        if self.channels[str(reaction.message.channel.id)]["msg_id"] != reaction.message.id:
            return
        if user.id == self.bot.user.id:
            return
        if user.id not in self.channels[str(reaction.message.channel.id)]["reacted"]:
            if str(reaction.emoji) == ":doubt:855722126186119208":
                await reaction.message.channel.send(f"**{user.name}** has pressed x to doubt.")
                self.channels[str(reaction.message.channel.id)]["reacted"].append(user.id)
