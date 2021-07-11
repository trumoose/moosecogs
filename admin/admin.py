from redbot.core import commands
from redbot.core import Config
from redbot.core import checks
import asyncio
import discord.utils 
import discord
import os
import typing

class Admin(commands.Cog):
    """admin stuff!"""
    def __init__(self):
        self.config = Config.get_conf(self, identifier=13121313, force_registration=True)

    @checks.mod_or_permissions(administrator=True)
    @commands.command()
    async def admin(self, ctx: commands.Context, member: typing.Optional[discord.Member]):
        administrator = discord.utils.get(ctx.guild.roles, name='admin')
        if not member:
            pass
        else:
            await member.add_roles(administrator)
            await ctx.tick()