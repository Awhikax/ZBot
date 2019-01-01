import discord, feedparser, datetime, time, re, asyncio, mysql, random
from discord.ext import commands


web_link={'fr-minecraft':'http://fr-minecraft.net/rss.php',
          'frm':'http://fr-minecraft.net/rss.php',
          'minecraft.net':'https://minecraft.net/fr-fr/feeds/community-content/rss',
          'arobazzz':'http://le-minecraftien.e-monsite.com/blog/do/rss.xml',
          'minecraftien':'http://le-minecraftien.e-monsite.com/blog/do/rss.xml',
          'gunivers':'https://gunivers.net/feed/'
          }

reddit_link={'minecraft':'https://www.reddit.com/r/Minecraft',
             'reddit':'https://www.reddit.com/r/news',
             'discord':'https://www.reddit.com/r/discordapp'
             }

yt_link={'neil3000':'UC7SdIxpBCuP-KXSqaexTdAw',
         'grand_corbeau':'UCAt_W0Rgr33OePJ8jylkx0A',
         'mojang':'UC1sELGmy5jp5fQUugmuYlXQ',
         'frm':'frminecraft',
         'fr-minecraft':'frminecraft',
         'freebuild':'UCFl41Y9Hf-BtZBn7LGPHNAQ',
         'fb':'UCFl41Y9Hf-BtZBn7LGPHNAQ',
         'aurelien_sama':'AurelienSama',
         'asilis':'UC2_9zcNSfEBecm3yaojexXw',
         'leirof':'UCimA2SBz78Mj-TQ2n4TmEVw',
         'gunivers':'UCtQb5O95cCGp9iquLjY9O1g',
         'platon_neutron':'UC2xPiOqjQ-nZeCka_ZNCtCQ',
         'aragorn1202':'UCjDG6KLKOm6_8ax--zgeB6Q'
         }

guilds_limit_exceptions={"391968999098810388":30,
        "356067272730607628":30}


async def check_admin(ctx):
    return await ctx.bot.cogs['AdminCog'].check_if_admin(ctx)

async def can_use_rss(ctx):
    return ctx.channel.permissions_for(ctx.author).administrator or await ctx.bot.cogs["AdminCog"].check_if_admin(ctx)

