from .approvalchart import Approvalchart

def setup(bot):
    bot.add_cog(Approvalchart(bot))