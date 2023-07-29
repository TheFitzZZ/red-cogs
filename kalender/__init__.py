from .kalender import Kalender


async def setup(bot):
    await bot.add_cog(Kalender(bot))