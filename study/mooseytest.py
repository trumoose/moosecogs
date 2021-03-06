from redbot.core import commands
from redbot.core import Config
import discord.utils 
import discord

class Mooseytest(commands.Cog):
    """moosey test"""
    def __init__(self):
        self.config = Config.get_conf(self, identifier=131213121312, force_registration=True)
        self.config.register_member(roles = [], studyInProgess = False)

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def study(self, ctx):
        """Removes all other roles for studying."""
        
        studying = discord.utils.get(ctx.guild.roles, name='study')

        everyone1 = ctx.guild.get_role(776052319271911434)
        everyone2 = ctx.guild.get_role(766870004086865930)
        userroles = ctx.author.roles
        if everyone1 in userroles:
            userroles.remove(everyone1)
            
        if everyone2 in userroles:
            userroles.remove(everyone2)

        roleArray = []
        
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
                    await ctx.author.add_roles(*roleArray)
                    roles.clear()
                    await ctx.author.remove_roles(studying)
                    await ctx.send('**{0}** has finished studying!'.format(ctx.author.name))
                    await ctx.tick()
            else:
                for r in userroles:
                    roles.append(r.id)
                await ctx.author.edit(roles=[])
                await ctx.author.add_roles(studying)
                await ctx.send('**{0}** has been sent to study purgatory!'.format(ctx.author.name))
                await self.config.member(ctx.author).studyInProgess.set(True)
                await ctx.tick()

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