class RssCog:
    """Cog which deals with everything related to rss flows. Whether it is to add automatic tracking to a stream, or just to see the latest video released by Discord, it is this cog that will be used."""

    def __init__(self,bot):
        self.bot = bot
        self.file = "rss"
        self.embed_color = discord.Color(6017876)
        try:
            self.translate = bot.cogs["LangCog"].tr
        except:
            pass
        try:
            self.date = bot.cogs["TimeCog"].date
        except:
            pass
        try:
            self.print = bot.cogs["UtilitiesCog"].print2
        except:
            pass
        self.zbot = discord.Client()

    async def on_ready(self):
        self.translate = self.bot.cogs["LangCog"].tr
        self.date = self.bot.cogs["TimeCog"].date
        self.print = self.bot.cogs["UtilitiesCog"].print2


    class rssMessage:
        def __init__(self,Type,url,title,emojis,date=datetime.datetime.now(),author=None,Format=None,channel=""):
            self.Type = Type
            self.url = url
            self.title = title
            if type(date) == datetime.datetime:
                self.date = date
            elif type(date) == time.struct_time:
                self.date = datetime.datetime(*date[:6])
            elif type(date) == str:
                self.date = date
            else:
                date = None
            self.author = author
            self.format = Format
            if Type == 'yt':
                self.logo = emojis['youtube']
            elif Type == 'tw':
                self.logo = emojis['twitter']
            elif Type == 'reddit':
                self.logo = emojis['reddit']
            else:
                self.logo = ':newspaper:'
            self.channel = channel
            self.mentions = []
            if self.author == None:
                self.author = channel
        
        async def fill_mention(self,guild,roles,translate):
            if roles == []:
                r = await translate(guild.id,"keywords","none")
            else:
                r = list()
                for item in roles:
                    if item=='':
                        continue
                    role = discord.utils.get(guild.roles,id=int(item))
                    if role != None:
                        r.append(role.mention)
                    else:
                        r.append(item)
                self.mentions = r
            return self

        async def create_msg(self,fct,language,Format=None):
            if Format == None:
                Format = self.format
            d = await fct(self.date,lang=language,year=False,hour=True,digital=True)
            Format = Format.replace('\\n','\n')
            return Format.format(channel=self.channel,title=self.title,date=d,url=self.url,link=self.url,mentions=", ".join(self.mentions),logo=self.logo,author=self.author)


    @commands.group(name="rss")
    @commands.cooldown(2,20,commands.BucketType.channel)
    async def rss_main(self,ctx):
        """See the last post of a rss feed"""
        return

    @rss_main.command(name="youtube",aliases=['yt'])
    async def request_yt(self,ctx,ID):
        """the last video of a YouTube channel"""
        if ID in yt_link.keys():
            ID = yt_link[ID]
        if "youtube.com" in ID or "youtu.be" in ID:
            ID= await self.parse_yt_url(ID)
        text = await self.rss_yt(ctx.guild,ID)
        if type(text) == str:
            await ctx.send(text)
        else:
            form = await self.translate(ctx.guild,"rss","yt-form-last")
            await ctx.send(await text[0].create_msg(self.date,await self.translate(ctx.guild,"current_lang","current"),form))

    @rss_main.command(name='twitter',aliases=['tw'])
    async def request_tw(self,ctx,name):
        """The last tweet of a Twitter account"""
        if "twitter.com" in name:
            name = await self.parse_tw_url(name)
        try:
            text = await self.rss_tw(ctx.guild,name)
        except Exception as e:
            await self.bot.cogs['ErrorsCog'].on_error(e,ctx)
        if type(text) == str:
            await ctx.send(text)
        else:
            form = await self.translate(ctx.guild,"rss","tw-form-last")
            await ctx.send(await text[0].create_msg(self.date,await self.translate(ctx.guild,"current_lang","current"),form))

    @rss_main.command(name="web")
    async def request_web(self,ctx,link):
        """The last post on any other rss feed"""
        if link in web_link.keys():
            link = web_link[link]
        text = await self.rss_web(ctx.guild,link)
        if type(text) == str:
            await ctx.send(text)
        else:
            form = await self.translate(ctx.guild,"rss","web-form-last")
            await ctx.send(await text[0].create_msg(self.date,await self.translate(ctx.guild,"current_lang","current"),form))

    @rss_main.command(name="add",hidden=True)
    @commands.guild_only()
    @commands.check(can_use_rss)
    async def system_add(self,ctx,link):
        """Subscribe to a rss feed (displayed on this channel regularly)"""
        await ctx.send("Sorry but we can't do that for now, our database is offline :confused:")

    @rss_main.command(name="remove",hidden=True)
    @commands.guild_only()
    @commands.check(can_use_rss)
    async def systeme_rm(self,ctx,ID:int=None):
        """Delete an rss feed from the list"""
        await ctx.send("Sorry but we can't do that for now, our database is offline :confused:")

    @rss_main.command(name="list",hidden=True)
    @commands.guild_only()
    @commands.check(can_use_rss)
    async def list_flows(self,ctx):
        """Get a list of every rss/Minecraft feed"""
        await ctx.send("Sorry but we can't do that for now, our database is offline :eyes:")

    @rss_main.command(name="roles",hidden=True)
    @commands.guild_only()
    @commands.check(can_use_rss)
    async def roles_flows(self,ctx,ID:int=None):
        """configures a role to be notified when a news is posted"""
        await ctx.send("Sorry but we can't do that for now, our database is offline :confused:")


    async def parse_yt_url(self,url):
        r = r'(?:http.*://)?(?:www.)?(?:youtube.com|youtu.be)(?:/channel/|/user/)(.+)'
        match = re.search(r,url)
        if match == None:
            return None
        else:
            return match.group(1)

    async def parse_tw_url(self,url):
        r = r'(?:http.*://)?(?:www.)?(?:twitter.com/)(.+)'
        match = re.search(r,url)
        if match == None:
            return None
        else:
            return match.group(1)


    async def rss_yt(self,guild,identifiant,date=None):
        if identifiant=='help':
            return await self.translate(guild,"rss","yt-help")
        url = 'https://www.youtube.com/feeds/videos.xml?channel_id='+identifiant
        feeds = feedparser.parse(url)
        if feeds.entries==[]:
            url = 'https://www.youtube.com/feeds/videos.xml?user='+identifiant
            feeds = feedparser.parse(url)
            if feeds.entries==[]:
                return await self.translate(guild,"rss","nothing")
        if not date:
            feed = feeds.entries[0]
            obj = self.rssMessage(Type='yt',url=feed['link'],title=feed['title'],emojis=self.bot.cogs['EmojiCog'].customEmojis,date=feed['published_parsed'],author=feed['author'])
            return [obj]
        else:
            liste = list()
            for feed in feeds.entries:
                if datetime.datetime(*feed['published_parsed'][:6]) <= date:
                    break
                obj = self.rssMessage(Type='yt',url=feed['link'],title=feed['title'],emojis=self.bot.cogs['EmojiCog'].customEmojis,date=feed['published_parsed'],author=feed['author'])
                liste.append(obj)
            liste.reverse()
            return liste

    async def rss_tw(self,guild,nom,date=None):
        if nom == 'help':
            return await self.translate(guild,"rss","tw-help")
        url = 'http://twitrss.me/twitter_user_to_rss/?user='+nom
        feeds = feedparser.parse(url)
        if feeds.entries==[]:
            url = 'http://twitrss.me/twitter_user_to_rss/?user='+nom.capitalize()
            feeds = feedparser.parse(url)
            if feeds.entries==[]:
                url = 'http://twitrss.me/twitter_user_to_rss/?user='+nom.lower()
                feeds = feedparser.parse(url)
                if feeds.entries==[]:
                    return await self.translate(guild,"rss","nothing")
        if date != None:
            await self.logs_append("requête Twitter pour la chaine {}".format(nom))
            await self.logs_append("   Date du plus haut tweet : {}".format(feeds.entries[0]['published_parsed']))
        if len(feeds.entries)>1:
            while feeds.entries[0]['published_parsed'] < feeds.entries[1]['published_parsed']:
                del feeds.entries[0]
                if len(feeds.entries)==1:
                    break
        if not date:
            feed = feeds.entries[0]
            r = re.search(r"(pic.twitter.com/[^\s]+)",feed['title'])
            if r != None:
                t = feed['title'].replace(r.group(1),'')
            else:
                t = feed['title']
            obj = self.rssMessage(Type='tw',url=feed['link'],title=t,emojis=self.bot.cogs['EmojiCog'].customEmojis,date=feed['published_parsed'],author=feed['author'],channel=feeds.feed['title'])
            return [obj]
        else:
            liste = list()
            for feed in feeds.entries:
                await self.logs_append("  Résultat de la recherche : {}".format(feed['published_parsed']))
                if datetime.datetime(*feed['published_parsed'][:6]) <= date:
                    break
                obj = self.rssMessage(Type='tw',url=feed['link'],title=feed['title'],emojis=self.bot.cogs['EmojiCog'].customEmojis,date=feed['published_parsed'],author=feed['author'],channel= feeds.feed['title'])
                liste.append(obj)
            liste.reverse()
            return liste

    async def rss_web(self,guild,url,date=None):
        if url == 'help':
            return await self.translate(guild,"rss","web-help")
        feeds = feedparser.parse(url)
        if 'bozo_exception' in feeds.keys() and len(feeds.entries)==0:
            return await self.translate(guild,"rss","web-invalid")
        if 'published_parsed' in feeds.entries[0]:
            published = 'published_parsed'
        else:
            published = 'published'
        while feeds.entries[0][published] < feeds.entries[1][published]:
            del feeds.entries[0]
        if not date or published == 'published':
            feed = feeds.entries[0]
            obj = self.rssMessage(Type='web',url=feed['link'],title=feed['title'],emojis=self.bot.cogs['EmojiCog'].customEmojis,date=feed[published],author=feed['author'] if 'author' in feed.keys() else None,channel= feeds.feed['title'])
            return [obj]
        else:
            liste = list()
            for feed in feeds.entries:
                if datetime.datetime(*feed['published_parsed'][:6]) <= date:
                    break
                obj = self.rssMessage(Type='web',url=feed['link'],title=feed['title'],emojis=self.bot.cogs['EmojiCog'].customEmojis,date=feed[published],author=feed['author'] if 'author' in feed.keys() else None,channel= feeds.feed['title'])
                liste.append(obj)
            liste.reverse()
            return liste


    async def loop(self):
        print("[RSS] Rss flow exited, can't use the database")
        return


    @commands.command(name="rss_loop",hidden=True)
    @commands.check(check_admin)
    async def rss_loop_admin(self,ctx,permanent:bool=False):
        """Force the rss loop"""
        await ctx.send("T'as déjà oublié que la base de donnée était hors ligne ? :face_palm:")

def setup(bot):
    bot.add_cog(RssCog(bot))