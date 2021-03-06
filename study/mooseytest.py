from redbot.core import commands
from redbot.core import Config
import discord.utils 
import discord

class Mooseytest(commands.Cog):
    """moosey test"""
    def __init__(self):
        self.config = Config.get_conf(self, identifier=131213121312)
        self.config.register_user(userroles = [])

    @commands.command()
    async def mooseytest(self, ctx):
        """moosey test!"""
        await ctx.send("mooseytest")
        
    @commands.command()
    async def study(self, ctx):
        """Removes all other roles for studying."""
       
        author = ctx.author
        store_roles = await self.config.user(author).userroles()
        studying = await discord.utils.get(ctx.guild.roles, name='study')

        if studying in author.roles:
            await author.add_roles(*store_roles)
            for r in store_roles:
                await store_roles.remove(r)
            await author.remove_roles(studying)
            await ctx.send('{0} has finished studying!'.format(author.name))
        else:
            for r in author.roles:
                await store_roles.append(r)
            await author.remove_roles(*store_roles)
            await author.add_roles(studying)
            await ctx.send('{0} has been sent to study purgatory!'.format(author.name))
        
        await self.config.user(author).userroles.set(store_roles)
        
    @commands.command()
    async def printallroles(self, ctx):
        """moosey test!"""
        out = ""
        for r in ctx.author.roles:
            out += str(r.name) + "\n"
        await ctx.send('{}'.format(out))
        
    @commands.command()
    async def printstudyrole(self, ctx):
        """moosey test!"""
        
        studying = discord.utils.get(ctx.guild.roles, name='study')
        
        await ctx.send('{}'.format(studying.name))
        
    @commands.command()
    async def addstudystring(self, ctx):
        """moosey test!"""
        
        studying = discord.utils.get(ctx.guild.roles, name='study')
        
        await ctx.author.add_roles(studying)
        
        if studying in ctx.author.roles:
            await ctx.send('Added study role!')
            
    @commands.command()
    async def checkstudying(self, ctx):
        """moosey test!"""
        
        studying = discord.utils.get(ctx.guild.roles, name='study')

        if studying in ctx.author.roles:
            await ctx.send('{} is studying hard!'.format(ctx.author.name))
            
    @commands.command()
    async def printguildname(self, ctx):
        await ctx.send('Guild name: {}'.format(ctx.guild.name))

    @commands.command()
    async def printmyname(self, ctx):
        await ctx.send('Hi {}!'.format(ctx.author.name))
    
    @commands.command()
    async def appendmyroles(self, ctx):
        user_group = self.config.user(ctx.author)
        async with user_group.userroles() as userroles:
            userroles = ctx.author.roles;
            for r in userroles:
                await ctx.send('userroles: {}.'.format(r.name))
        myroles = await self.config.user(ctx.author).userroles()
        await ctx.send('len: {}.'.format(str(len(myroles))))
        
    @commands.command()
    async def removemyroles(self, ctx):
        myroles = []
        user_group = self.config.user(ctx.author)
        async with user_group.userroles() as userroles:
            userroles = myroles
    
    @commands.command()
    async def printmyroles(self, ctx):
        myroles = await self.config.user(ctx.author).userroles()
        await ctx.send('len: {}.'.format(str(len(myroles))))