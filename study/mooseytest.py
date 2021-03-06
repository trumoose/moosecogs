from redbot.core import commands
from redbot.core import Config
import discord.utils 
import discord

class Mooseytest(commands.Cog):
    """moosey test"""
    def __init__(self):
        self.config = Config.get_conf(self, identifier=131213121312, force_registration=True)
        self.config.register_user(roles = [])

    @commands.command()
    async def mooseytest(self, ctx):
        """moosey test!"""
        await ctx.send("mooseytest")
        
    @commands.command()
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

        async with self.config.user(ctx.author).roles() as roles:
            if studying in ctx.author.roles:
                await ctx.author.add_roles(roles)
                roles.clear()
                await ctx.author.remove_roles(studying)
                await ctx.send('{0} has finished studying!'.format(ctx.author.name))
            else:
                for r in userroles:
                        roles.append(r.id)
                await ctx.author.edit(roles=[])
                await ctx.author.add_roles(studying)
                await ctx.send('{0} has been sent to study purgatory!'.format(ctx.author.name))
            await ctx.tick()

    @commands.command()
    async def appendmyroles(self, ctx):
        async with self.config.user(ctx.author).roles() as roles:
            for r in ctx.author.roles:
                roles.append(r.id)
            await ctx.tick()
        
    @commands.command()
    async def removemyroles(self, ctx):
        async with self.config.user(ctx.author).roles() as roles:
            for r in roles:
                roles.clear()
            await ctx.tick()
    
    @commands.command()
    async def printmyroles(self, ctx):
        async with self.config.user(ctx.author).roles() as roles:
            for r in roles:
                await ctx.send('roleid: {}'.format(r))
            await ctx.tick()