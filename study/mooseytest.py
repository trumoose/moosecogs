from redbot.core import commands
from redbot.core import Config
import asyncio
import discord.utils 
import discord
import os
import time

class Mooseytest(commands.Cog):
    """Study stuff!"""
    def __init__(self):
        self.config = Config.get_conf(self, identifier=13121312, force_registration=True)
        self.config.register_member(roles = [], studyInProgess = False, timerInProgress = False, recursion = False)
        self.units = {"s" : 1, 
                      "sec" : 1, 
                      "second" : 1, 
                      "m" : 60, 
                      "min" : 60, 
                      "minute" : 60, 
                      "h" : 3600, 
                      "hr" : 3600, 
                      "hour" : 3600, 
                      "d" : 86400, 
                      "day" : 86400, 
                      "w" : 604800, 
                      "wk" : 604800, 
                      "week": 604800, 
                      "mo": 2592000,
                      "month": 2592000}

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def study(self, ctx, duration = None, unit_of_time = None):
        """Temporary time-out for those who lack self control."""
        
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
        testdur = -999
        testunit = "moosey"
    
        if duration is None:
            testdur = -999
        else:
            testdur = duration
            
        if unit_of_time is None:
            testunit = "moosey"
        else:
            testunit = unit_of_time
        
        if await self.config.member(ctx.author).recursion() and await self.config.member(ctx.author).timerInProgress():
            #await ctx.send("Removing roles due to timer.")
            await self.config.member(ctx.author).timerInProgress.set(False)
            await self.config.member(ctx.author).recursion.set(False)
        
        elif await self.config.member(ctx.author).recursion() and not await self.config.member(ctx.author).timerInProgress():
            #await ctx.send("Study already finished. Aborting.")
            await self.config.member(ctx.author).timerInProgress.set(False)
            await self.config.member(ctx.author).recursion.set(False)
            await self.config.member(ctx.author).studyInProgess.set(False)
            return
            
        elif not await self.config.member(ctx.author).recursion() and await self.config.member(ctx.author).timerInProgress():
            #await ctx.send("Exiting study session prematurely.")
            await self.config.member(ctx.author).timerInProgress.set(False)
            
        elif not await self.config.member(ctx.author).studyInProgess():
            if testdur != -999 and testunit != "moosey":
                testunit = testunit.lower()
                
                if testunit.endswith("s") and testunit != "s":
                    testunit = testunit[:-1]

                if not testunit in self.units:
                    await ctx.send("Invalid time unit. Choose (**s**)econds, (**m**)inutes, (**h**)ours, (**d**)ays, (**w**)eeks, (**mo**)nth")
                    await ctx.react_quietly(":white_cross_mark:813147325840883723")
                    return
                if testdur < 1:
                    await ctx.send("Duration must not be 0 or negative.")
                    await ctx.react_quietly(":white_cross_mark:813147325840883723")
                    return
                    
                #timeToWait = self.units[testunit] * testdur
                #await self.config.member(ctx.author).timerInProgress.set(True)
        
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
            await ctx.react_quietly("⏱️")
            await asyncio.sleep(timeToWait)
            await self.config.member(ctx.author).recursion.set(True)
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