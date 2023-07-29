from .bookstack import Bookstack


async def setup(bot):
    await bot.add_cog(Bookstack())