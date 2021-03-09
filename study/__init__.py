from .mooseytest import Mooseytest
from .mooseytest import Countchart

def setup(bot):
    bot.add_cog(Mooseytest())
    bot.add_cog(Countchart())