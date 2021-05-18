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
        
        # finds role named "study" in the server
        studying = discord.utils.get(ctx.guild.roles, name='study')

        """
        This cog works by adding the user's roles to an array stored by the bot, which is saved until the user calls the command again.
        Unfortunately, there are default/hidden/unassignable roles that cannot be added or removed, and throw an exception when the bot tries to add them back.
        Thus, we must get these roles by their reference ID (different for every server) and remove them manually from the roles array before applying the roles back.
        """
        
        # hardcoded values, dependant on the server :/
        everyone1 = ctx.guild.get_role(776052319271911434)
        everyone2 = ctx.guild.get_role(766870004086865930)
        serverbooster = ctx.guild.get_role(767011709155672095)
        botwrangler = ctx.guild.get_role(768348291527737345)
        
        # this is the stored array of roles we want to reapply, NOT the roles that the user currently has. only applicable if calling to unstudy.
        userroles = ctx.author.roles
        
        # removing the default roles from this array before we go to re-add them
        if everyone1 in userroles:
            userroles.remove(everyone1)
        if everyone2 in userroles:
            userroles.remove(everyone2)
        if serverbooster in userroles:
            userroles.remove(serverbooster)
        if botwrangler in userroles:
            userroles.remove(botwrangler)

        # this is the array we will populate with the user's current roles, if not calling to unstudy
        roleArray = 
        
        # variable initializion for the time to study for
        timeToWait = 0
        
        # for some reason the bot freaks out if the parameters are unitialized, so we set up some default initializations to check against
        testdur = -1
        testunit = "default"
    
        # if the user passes parameters for the time to study for...
        if unit_of_time == None and duration is not None:
            testdur = "".join([i for i in duration if not i.isalpha()])
            testunit = "".join([i for i in duration if i.isalpha()])
            
        # otherwise, the user typed something in for the time and duration
        elif duration != None:
            testdur = duration    
        if unit_of_time != None:
            testunit = unit_of_time
        
        # reset user variables after studying with timer
        if await self.config.member(ctx.author).recursion() and await self.config.member(ctx.author).timerInProgress():
            await self.config.member(ctx.author).timerInProgress.set(False)
            await self.config.member(ctx.author).recursion.set(False)
        
        # reset user variables if the user stopped their studying manually before their timer was up
        elif await self.config.member(ctx.author).recursion() and not await self.config.member(ctx.author).timerInProgress():
            await self.config.member(ctx.author).timerInProgress.set(False)
            await self.config.member(ctx.author).recursion.set(False)
            return
            
        # reset user variables normally when the user calls the command manually
        elif not await self.config.member(ctx.author).recursion() and await self.config.member(ctx.author).timerInProgress():
            await self.config.member(ctx.author).timerInProgress.set(False)
            await self.config.member(ctx.author).recursion.set(False)
            
        # if the user is not currently studying that means they want to study :)
        elif not await self.config.member(ctx.author).studyInProgess():
            # check if the durations are NOT set to default values, in which case the user wants to study for a certain amount of time
            if testdur != -1 and testunit != "default":
            
                # sanitizing inputs...
                testunit = testunit.lower()
                if testunit.endswith("s") and testunit != "s":
                    testunit = testunit[:-1]

                # error handling, etc.
                if not testunit in self.units:
                    await ctx.send("Invalid time unit. Choose (**s**)econds, (**m**)inutes, (**h**)ours, (**d**)ays, (**w**)eeks, (**mo**)nth")
                    await ctx.react_quietly(":white_cross_mark:813147325840883723")
                    return
                if int(testdur) < 1:
                    await ctx.send("Must not be 0 or negative.")
                    await ctx.react_quietly(":white_cross_mark:813147325840883723")
                    return
                    
                # set up the time and set the user is studying for
                timeToWait = self.units[str(testunit)] * int(testdur)
                await self.config.member(ctx.author).timerInProgress.set(True)
        
        # get a list of all the users roles
        async with self.config.member(ctx.author).roles() as roles:
            # if the user HAS the studying role...
            if studying in ctx.author.roles:
                # if the user somehow has the studying role but isn't internally marked as studying, something went wrong (added the role manually, maybe?)
                if not await self.config.member(ctx.author).studyInProgess():
                    await ctx.send("You're not currently studying. Did something go wrong?")
                    await ctx.react_quietly(":white_cross_mark:813147325840883723")
                # otherwise, we can proceed with unstudying
                else:
                    # add each of the user's STORED ROLES to a new array of roles
                    for r in roles:
                        try:
                            roleToAdd = discord.utils.get(ctx.guild.roles, id=r)
                            roleArray.append(roleToAdd)
                        except:
                            await ctx.send('Could not get role {}'.format(roleToAdd.name))
                    # add the hardcoded default roles to the array, if they exist on the user
                    if serverbooster in ctx.author.roles:
                        roleArray.append(serverbooster)
                    if botwrangler in ctx.author.roles:
                        roleArray.append(botwrangler)
                    # discord rate limits the amount of roles we can add one at a time, so we do it all at once by changing the user's role array to the one we just created
                    await ctx.author.edit(roles=roleArray)
                    # remove the studying role from the user/change internal studying boolean
                    await ctx.author.remove_roles(studying)
                    await self.config.member(ctx.author).studyInProgess.set(False)
                    await ctx.tick()
            # if the user does NOT have the studying role...
            elif not studying in ctx.author.roles:
                # empty the bot's stored roles 
                roles.clear()
                # add all the user's current roles to the bot's storage
                for r in userroles:
                    roles.append(r.id)
                # if the user has a special role, we need to make sure they keep it. otherwise, we just clear their roles
                if serverbooster in ctx.author.roles:
                    await ctx.author.edit(roles=[serverbooster])
                elif botwrangler in ctx.author.roles:
                    await ctx.author.edit(roles=[botwrangler])
                else:
                    await ctx.author.edit(roles=[])
                # add the studying role to the user/change internal studying boolean
                await ctx.author.add_roles(studying)
                await self.config.member(ctx.author).studyInProgess.set(True)
                # check if the user typed in a time to study for...
                if not await self.config.member(ctx.author).timerInProgress():
                    await ctx.react_quietly("📝")
        
        # if the user typed in a time...
        if await self.config.member(ctx.author).timerInProgress():
            await ctx.react_quietly("⏱️")
            # sleep for the amount of time
            await asyncio.sleep(timeToWait)
            # recursively call the study command, which will remove the user's roles
            await self.config.member(ctx.author).recursion.set(True)
            await self.study(ctx)
            await ctx.tick()
            
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