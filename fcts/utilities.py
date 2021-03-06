import discord, sys, traceback, importlib, datetime,random, re
from fcts import utilities
from discord.ext import commands



class UtilitiesCog:
    """This cog has various useful functions for the rest of the bot."""

    def __init__(self,bot):
        self.bot = bot
        self.list_prefixs = dict()
        self.file = "utilities"

    async def reload(self,liste):
        for m in liste:
            exec("importlib.reload({})".format(m))

    def find_prefix(self,guild):
        if str(guild.id) in self.list_prefixs.keys():
            return self.list_prefixs[str(guild.id)]
        else:
            cnx = self.bot.cogs['ServerCog'].connect()
            cursor = cnx.cursor(dictionary = False)
            cursor.execute("SELECT `prefix` FROM `servers` WHERE `ID`="+str(guild.id))
            liste = list()
            for x in cursor:
                liste.append(x)
            cnx.close()
            if liste == []:
                self.list_prefixs[str(guild.id)] = '!'
                return '!'
            self.list_prefixs[str(guild.id)] = liste[0][0]
            return str(liste[0][0])

    def update_prefix(self,ID,prefix):
        try:
            print("Prefix updated for guild {} : changed to {}".format(ID,prefix))
        except:
            pass
        self.list_prefixs[str(ID)] = prefix

    async def print2(self,text):
        try:
            print(text)
        except UnicodeEncodeError:
            text = await self.anti_code(str(text))
            try:
                print(text)
            except UnicodeEncodeError:
                print(text.encode("ascii","ignore").decode("ascii"))

    async def anti_code(self,text):
        if type(text)==str:
            for i,j in [('é','e'),('è','e'),('à','a'),('î','i'),('ê','e'),('ï','i'),('ü','u'),('É','e'),('ë','e'),('–','-'),('“','"'),('’',"'"),('û','u'),('°','°'),('Ç','C'),('ç','c')]:
                text=text.replace(i,j)
            return text
        elif type(text)==list:
            text2=[]
            for i,j in [('é','e'),('è','e'),('à','a'),('î','i'),('ê','e'),('ï','i'),('ü','u'),('É','e'),('ë','e'),('–','-'),('“','"'),('’',"'"),('û','u'),('°','°'),('Ç','C'),('ç','c')]:
                for k in text:
                    text2.append(k.replace(i,j))
                    return text2


    async def find_everything(self,ctx,name,Type=None):
        item = None
        if type(Type) == str:
            Type = Type.lower()
        if Type == None:
            for i in [commands.RoleConverter,commands.MemberConverter,
                    commands.TextChannelConverter,commands.InviteConverter,
                    commands.UserConverter,commands.VoiceChannelConverter,
                    commands.EmojiConverter,commands.CategoryChannelConverter]:
                try:
                    a = await i().convert(ctx,name)
                    item = a
                    if item != None:
                        return item
                except:
                    pass
        elif Type == 'member':
            try:
                item = await commands.MemberConverter().convert(ctx,name)
            except:
                pass
        elif Type == 'role':
            try:
                item = await commands.RoleConverter().convert(ctx,name)
            except:
                pass
        elif Type == 'user':
            try:
                item = await commands.UserConverter().convert(ctx,name)
            except:
                if name.isnumeric():
                    item = await self.bot.get_user_info(int(name))
        elif Type == 'textchannel' or Type == "channel":
            try:
                item = await commands.TextChannelConverter().convert(ctx,name)
            except:
                pass
        elif Type == 'invite':
            try:
                item = await commands.InviteConverter().convert(ctx,name)
            except:
                pass
        elif Type == 'voicechannel' or Type == 'channel':
            try:
                item = await commands.VoiceChannelConverter().convert(ctx,name)
            except:
                pass
        elif Type == 'emoji':
            try:
                item = await commands.EmojiConverter().convert(ctx,name)
            except:
                pass
        elif Type == 'category':
            try:
                item = await commands.CategoryConverter().convert(ctx,name)
            except:
                pass
        elif Type == 'guild' and name.isnumeric():
            item = self.bot.get_guild(int(name))
        return item

    async def find_img(self,name):
        return discord.File("../images/{}".format(name))

    async def suppr(self,msg):
        try:
            await msg.delete()
        except:
            await self.print2("Unable to delete message "+str(msg))
            pass

    async def global_check(self,ctx):
        if type(ctx)==commands.context:
            ctx = ctx.guild
        elif type(ctx) != discord.guild:
            return True
        config = await self.bot.cogs['ServerCog'].get_bot_infos(self.bot.user.id)
        if len(config)==0:
            return True
        return not str(ctx.id) in config[0]['banned_guilds'].split(";")

    async def create_footer(self,embed,user):
        embed.set_footer(text="Requested by {}".format(user.name), icon_url=user.avatar_url_as(format='png'))
        return embed

    async def get_online_number(self,members):
        online = 0
        for m in members:
            if str(m.status) in ["online","idle"]:
                online += 1
        return online
    
    async def get_bots_number(self,members):
        return len([x for x in members if x.bot])

    async def on_message(self,msg):
        try:
            await self.bot.cogs['FunCog'].check_suggestion(msg)
        except KeyError:
            pass
        except Exception as e:
            await self.bot.cogs['ErrorsCog'].on_error(e,msg)

    async def set_find(self,set,name):
        for x in set:
            if x.name==name:
                return x

    async def check_any_link(self,text):
        ch = r"(https?://?(?:[-\w.]|(?:%[\da-fA-F]{2}))+|discord.gg/[^\s]+)"
        return re.search(ch,text)

    async def check_discord_invite(self,text):
        ch = r"((?:discord\.gg|discordapp.com/invite|discord.me)/.+)"
        return re.search(ch,text)

    def sync_check_any_link(self,text):
        ch = r"(https?://?(?:[-\w.]|(?:%[\da-fA-F]{2}))+|discord.gg/[^\s]+)"
        return re.search(ch,text)

    def sync_check_discord_invite(self,text):
        ch = r"((?:discord\.gg|discordapp.com/invite|discord.me)/.+)"
        return re.search(ch,text)

    async def clear_msg(self,text,everyone=True,ctx=None):
        """Remove every mass mention form a text, and add custom emojis"""
        if everyone:
            text = text.replace("@everyone","@"+u"\u200B"+"everyone").replace("@here","@"+u"\u200B"+"here")
        #for x in re.finditer(r'<(a?:[^:]+:)\d+>',text):
        #    text = text.replace(x.group(0),x.group(1))
        #for x in self.bot.emojis: #  (?<!<|a)(:[^:<]+:)
        #    text = text.replace(':'+x.name+':',str(x))
        for x in re.finditer(r'(?<!<|a):([^:<]+):',text):
            try:
                em = await commands.EmojiConverter().convert(ctx,x.group(1))
            except Exception as e:
                print(e)
                continue
            if em != None:
                text = text.replace(x.group(0),"<{}:{}:{}>".format('a' if em.animated else '' , em.name , em.id))
        return text

    async def is_premium(self,user):
        guild = self.bot.get_guild(356067272730607628)
        if guild == None:
            return False
        if type(user)==discord.User:
            user = guild.get_member(user.id)
            if user == None:
                return False
        role = guild.get_role(523904552374763532)
        if role == None:
            return False
        return role in user.roles


def setup(bot):
    bot.add_cog(UtilitiesCog(bot))
