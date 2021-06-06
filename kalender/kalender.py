from redbot.core import Config
from redbot.core import commands
import requests
import json
import datetime
import discord
from datetime import datetime, timedelta

class Kalender(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.config = Config.get_conf(self, identifier=38586798456)
        self.bot = bot
        default_global = {
            "foobar": True,
            "dates": {
            }
        }
        default_guild = {
            "blah": [],
            "dates": {
            }
        }
        self.config.register_global(**default_global)
        self.config.register_guild(**default_guild)

  
    @commands.command()
    async def caltest(self, ctx):
        """This does stuff!"""
        # Your code will go here
        # await ctx.send("Lese Default Dict...")
        # await ctx.send("The value of dates is {}".format("True" if dates else "False"))
        

        await ctx.send("Löse Update aus...")
        await self.kalender(ctx, True)


        #################

        # await ctx.send("Löse Update aus...")
        # channel = await ctx.bot.get_shared_api_tokens("calchannelid")
        # msgid = await self.config.guild(ctx.guild).calendarmsgid()
        # await ctx.send(channel['calchannelid'])

        # channeldata = self.bot.get_channel(int(channel['calchannelid']))
        # msg = await channeldata.fetch_message(msgid)

        # em = discord.Embed(title="Aktueller Terminplan des Konvents", url="https://konvent.fitzzz.de/books/anatomie-i")
        # em.set_author(name=f"Ein neuer Kalender wird aufgehängt...")
        # em.add_field(name="Jagdausflug", value="19.02. 21 Uhr ", inline=True)

        # await msg.edit(content=None, embed=em)

        #################
        
        # dates = await self.config.guild(ctx.guild).dates()
        # for key in dates:
        #     await ctx.send("Key is "+ key)



    @commands.command()
    async def neuesevent(self, ctx: commands.Context, *ids: str):
        """Fügt ein neues Ereignis zum Kalender hinzu."""

        if not ids:
            await ctx.send('Bitte folgenden Syntax einhalten: !neuesevent "Beschreibung" "Datum/Uhrzeit" _mit_ Anführungszeichen!')
            return

        if len(ids) != 2:
            await ctx.send('Bitte folgenden Syntax einhalten: !neuesevent "Beschreibung" "Datum/Uhrzeit" _mit_ Anführungszeichen!')
            return

        try:
            is_already_item = await self.config.guild(ctx.guild).dates.get_raw(ids[0])
            if is_already_item:
                await self.config.guild(ctx.guild).dates.clear_raw(ids[0])
                await ctx.send(f"Das Ereignis {ids[0]} existiert schon.")
        except KeyError:
            await self.config.guild(ctx.guild).dates.set_raw(ids[0], value=ids[1])
            await self.kalender(ctx, True)
            await ctx.send(f"Das Ereignis {ids[0]} wurde dem Kalender hinzugefügt.")



    @commands.command()
    async def loescheevent(self, ctx: commands.Context, *id: str):
        """Löscht ein bestehendes Ereignis aus dem Kalender."""

        if not id:
            await ctx.send('Bitte folgenden Syntax einhalten: !löscheevent "Eventname"')
            return

        if len(id) != 1:
            await ctx.send('Bitte folgenden Syntax einhalten: !löscheevent "Eventname"')
            return

        try:
            is_already_item = await self.config.guild(ctx.guild).dates.get_raw(id[0])
            if is_already_item:
                await self.config.guild(ctx.guild).dates.clear_raw(id[0])
                await self.kalender(ctx, True)
                await ctx.send(f"Das Ereignis {id[0]} wurde entfernt.")

        except KeyError:
            await ctx.send(f"Das Ereignis {id[0]} nicht gefunden.")


    @commands.command()
    async def kalender(self, ctx: commands.Context, update = False):
        """This posts or updates the calendar"""

        user = ctx.message.author.name
        url = ctx.message.author.avatar_url
        url = "https://konvent.fitzzz.de/uploads/images/system/2021-04/wappen-transparent.png"
        url_link = "https://cdn.discordapp.com/emojis/595164813982826497.png?v=1"
        url_calendarlogo = "https://konvent.fitzzz.de/uploads/images/gallery/2021-06/scaled-1680-/kalender.png"

        em = discord.Embed(title="Aktueller Terminplan des Konvents", url="https://konvent.fitzzz.de/books/der-gildenkalender/page/nutzung-unseres-schreibers-scrib")
        em.set_author(name=f"*Ein Kalender ist in der Eingangshalle aufgehängt*", icon_url=url)

        dates = await self.config.guild(ctx.guild).dates()

        for key in dates:
            em.add_field(name=key, value=dates[key], inline=True)
        
        em.set_footer(text=f"Für Hilfe zur Nutzung bitte auf die Überschrift klicken.", icon_url=url_link)
        em.set_thumbnail(url=url_calendarlogo)
        
        channel = await ctx.bot.get_shared_api_tokens("calchannelid")
        channeldata = self.bot.get_channel(int(channel['calchannelid']))


        if update != True:
            calmsg = await channeldata.send(None, embed=em)
            await self.config.guild(ctx.guild).calendarmsgid.set(calmsg.id)
        
        if update == True:
            msgid = await self.config.guild(ctx.guild).calendarmsgid()
            msg = await channeldata.fetch_message(msgid)
            await msg.edit(content=None, embed=em)


  
   