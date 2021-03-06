from redbot.core import commands
from redbot.core import Config
import discord.utils 

class Mooseytest(commands.Cog):
    """moosey test"""
    def __init__(self):
        self.config = Config.get_conf(self, identifier=131213121312)
        self.config.register_user(roles = [])

    @commands.command()
    async def mooseytest(self, ctx):
        """moosey test!"""
        await ctx.send("mooseytest")
        
    @commands.command()
    async def study(self, ctx):
        """Removes all other roles for studying."""
        
        author = ctx.author
        store_roles = self.config.user(author).roles
        studying = discord.utils.get(ctx.guild.roles, name='study')

        if studying in author.roles:
            await author.add_roles(*store_roles)
            for r in store_roles:
                await store_roles.remove(r)
            await author.remove_roles(studying)
            ctx.send('{0} has finished studying!'.format(ctx.author))
        else:
            for r in author.roles:
                await store_roles.append(r)
            await author.remove_roles(*store_roles)
            await author.add_roles(studying)
            ctx.send('{0} has been sent to study purgatory!'.format(ctx.author))
        
        self.config.user(author).roles = store_roles
        
    @commands.command()
    async def printallroles(self, ctx):
        """moosey test!"""
        out = ""
        for r in ctx.author.roles:
            out += str(r) + "\n"
        ctx.send('{}'.format(out))
        
    @commands.command()
    async def printstudyrolectx(self, ctx):
        """moosey test!"""
        
        studying = discord.utils.get(ctx.guild.roles, name='study')
        
        ctx.send('{}'.format(studying))
        
    @commands.command()
    async def printstudyrole(self, ctx):
        """moosey test!"""
        
        studying = discord.utils.get(guild.roles, name='study')
        
        ctx.send('{}'.format(studying))
        
    @commands.command()
    async def addstudystring(self, ctx):
        """moosey test!"""
        
        studying = discord.utils.get(ctx.guild.roles, name='study')
        
        await ctx.author.add_roles(studying)
        
        if studying in ctx.author.roles:
            ctx.send('Added study role!')
            
    @commands.command()
    async def addstudystringctx(self, ctx):
        """moosey test!"""
        
        studying = discord.utils.get(guild.roles, name='study')
        
        await ctx.author.add_roles(studying)
        
        if studying in ctx.author.roles:
            ctx.send('Added study role!')
        
    @commands.command()
    async def addstudyid(self, ctx):
        """moosey test!"""
        
        await ctx.author.add_roles(817614968127881236)
        
        if 817614968127881236 in ctx.author.roles:
            ctx.send('Added study role!')