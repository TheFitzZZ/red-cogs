from redbot.core import Config
from redbot.core import commands
import requests
import json
import datetime
import discord
from datetime import datetime, timedelta

class Test(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.config = Config.get_conf(self, identifier=3858673456)
        self.bot = bot
        default_global = {
            "foobar": True,
            "dates": {
                # "Test 1": "1.1. 01:00 Uhr",
                # "Test 2": "2.2. 02:00 Uhr"
            }
        }
        default_guild = {
            "blah": [],
            # "baz": 1234567890
            "dates": {
                # "Test 1": "1.1. 01:00 Uhr",
                # "Test 2": "2.2. 02:00 Uhr"
            },
            "calendarmsgid": 0
        }
        self.config.register_global(**default_global)
        self.config.register_guild(**default_guild)

  
    @commands.command()
    async def test(self, ctx):
        """This does stuff!"""
        # Your code will go here
        # await ctx.send("Lese Default Dict...")
        dates = await self.config.guild(ctx.guild).dates()
        # await ctx.send("The value of dates is {}".format("True" if dates else "False"))

        for key in dates:
            await ctx.send("Key is "+ key)


        # await ctx.send("Lösche ein Dict...")
        # del dates["Test 1"]

        # for key in dates:
        #     await ctx.send("Key is "+ key)

        # await ctx.send("Adde ein Dict...")

        # dates["Test 3"] = "rofl"
        # for key in dates:
        #     await ctx.send("Key is "+ key)

    #    @post.command(name='작성', usage='작성 [제목]', aliases=['write'], help='글을 작성합니다', brief='usingcommand')
    #             await msg.edit(embed=Embed(title='글 작성이 취소되었습니다', color=Color.green()))
    #         await msg.add_reaction('⭕')
    # post = self.bot.postDB.getByID(id)
    # 		print(self.db.deletePost(id))

    @commands.command()
    async def getpostid(self, ctx):
        """This does stuff!"""

        test = await ctx.send("This is a post...")
        #await ctx.send(test.id)
        await self.config.guild(ctx.guild).calendarmsgid.set(test.id)

        #msgid = await self.config.guild(ctx.guild).calendarmsgid()
        #await ctx.send(msgid)

    @commands.command()
    async def deletepost(self, ctx, channel: discord.TextChannel = None):
        """This does stuff!"""
        # msgid = await self.config.guild(ctx.guild).calendarmsgid()
        channel = await ctx.bot.get_shared_api_tokens("calchannelid")
        msgid = await self.config.guild(ctx.guild).calendarmsgid()
        await ctx.send(channel['calchannelid'])


        channell = self.bot.get_channel(int(channel['calchannelid']))
        # await ctx.send(channell)
        
        # chan = commands.get_channel(channel)
        msg = await channell.fetch_message(msgid)
        await msg.edit(content="Some content!")
        
        
        await msg.delete()

        #msg = await ctx.guild.deletepost(msgid)  #get_message(channel, message_id)
        #await msg.deletepost()



    @commands.command()
    async def senttochannel(self, ctx):
        """This does stuff!"""

        # Get the channel we should send this to from the secret storage (workaround for now ... or ever cus it works and I'm lazy)
        test = await ctx.bot.get_shared_api_tokens("channelid")
        channelid = test.get("channelid")
        channelid = int(channelid)
        chan = ctx.bot.get_channel(channelid)

    @commands.command()
    async def tneuesevent(self, ctx: commands.Context, *ids: str):
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
            await self.tkalender(ctx, True)
            await ctx.send(f"Das Ereignis {ids[0]} wurde dem Kalender hinzugefügt.")




    @commands.command()
    async def tloescheevent(self, ctx: commands.Context, *id: str):
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
    async def tkalender(self, ctx: commands.Context):
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
    
   

    # @commands.command()
    # async def sorttest(self, ctx: commands.Context):
    #     """This does stuff!"""
    #     # Your code will go here
    #     await ctx.send("Sorting test...")

    #     dates = await self.config.guild(ctx.guild).dates()

    #     await ctx.send(dates)
    #     for key in dates:
    #         await ctx.send(key)









    @commands.command()
    async def ad2(self, ctx: commands.Context, *ids: str):
        """This does stuff!"""
        # Your code will go here
        # await ctx.send("Lese Default Dict..."+ ctx.Content)

        if len(ids) != 2:
            return await ctx.send_help()

        await ctx.send(len(ids))

        for idx in ids:
            await ctx.send("Key is "+ idx)
            
    @commands.command()
    async def checkdate(self, ctx: commands.Context, *ids: str):
        """This does stuff!"""
        # Your code will go here
        # await ctx.send("Lese Default Dict..."+ ctx.Content)

        if len(ids) != 4:
            return await ctx.send_help()

        await ctx.send(len(ids))

        for idx in ids:
            await ctx.send("Key is "+ idx)

        self.validate(ids[1])
        self.valitime(ids[2])   
            



    def validate(self, date_text):
        try:
            datetime.strptime(date_text, '%d.%m.%y')
            return True
        except ValueError:
            # raise ValueError("Incorrect data format, should be DD.MM.YY")
            return False


    def valitime(self, date_text):
        try:
            datetime.strptime(date_text, '%H:%M')
            return True
        except ValueError:
            #raise ValueError("Incorrect time format, should be 23:45")
            return False


        

    @commands.command(name="testem")
    async def testembed(self, ctx: commands.Context):
        """This posts an example embed"""
        # guild = self.bot.get_guild(payload.guild_id)
        # user = guild.get_member(payload.user_id)

        user = ctx.message.author.name
        url = ctx.message.author.avatar_url
        url = "https://konvent.fitzzz.de/uploads/images/cover_book/2021-01/thumbs-440-250/necro-b1.png"
        url_link = "https://konvent.fitzzz.de/uploads/images/gallery/2021-03/scaled-1680-/link.png"
        url_calendarlogo = "https://cdn4.iconfinder.com/data/icons/small-n-flat/24/calendar-512.png"

        em = discord.Embed(title="Aktueller Terminplan des Konvents", url="https://konvent.fitzzz.de/books/anatomie-i")
        em.set_author(name=f"Ein Buch wurde aktualisiert!")
        #em.set_author(name=f"is hosting", icon_url=url)

        # em.description = (
        #     f"Name des Buchs: "
        # )

        em.add_field(name="Jagdausflug", value="19.02. 21 Uhr ", inline=True)
        em.add_field(name="Unterricht Konvent", value="23.04. 20 Uhr", inline=False)
        em.add_field(name="Unterricht Akademie", value="26.05. 20 Uhr")
        #em.set_image(url=url)
        em.set_footer(text=f"Test!", icon_url=url_link)
        #em.set_footer(text=f"Approved by {user}")

        # thumbnails = await self.config.guild(ctx.guild).custom_links()
        # for name, link in thumbnails.items():
        #     if name.lower() in event.event.lower():
        em.set_thumbnail(url=url_calendarlogo)

        await ctx.send(None, embed=em)
    
     
    @commands.command(name="status")
    async def shit(self, ctx: commands.Context):
        """This posts an example embed"""
        # guild = self.bot.get_guild(payload.guild_id)
        # user = guild.get_member(payload.user_id)

        #current_status = ctx.me.status
        #current_game = str(ctx.me.game)
        
        new_game = "test"

        await ctx.send("Changing status...")
        #await self.bot.change_presence(game=discord.Game(name=new_game), status=current_status)
        game = discord.Game(
            name=new_game
        )
        await self.bot.change_presence(activity=game)
     
     
     
    # @commands.command(name="bb")
    # async def bb(self, ctx: commands.Context):
    #     """Set the emoji to use for bookmarks
        
    #     The default is :bookmark:"""
    #     query = await ctx.send("What emoji should be used for bookmarks?")
    #     def check_reaction_user(reaction: discord.Reaction, user: discord.User):
    #         return user == ctx.author and reaction.message.id == query.id
    #     try:
    #         reaction, user = await ctx.bot.wait_for("reaction_add", check=check_reaction_user, timeout=60)
    #     except:
    #         await ctx.send("I'm done waiting. Please try reacting with an emoji next time.")
    #         return
    #     await self.conf.guild(ctx.message.guild).bookmark.set(reaction.emoji)
    #     await ctx.send(f"Bookmark emoji set to {reaction.emoji}")
    
    
    
    
    @commands.command(name="cb2")
    async def cb(self, ctx: commands.Context):
        """Prüft auf aktualisierte Objekte in der Bibliothek"""
        # await ctx.send("Prüfe manuell auf Neues in der Bibliothek...")

        # Input the appropriate values for these three variables
        book_url = 'https://konvent.fitzzz.de/api/books'
        chapters_url = 'https://konvent.fitzzz.de/api/chapters'
        shelves_url = 'https://konvent.fitzzz.de/api/shelves'
        pages_url = 'https://konvent.fitzzz.de/api/pages'

        # Handle authentication
        access_token = await ctx.bot.get_shared_api_tokens("bookstack")
        token = access_token.get("scrib")
        token = str(token)
        header = {"Content-Type": "application/json", "Authorization": ("Token "+token)}

        # Prep global vars
        json_books: object
        json_shelves: object
        json_chapters: object
        json_pages: object
        

        async def get_updates():
            global json_books
            global json_shelves
            global json_chapters
            global json_pages

            try:
                response = requests.get(book_url, headers=header)
                response.raise_for_status()
                
                json_books=response.json()
                json_books=json_books['data']

                response = requests.get(shelves_url, headers=header)
                response.raise_for_status()
                
                json_shelves=response.json()
                json_shelves=json_shelves['data']

                response = requests.get(chapters_url, headers=header)
                response.raise_for_status()
                
                json_chapters=response.json()
                json_chapters=json_chapters['data']

                response = requests.get(pages_url, headers=header)
                response.raise_for_status()
                
                json_pages=response.json()
                json_pages=json_pages['data']

            except requests.exceptions.HTTPError as error:
                print(error)
                # This code will run if there is a 404 error.
        
        def get_detail(type, id):
            global json_books
            global json_shelves
            global json_chapters
            global json_pages

            if(type == "shelve"):
                url = shelves_url + "/" + str(id)
            elif(type == "book"):
                url = book_url + "/" + str(id)
            elif(type == "chapter"):
                url = chapters_url + "/" + str(id)
            elif(type == "page"):
                url = pages_url + "/" + str(id)
            
            try:
                response = requests.get(url, headers=header)
                response.raise_for_status()
                
                json=response.json()
                #json=json['data']

                #print(json)
                #print(json['created_by'])
                name = json['updated_by']['name']
                slug = json['slug']
                
                if(type == "book" or type == "shelve"):
                    coverpath = json['cover']['path']
                else:
                    coverpath = "/uploads/images/gallery/2021-03/scaled-1680-/book.png"

                result = [name,slug,coverpath]

                return result
                
            except requests.exceptions.HTTPError as error:
                print(error)
                # This code will run if there is a 404 error.

        async def check_update():
            global json_books
            global json_shelves
            global json_chapters
            global json_pages
            
            
            # Get the channel we should send this to from the secret storage (workaround for now ... or ever cus it works and I'm lazy)
            test = await ctx.bot.get_shared_api_tokens("channelid")
            channelid = test.get("channelid")
            channelid = int(channelid)
            chan = ctx.bot.get_channel(channelid)

            # Iterate through the shelves
            for shelve in json_shelves:  
                result = is_recent(shelve['updated_at'])
                if(result):
                    #await ctx.send(shelve['name'])
                    item = get_detail("shelve", shelve['id'])
                    em = build_embed(shelve['name'], item[2], item[1], "shelves", item[0] )
                    await chan.send(None, embed=em)
            pass

            # Iterate through the books
            for book in json_books:
                result = is_recent(book['updated_at'])
                if(result):
                    #await ctx.send(book['name'])
                    item = get_detail("book", book['id'])
                    em = build_embed(book['name'], item[2], item[1], "books", item[0] )
                    await chan.send(None, embed=em)
            pass

            # Iterate through the chapters
            for chapter in json_chapters:
                result = is_recent(chapter['updated_at'])
                if(result):
                    #await ctx.send(chapter['name'])
                    item = get_detail("chapter", chapter['id'])
                    em = build_embed(chapter['name'], item[2], item[1], "chapters", item[0] )
                    await chan.send(None, embed=em)
            pass

            # Iterate through the pages
            for page in json_pages:
                result = is_recent(page['updated_at'])
                if(result):
                    #await ctx.send(page['name'])
                    item = get_detail("page", page['id'])
                    em = build_embed(page['name'], item[2], item[1], "pages", item[0] )
                    await chan.send(None, embed=em)
            pass

        def is_recent(strtimestamp):
            # Get current datetime
            start = datetime.now()
            end   = datetime.strptime(strtimestamp, '%Y-%m-%d %H:%M:%S')
            delta = start-end

            # Dumb workaround that if you read it it will make you sick
            deltaa = datetime.now()
            deltab = datetime.now()
            deltaa = deltaa.replace(hour=2, minute=0, second=0, microsecond=0)
            deltab = deltab.replace(hour=1, minute=0, second=0, microsecond=0)
            timeframe = deltaa - deltab
            
            if(delta < timeframe):
                #print("yes")
                return True
            else:
                #print("no")
                return False

        def build_embed(name, thumburl, slug, type, editor):
            url_thumb = "https://konvent.fitzzz.de" + thumburl
            #url_link = "https://konvent.fitzzz.de/uploads/images/gallery/2021-03/scaled-1680-/link.png"
            url_calendarlogo = "https://konvent.fitzzz.de/uploads/images/gallery/2021-03/wappen-transparent.png"
            url_item = "https://konvent.fitzzz.de/" # "https://konvent.fitzzz.de/" + type + "/" + slug

            if(type == "books"):
                authortext = "Ein Buch wurde aktualisiert!"
            elif(type == "pages"):
                authortext = "Eine Seite wurde aktualisiert!"
            elif(type == "chapters"):
                authortext = "Ein Kapitel wurde aktualisiert!"
            elif(type == "shelves"):
                authortext = "Ein Regal wurde aktualisiert!"

            em = discord.Embed(title=name, url=url_item)
            em.set_author(name=authortext)
            em.add_field(name="Bearbeiter/in", value=editor)
            em.set_image(url=url_thumb)
            #em.set_footer(text=f"Zum öffnen des Buches des Buches den Titel anklicken!", icon_url=url_link)
            em.set_thumbnail(url=url_calendarlogo)

            return em

        

        await get_updates()
        await check_update()

        #await ctx.send(None, embed=em)
        #await ctx.send("The end.")
