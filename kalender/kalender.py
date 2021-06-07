from redbot.core import Config
from redbot.core import commands
import requests
import json
import datetime
import discord
from pytz import timezone
import pytz
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
            await ctx.send('Bitte folgenden Syntax einhalten: !neuesevent "Beschreibung" Datum Anfang Ende - Beschreibung _mit_ Anführungszeichen! Beispiel siehe: tinyurl.com/scribii')
            return

        if len(ids) != 4:
            await ctx.send('Bitte folgenden Syntax einhalten: !neuesevent "Beschreibung" Datum Anfang Ende - Beschreibung _mit_ Anführungszeichen! Beispiel siehe: tinyurl.com/scribii')
            return

        if self.validate(ids[1]) != True:
            await ctx.send('Datum fehlerhaft! Beispiel siehe: tinyurl.com/scribii')
            return

        if self.valitime(ids[2]) != True:
            await ctx.send('Anfangszeit fehlerhaft! Beispiel siehe: tinyurl.com/scribii')
            return

        if self.valitime(ids[3]) != True:
            await ctx.send('Endzeit fehlerhaft! Beispiel siehe: tinyurl.com/scribii')
            return

        eventdate = f"{ids[1]} {ids[2]} {ids[3]}"

        try:
            is_already_item = await self.config.guild(ctx.guild).dates.get_raw(ids[0])
            if is_already_item:
                await self.config.guild(ctx.guild).dates.clear_raw(ids[0])
                await ctx.send(f"Das Ereignis {ids[0]} existiert schon.")
        except KeyError:
            await self.config.guild(ctx.guild).dates.set_raw(ids[0], value=eventdate)
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

        dates = await self.config.guild(ctx.guild).dates()

        event_collection = {}

        for key in dates:
            list = dates[key].split()
            event_collection[key] = {'date':list[0],'start':list[1],'end':list[2]}
        
        sorted_events = sorted(event_collection, key = lambda x: datetime.strptime(event_collection[x]  ['date'], '%d.%m.%y'))

        em.set_author(name=f"Nächstes Ereignis: {sorted_events[0]}", icon_url=url)


        for event in sorted_events:
            list = dates[event].split()
            textdate = f"{list[0]}\n {list[1]}-{list[2]} Uhr"
            em.add_field(name=event, value=textdate, inline=True)
        
        em.set_footer(text=f"Für Hilfe zur Nutzung bitte auf die Überschrift klicken.", icon_url=url_link)
        em.set_thumbnail(url=url_calendarlogo)
        
        channel = await ctx.bot.get_shared_api_tokens("calchannelid")
        channeldata = self.bot.get_channel(int(channel['calchannelid']))


        if update != True:
            calmsg = await channeldata.send(content="*Ein Kalender wird vom Schreiber Scrib in der Eingangshalle des Anwesens aufgehängt*", embed=em)
            await self.config.guild(ctx.guild).calendarmsgid.set(calmsg.id)
        
        if update == True:
            msgid = await self.config.guild(ctx.guild).calendarmsgid()
            msg = await channeldata.fetch_message(msgid)
            await msg.edit(content="*Ein Kalender wird vom Schreiber Scrib in der Eingangshalle des Anwesens aufgehängt*", embed=em)


  
    def validate(self, date_text):
        try:
            datetime.strptime(date_text, '%d.%m.%y')
            return True
        except ValueError:
            return False


    def valitime(self, date_text):
        try:
            datetime.strptime(date_text, '%H:%M')
            return True
        except ValueError:
            return False



    @commands.command()
    async def calclean(self, ctx: commands.Context):
        dates = await self.config.guild(ctx.guild).dates()

        for key in dates:
            list = dates[key].split()
            a = datetime.strptime(list[0], '%d.%m.%y')
            b = datetime.now()
            isold = a.date()<b.date()
            if isold == True:
                await self.config.guild(ctx.guild).dates.clear_raw(key)
                await self.kalender(ctx, True)
    
    @commands.command()
    async def calnotify(self, ctx: commands.Context):
        dates = await self.config.guild(ctx.guild).dates()
        channel = await ctx.bot.get_shared_api_tokens("calnotichannelid")
        channeldata = self.bot.get_channel(int(channel['calnotichannelid']))
        url = "https://konvent.fitzzz.de/uploads/images/system/2021-04/wappen-transparent.png"


        for key in dates:
            list = dates[key].split()
            a = datetime.strptime(list[0], '%d.%m.%y')
            c = datetime.strptime(list[1], '%H:%M')
            b = datetime.utcnow()
            d1 = datetime(a.year, a.month, a.day, c.hour, c.minute, 0) 

            utc = pytz.timezone('UTC')
            now = utc.localize(datetime.utcnow())
            de = pytz.timezone('Europe/Berlin')
            local_time = now.astimezone(de)
            d2 = datetime(local_time.year, local_time.month, local_time.day, local_time.hour, local_time.minute, 0)

            istoday = a.date()==b.date()
            if istoday == True:
                minutes_diff = (d1 - d2).total_seconds() / 60.0
                #await ctx.send(minutes_diff)

                if minutes_diff == 60:
                    em = discord.Embed()
                    em.set_author(name=key, icon_url=url)
                    em.description = (
                        f"Heute, am {list[0]}, von {list[1]} bis ca. {list[2]} Uhr"
                    )
                    allowed_mentions = discord.AllowedMentions(everyone = True)
                    await channeldata.send("@everyone *Die Glocke :bell: in der Eingangshalle wird geläutet und der Schreiber erinnert an das für heute angekündigte Ereignis, welches in einem Stundenlauf wohl starten mag...*",embed=em, allowed_mentions = allowed_mentions)
                

    @commands.command()
    async def calupdate(self, ctx: commands.Context):
        await self.kalender(ctx, True)