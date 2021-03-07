from redbot.core import commands
from redbot.core import Config
import asyncio
import discord.utils 
import discord
import os
import time

class Mooseytest(commands.Cog):
    """moosey test"""
    def __init__(self):
        self.config = Config.get_conf(self, identifier=131213121312, force_registration=True)
        self.config.register_member(roles = [], studyInProgess = False, timerInProgress = False)
        self.units = {"s" : 1, "second" : 1, "m" : 60, "minute" : 60, "hour" : 3600, "h" : 3600, "day" : 86400, "d" : 86400, "week": 604800, "w" : 604800, "month": 2592000, "mo": 2592000}

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def study(self, ctx, quantity = -999, time_unit = "moosey"):
        """Removes all other roles for focusing."""
        
        studying = discord.utils.get(ctx.guild.roles, name='study')

        everyone1 = ctx.guild.get_role(776052319271911434)
        serverbooster = ctx.guild.get_role(767011709155672095)
        everyone2 = ctx.guild.get_role(766870004086865930)
        
        userroles = ctx.author.roles
        if everyone1 in userroles:
            userroles.remove(everyone1)
            
        if everyone2 in userroles:
            userroles.remove(everyone2)
            
        if serverbooster in userroles:
            userroles.remove(serverbooster)

        roleArray = []
        timeToWait = 0
    
        if await self.config.member(ctx.author).timerInProgress():
            await ctx.send("Restoring roles.")
            await self.config.member(ctx.author).timerInProgress.set(False)
            
        elif not await self.config.member(ctx.author).studyInProgess():
            if quantity != -999 or time_unit != "moosey":
                time_unit = time_unit.lower()
                
                s = ""
                if time_unit.endswith("s"):
                    time_unit = time_unit[:-1]
                    s = "s"

                if not time_unit in self.units:
                    await ctx.send("Invalid time unit. Choose (**m**)inutes/(**h**)ours/(**d**)ays/(**w**)eeks/(**mo**)nth")
                    return
                if quantity < 1:
                    await ctx.send("Quantity must not be 0 or negative.")
                    return
                    
                timeToWait = self.units[time_unit] * quantity
                await self.config.member(ctx.author).timerInProgress.set(True)
        
        async with self.config.member(ctx.author).roles() as roles:
            if studying in ctx.author.roles:
                if not await self.config.member(ctx.author).studyInProgess():
                    await ctx.send("You're not currently studying. Did something go wrong?")
                    await ctx.react_quietly(":white_cross_mark:813147325840883723")
                else:
                    for r in roles:
                        try:
                            roleToAdd = discord.utils.get(ctx.guild.roles, id=r)
                            roleArray.append(roleToAdd)
                        except:
                            await ctx.send('Could not get role {}'.format(roleToAdd.name))
                    if serverbooster in ctx.author.roles:
                        roleArray.append(serverbooster)
                    await ctx.author.edit(roles=roleArray)
                    await ctx.author.remove_roles(studying)
                    await self.config.member(ctx.author).studyInProgess.set(False)
                    await ctx.tick()
            elif not studying in ctx.author.roles:
                roles.clear()
                for r in userroles:
                    roles.append(r.id)
                if serverbooster in ctx.author.roles:
                    await ctx.author.edit(roles=[serverbooster])
                else:
                    await ctx.author.edit(roles=[])
                await ctx.author.add_roles(studying)
                await self.config.member(ctx.author).studyInProgess.set(True)
                await ctx.tick()
                if await self.config.member(ctx.author).timerInProgress():
                    await ctx.send("Waiting for {}...".format(str(timeToWait)))
                    await asyncio.sleep(timeToWait)
                    await ctx.send("time!")
                    await self.study(ctx)

    @commands.command()
    async def appendmyroles(self, ctx):
        async with self.config.member(ctx.author).roles() as roles:
            for r in ctx.author.roles:
                roles.append(r.id)
            await ctx.tick()
    
    @commands.command()
    async def removestudy(self, ctx):
        studying = discord.utils.get(ctx.guild.roles, name='study')
        await ctx.author.remove_roles(studying)
        await self.config.member(ctx.author).studyInProgess.set(False)
        await self.config.member(ctx.author).timerInProgress.set(False)

        
    @commands.command()
    async def addadmin(self, ctx):
        studying = discord.utils.get(ctx.guild.roles, name='admin')
        await ctx.author.add_roles(studying)
        
    @commands.command()
    async def removemyroles(self, ctx):
        async with self.config.member(ctx.author).roles() as roles:
            for r in roles:
                roles.clear()
            await ctx.tick()
    
    @commands.command()
    async def printmyroles(self, ctx):
        async with self.config.member(ctx.author).roles() as roles:
            for r in roles:
                await ctx.send('roleid: {}'.format(r))
            await ctx.tick()