from .kalender import Kalender


def setup(bot):
    bot.add_cog(Kalender(bot))