from redbot.core import Config
from redbot.core import commands
import requests
import json
import datetime
import discord
from datetime import datetime, timedelta

class Calendar(commands.Cog):
    def __init__(self):
        self.config = Config.get_conf(self, identifier=38586798456)
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
        dates = await self.config.guild(ctx.guild).dates()
        # await ctx.send("The value of dates is {}".format("True" if dates else "False"))

        for key in dates:
            await ctx.send("Key is "+ key)



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
                await ctx.send(f"Das Ereignis {id[0]} wurde entfernt.")
        except KeyError:
            await ctx.send(f"Das Ereignis {id[0]} nicht gefunden.")


    @commands.command()
    async def kalender(self, ctx: commands.Context):
        """This posts an example embed"""
        # guild = self.bot.get_guild(payload.guild_id)
        # user = guild.get_member(payload.user_id)

        user = ctx.message.author.name
        url = ctx.message.author.avatar_url
        url = "https://konvent.fitzzz.de/uploads/images/system/2021-04/wappen-transparent.png"
        url_link = "https://konvent.fitzzz.de/uploads/images/gallery/2021-03/scaled-1680-/link.png"
        url_calendarlogo = "https://cdn4.iconfinder.com/data/icons/small-n-flat/24/calendar-512.png"

        em = discord.Embed(title="Aktueller Terminplan des Konvents", url="https://konvent.fitzzz.de/books/anatomie-i")
        #em.set_author(name=f"Ein Buch wurde aktualisiert!")
        em.set_author(name=f"Ein neuer Kalender wird aufgehängt...", icon_url=url)

        # em.description = (
        #     f"Name des Buchs: "
        # )

        dates = await self.config.guild(ctx.guild).dates()

        for key in dates:
            em.add_field(name=key, value=dates[key], inline=True)
            # await ctx.send("Key is "+ key)
            # await ctx.send("Key is "+ dates[key])


        # em.add_field(name="Jagdausflug", value="19.02. 21 Uhr ", inline=True)
        # em.add_field(name="Unterricht Konvent", value="23.04. 20 Uhr", inline=False)
        # em.add_field(name="Unterricht Akademie", value="26.05. 20 Uhr")
        
        #em.set_image(url=url)
        #em.set_footer(text=f"Test!", icon_url=url_link)
        #em.set_footer(text=f"Approved by {user}")

        # thumbnails = await self.config.guild(ctx.guild).custom_links()
        # for name, link in thumbnails.items():
        #     if name.lower() in event.event.lower():
        em.set_thumbnail(url=url_calendarlogo)

        await ctx.send(None, embed=em)
    
   