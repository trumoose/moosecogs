from redbot.core import commands
from redbot.core import Config

class Mooseytest(commands.Cog):
    """moosey test"""
    def __init__(self):
        self.config = Config.get_conf(self, identifier=131213121312)
        self.config.register_user(roles = [])

    @commands.command()
    async def mooseytest(self, ctx):
        """moosey test!"""
        await ctx.send("mooseytest")
        
    @commands.command
    async def study(self, ctx):
        """Removes all other roles for studying."""
        
        author = ctx.author
        roles = self.config.user(author).roles
        
        if 817614968127881236 in author.roles:
            for r in roles:
                await author.add_roles(r)
                await roles.remove(r)
            await author.remove_roles(817614968127881236)
            ctx.send('{0} has finished studying!'.format(ctx.author))
        else:
            for r in author.roles:
                await roles.append(r)
                await author.remove_roles(r)
            await author.add_roles(817614968127881236)
            ctx.send('{0} has been sent to study purgatory!'.format(ctx.author))
        
        self.config.user(author).roles = roles
