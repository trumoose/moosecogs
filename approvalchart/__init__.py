from .countchart import Countchart

def setup(bot):
    bot.add_cog(Countchart(bot))