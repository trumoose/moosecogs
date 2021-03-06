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

        if studying in ctx.author.roles:
            async with self.config.user(ctx.author).roles() as roles:
                #await ctx.author.add_roles(*roles)
                roles.clear()
                await ctx.tick()
            #await ctx.author.remove_roles(studying)
            #await ctx.send('{0} has finished studying!'.format(ctx.author.name))
        else:
            async with self.config.user(ctx.author).roles() as roles:
                for r in ctx.author.roles:
                    roles.append(r.id)
                #await ctx.author.remove_roles(*roles)
                await ctx.tick()
            #await ctx.author.add_roles(studying)
            #await ctx.send('{0} has been sent to study purgatory!'.format(ctx.author.name))
        
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