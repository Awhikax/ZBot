import discord, datetime

class Events:
    """Cog for the management of major events that do not belong elsewhere. Like when a new server invites the bot."""

    def __init__(self,bot):
        self.bot = bot
        self.file = "events"
        self.embed_colors = {"welcome":5301186,
        "mute":4868682,
        "kick":16730625,
        "ban":13632027,
        "slowmode":5671364,
        "clear":16312092,
        "warn":9131818}
    
    async def on_guild_add(self,guild):
        """Called when the bot joins a guild"""
        print("HEEY")
        await self.send_guild_log(guild,"join")


    async def on_guild_del(self,guild):
        """Called when the bot left a guild"""
        print("BYYE")
        await self.send_guild_log(guild,"left")

    async def send_guild_log(self,guild,Type):
        """Send a log to the logging channel when the bot joins/leave a guild"""
        try:
            if Type == "join":
                desc = "Bot **joins the server** {}".format(guild.name)
            else:
                desc = "Bot **left the server** {}".format(guild.name)
            emb = self.bot.cogs["EmbedCog"].Embed(desc=desc,color=self.embed_colors['welcome']).update_timestamp().set_author(self.bot.user)
            await self.bot.cogs["EmbedCog"].send([emb])
        except Exception as e:
            await self.bot.cogs["ErrorsCog"].on_error(e,None)


    async def on_new_message(self,msg):
        if msg.guild == None:
            await self.send_mp(msg)
        if msg.author.bot==False and await self.bot.cogs['AdminCog'].check_if_admin(msg.author) == False:
            if str(await self.bot.cogs["ServerCog"].find_staff(msg.guild,"anti_caps_lock")) in ['1','True'] and len(msg.content)>7:
                if sum(1 for c in msg.content if c.isupper())/len(msg.content) > 0.75:
                    try:
                        await msg.channel.send(str(await self.bot.cogs["LangCog"].tr(msg.guild,"modo","caps-lock")).format(msg.author.mention),delete_after=4.0)
                    except:
                        pass

    async def send_mp(self,msg):
        channel = self.bot.get_channel(488768968891564033)
        emb = msg.embeds[0] if len(msg.embeds)>0 else None
        text = "__`{} ({} - {})`__\n{}".format(msg.author,msg.channel.recipient,await self.bot.cogs["TimeCog"].date(msg.created_at,digital=True),msg.content)
        if len(msg.attachments)>0:
            text += "".join(["\n{}".format(x.url) for x in msg.attachments])
        await channel.send(text,embed=emb)



    async def send_logs_per_server(self,guild,Type,message,author=None):
        """Send a log in a server. Type is used to define the color of the embed"""
        c = self.embed_colors[Type.lower()]
        try:
            config = str(await self.bot.cogs["ServerCog"].find_staff(guild.id,"modlogs_channel")).split(';')[0]
            if config == "" or config.isnumeric()==False:
                return
            channel = guild.get_channel(int(config))
        except Exception as e:
            await self.bot.cogs["ErrorsCog"].on_error(e,None)
            return
        if channel == None:
            return
        emb = self.bot.cogs["EmbedCog"].Embed(desc=message,color=c).update_timestamp()
        if author != None:
            emb.set_author(author)
        try:
            await channel.send(embed=emb.discord_embed())
        except:
            pass


def setup(bot):
    bot.add_cog(Events(bot))