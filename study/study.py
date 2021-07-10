from redbot.core import commands
from redbot.core import Config
from redbot.core import checks
import asyncio
import discord.utils 
import discord
import os
import typing
import time

class Study(commands.Cog):
    """Study stuff!"""
    def __init__(self):
        self.config = Config.get_conf(self, identifier=13121312, force_registration=True)
        self.config.register_member(roles = [], studyInProgess = False, timerInProgress = False, recursion = False, timeStudying = -999, unitStudying = "moose")
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
        unstudying = discord.utils.get(ctx.guild.roles, name='unstudy')
        everyone1 = ctx.guild.get_role(776052319271911434)
        serverbooster = ctx.guild.get_role(767011709155672095)
        botwrangler = ctx.guild.get_role(768348291527737345)
        everyone2 = ctx.guild.get_role(766870004086865930)
        muradok = ctx.guild.get_role(824759479357931530)
        
        userroles = ctx.author.roles
        if everyone1 in userroles:
            userroles.remove(everyone1)
            
        if everyone2 in userroles:
            userroles.remove(everyone2)
            
        if serverbooster in userroles:
            userroles.remove(serverbooster)
            
        if botwrangler in userroles:
            userroles.remove(botwrangler)

        roleArray = []
        timeToWait = 0
        testdur = 999
        testunit = "moosey"
    
        if unit_of_time == None and duration is not None:
            testdur = "".join([i for i in duration if not i.isalpha()])
            testunit = "".join([i for i in duration if i.isalpha()])
            
        elif duration != None:
            testdur = duration
            
        if unit_of_time != None:
            testunit = unit_of_time
        
        time_spent_studying = await self.config.member(ctx.author).timeStudying()
        unit_spent_studying = await self.config.member(ctx.author).unitStudying()
        
        if await self.config.member(ctx.author).recursion() and await self.config.member(ctx.author).timerInProgress():
            #await ctx.send("**{}** has finished studying after {} {}.".format(ctx.author.name, time_spent_studying, unit_spent_studying))
            await self.config.member(ctx.author).timerInProgress.set(False)
            await self.config.member(ctx.author).recursion.set(False)
        
        elif await self.config.member(ctx.author).recursion() and not await self.config.member(ctx.author).timerInProgress():
            #await ctx.send("Study already finished. Aborting.")
            await self.config.member(ctx.author).timerInProgress.set(False)
            await self.config.member(ctx.author).recursion.set(False)
            return
            
        elif not await self.config.member(ctx.author).recursion() and await self.config.member(ctx.author).timerInProgress():
            #await ctx.send("**{}** has finished studying.".format(ctx.author.name))
            await self.config.member(ctx.author).timerInProgress.set(False)
            await self.config.member(ctx.author).recursion.set(False)
            
        elif not await self.config.member(ctx.author).studyInProgess():
            if testdur != -999 and testunit != "moosey":
                testunit = testunit.lower()
                
                if testunit.endswith("s") and testunit != "s":
                    testunit = testunit[:-1]

                if not testunit in self.units:
                    await ctx.send("Invalid time unit. Choose (**s**)econds, (**m**)inutes, (**h**)ours, (**d**)ays, (**w**)eeks, (**mo**)nth")
                    await ctx.react_quietly(":white_cross_mark:813147325840883723")
                    return
                    
                if int(testdur) < 1:
                    await ctx.send("Must not be 0 or negative.")
                    await ctx.react_quietly(":white_cross_mark:813147325840883723")
                    return
                    
                timeToWait = self.units[str(testunit)] * int(testdur)
                await self.config.member(ctx.author).timerInProgress.set(True)
        
        async with self.config.member(ctx.author).roles() as roles:
            if unstudying not in ctx.author.roles and friendlychat not in ctx.author.roles:
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
                        if botwrangler in ctx.author.roles:
                            roleArray.append(botwrangler)
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
                    elif botwrangler in ctx.author.roles:
                        await ctx.author.edit(roles=[botwrangler])
                    else:
                        await ctx.author.edit(roles=[])
                    await ctx.author.add_roles(studying)
                    await self.config.member(ctx.author).studyInProgess.set(True)
                    if not await self.config.member(ctx.author).timerInProgress():
                        await ctx.react_quietly("📝")
                
        if await self.config.member(ctx.author).timerInProgress():
            await ctx.react_quietly("⏱️")
            await self.config.member(ctx.author).timeStudying.set(testdur)
            await self.config.member(ctx.author).unitStudying.set(testunit)
            await asyncio.sleep(timeToWait)
            await self.config.member(ctx.author).recursion.set(True)
            await self.study(ctx)
            await ctx.tick()

        if ctx.author.id == 544696202311106571:
        	await ctx.author.add_roles(muradok)
    
    @checks.mod_or_permissions(manage_messages=True)
    @commands.command()
    async def unstudy(self, ctx: commands.Context, member: typing.Optional[discord.Member]):
        studying = discord.utils.get(ctx.guild.roles, name='study')
        unstudying = discord.utils.get(ctx.guild.roles, name='unstudy')
        everyone1 = ctx.guild.get_role(776052319271911434)
        serverbooster = ctx.guild.get_role(767011709155672095)
        botwrangler = ctx.guild.get_role(768348291527737345)
        everyone2 = ctx.guild.get_role(766870004086865930)
        muradok = ctx.guild.get_role(824759479357931530)
        
        roleArray = []
        
        async with self.config.member(member).roles() as roles:
            if studying in member.roles:
                if not await self.config.member(member).studyInProgess():
                    await ctx.send("That person doesn't appear to be studying.")
                    await ctx.react_quietly(":white_cross_mark:813147325840883723")
                else:
                    for r in roles:
                        try:
                            roleToAdd = discord.utils.get(ctx.guild.roles, id=r)
                            roleArray.append(roleToAdd)
                        except:
                            await ctx.send('Could not get role {}'.format(roleToAdd.name))
                    if serverbooster in member.roles:
                        roleArray.append(serverbooster)
                    if botwrangler in member.roles:
                        roleArray.append(botwrangler)
                    await member.edit(roles=roleArray)
                    await member.remove_roles(studying)
                    await self.config.member(member).studyInProgess.set(False)
                    await ctx.tick()
            else:
                await ctx.send("That person doesn't appear to be studying.")
                
            await member.add_roles(unstudying)
                
    @checks.mod_or_permissions(manage_messages=True)
    @commands.command()
    async def friendlychat(self, ctx: commands.Context, member: typing.Optional[discord.Member]):
        friendlychat = discord.utils.get(ctx.guild.roles, name='friendly-chat')
        unstudying = discord.utils.get(ctx.guild.roles, name='unstudy')
        serverbooster = ctx.guild.get_role(767011709155672095)
        everyone1 = ctx.guild.get_role(776052319271911434)
        everyone2 = ctx.guild.get_role(766870004086865930)
        userroles = member.roles
        if everyone1 in userroles:
            userroles.remove(everyone1)
            
        if everyone2 in userroles:
            userroles.remove(everyone2)
            
        if serverbooster in userroles:
            userroles.remove(serverbooster)
            
        roleArray = []
        
        async with self.config.member(member).roles() as roles:
            if friendlychat not in member.roles:
                if unstudying not in member.roles:
                    await ctx.send("Please use .unstudy first!")
                else:
                    for r in roles:
                        try:
                            roleToAdd = discord.utils.get(ctx.guild.roles, id=r)
                            roleArray.append(roleToAdd)
                        except:
                            await ctx.send('Could not get role {}'.format(roleToAdd.name))
                    if serverbooster in ctx.author.roles:
                        roleArray.append(serverbooster)
                    await member.edit(roles=roleArray)
                    await member.remove_roles(friendlychat)
                    await ctx.tick()
            else:
                roles.clear()
                for r in userroles:
                    roles.append(r.id)
                if serverbooster in ctx.author.roles:
                    await ctx.author.edit(roles=[serverbooster])
                else:
                    await ctx.author.edit(roles=[])
                await member.add_roles(friendlychat)
                await ctx.tick()
                
                
        
    @checks.mod_or_permissions(manage_messages=True)
    @commands.command()
    async def unfriendlychat(self, ctx: commands.Context, member: typing.Optional[discord.Member]):
        friendlychat = discord.utils.get(ctx.guild.roles, name='friendly-chat')
        await member.remove_roles(friendlychat)
        await ctx.tick()
    
    @checks.mod_or_permissions(manage_messages=True)
    @commands.command()
    async def appendmyroles(self, ctx):
        async with self.config.member(ctx.author).roles() as roles:
            for r in ctx.author.roles:
                roles.append(r.id)
            await ctx.tick()

    @checks.mod_or_permissions(manage_messages=True)
    @commands.command()
    async def printmyroles(self, ctx):
        async with self.config.member(ctx.author).roles() as roles:
            for r in roles:
                await ctx.send('roleid: {}'.format(r))
            await ctx.tick()
            
    @checks.mod_or_permissions(manage_messages=True)
    @commands.command()
    async def addstudyroles(self, ctx):
        studying = discord.utils.get(ctx.guild.roles, name='study')

        everyone1 = ctx.guild.get_role(776052319271911434)
        serverbooster = ctx.guild.get_role(767011709155672095)
        botwrangler = ctx.guild.get_role(801850754565537874)
        everyone2 = ctx.guild.get_role(766870004086865930)
        roleArray = []
        async with self.config.member(ctx.author).roles() as roles:
            for r in roles:
                try:
                    roleToAdd = discord.utils.get(ctx.guild.roles, id=r)
                    roleArray.append(roleToAdd)
                except:
                    await ctx.send('Could not get role {}'.format(roleToAdd.name))
            if serverbooster in ctx.author.roles:
                roleArray.append(serverbooster)
            if botwrangler in ctx.author.roles:
                roleArray.append(botwrangler)
            await ctx.author.edit(roles=roleArray)
            await ctx.author.remove_roles(studying)
            await self.config.member(ctx.author).studyInProgess.set(False)
            await ctx.tick()
            
    @checks.mod_or_permissions(manage_messages=True)
    @commands.command()
    async def resetall(self, ctx, member: typing.Optional[discord.Member]):
        if not member:
            member = ctx.author
        await self.config.member(member).recursion.set(False)
        await self.config.member(member).studyInProgess.set(False)
        await self.config.member(member).timerInProgress.set(False)
        async with self.config.member(member).roles() as roles:
            roles.clear()
            
    @checks.mod_or_permissions(manage_messages=True)
    @commands.command()
    async def studydebug(self, ctx, member: typing.Optional[discord.Member]):
        if not member:
            member = ctx.author
        e = discord.Embed(colour=member.color)
        e.set_author(name=f"{member.name}", icon_url=member.avatar_url)
        e.set_footer(text=f"{member.name}#{member.discriminator} ({member.id})")
        e.set_thumbnail(url=member.avatar_url)
        e.add_field(name="Studying:", value=str(await self.config.member(member).studyInProgess()))
        await ctx.send(embed=e)