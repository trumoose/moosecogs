from redbot.core import commands
from redbot.core import Config
import discord.utils 
import discord

class Mooseytest(commands.Cog):
    """moosey test"""
    def __init__(self):
        self.config = Config.get_conf(self, identifier=131213121312, force_registration=True)
        self.config.register_member(roles = [], studyInProgess = False, timerInProgress = False)
        self.units = {"m" : 60, "minute" : 60, "hour" : 3600, "h" : 3600, "day" : 86400, "d" : 86400, "week": 604800, "w" : 604800, "month": 2592000, "mo": 2592000}

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def study(self, ctx, quantity = -999, time_unit = "moosey",):
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
        
        if await self.config.member(ctx.author).studyInProgess():
            await ctx.send("Breaking timer.")
            await self.config.member(ctx.author).timerInProgress.set(False)
                
        if quantity != -999 and time_unit != "moosey" and not await self.config.member(ctx.author).studyInProgess():
            time_unit = time_unit.lower()
            
            s = ""
            if time_unit.endswith("s"):
                time_unit = time_unit[:-1]
                s = "s"

            elif not time_unit in self.units:
                await self.bot.say("Invalid time unit! Choose (m)inutes/(h)ours/(d)ays/(w)eeks/(mo)nth")
                return
            elif quantity < 1:
                await self.bot.say("Quantity must not be 0 or negative.")
                return
            elif quantity > 0:
                await self.config.member(ctx.author).timerInProgress.set(True)
            
            seconds = self.units[time_unit] * quantity
        
        async with self.config.member(ctx.author).roles() as roles:
            if studying in ctx.author.roles:
                if not await self.config.member(ctx.author).studyInProgess():
                    await ctx.send("You're not currently studying. Did something go wrong?")
                    await ctx.react_quietly(":white_cross_mark:813147325840883723")
                else:
                    #beanMsg = await ctx.send('Unfocusing **{0}**...'.format(ctx.user.name))
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
                    #beanMsg.delete()
                    await ctx.tick()
            if not studying in ctx.author.roles:
                #beanMsg = await ctx.send('Focusing **{0}**...'.format(ctx.user.name))
                roles.clear()
                for r in userroles:
                    roles.append(r.id)
                if serverbooster in ctx.author.roles:
                    await ctx.author.edit(roles=[serverbooster])
                else:
                    await ctx.author.edit(roles=[])
                await ctx.author.add_roles(studying)
                await self.config.member(ctx.author).studyInProgess.set(True)
                #beanMsg.delete()
                await ctx.tick()
                if await self.config.member(ctx.author).timerInProgress():
                    await asyncio.sleep(seconds)
                    await self.config.member(ctx.author).timerInProgress.set(False)

    @commands.command()
    async def appendmyroles(self, ctx):
        async with self.config.member(ctx.author).roles() as roles:
            for r in ctx.author.roles:
                roles.append(r.id)
            await ctx.tick()
        
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