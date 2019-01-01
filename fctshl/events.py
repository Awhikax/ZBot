import discord, datetime, asyncio

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
        self.points = 0
        self.table = {'kick':3,
            'ban':7,
            'invite':22,
            'emoji':30,
            'channel':45,
            'role':60,
            'guild':75}
    
    async def on_guild_add(self,guild):
        """Called when the bot joins a guild"""
        await self.send_guild_log(guild,"join")


    async def on_guild_del(self,guild):
        """Called when the bot left a guild"""
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
            return 
        if msg.author.bot==False and await self.bot.cogs['AdminCog'].check_if_admin(msg.author) == False and msg.guild!=None:
            if not msg.channel.permissions_for(msg.author).manage_guild and len(msg.content)>7:
                if sum(1 for c in msg.content if c.isupper())/len(msg.content) > 0.75:
                    try:
                        await msg.channel.send(str(await self.bot.cogs["LangCog"].tr(msg.guild,"modo","caps-lock")).format(msg.author.mention),delete_after=4.0)
                    except:
                        pass

    async def send_mp(self,msg):
        if "vient d'être ajouté dans la base de donnée" in msg.content:
            return
        channel = self.bot.get_channel(488768968891564033)
        emb = msg.embeds[0] if len(msg.embeds)>0 else None
        text = "__`{} ({} - {})`__\n{}".format(msg.author,msg.channel.recipient,await self.bot.cogs["TimeCog"].date(msg.created_at,digital=True),msg.content)
        if len(msg.attachments)>0:
            text += "".join(["\n{}".format(x.url) for x in msg.attachments])
        await channel.send(text,embed=emb)



    async def send_logs_per_server(self,guild,Type,message,author=None):
        """Send a log in a server. Type is used to define the color of the embed"""
        return

    async def add_points(self,points):
        """Ajoute ou enlève un certain nombre de points au score
        La principale utilité de cette fonction est de pouvoir check le nombre de points à chaque changement"""
        self.points += points
        if self.points<0:
            self.points = 0

    async def add_event(self,event):
        if event == "kick":
            await self.add_points(-self.table['kick'])
        elif event == "ban":
            await self.add_points(-self.table['ban'])


    async def check_user_left(self,member):
        """Vérifie si un joueur a été banni ou kick par ZBot"""
        try:
            async for entry in member.guild.audit_logs(user=member.guild.me,limit=15):
                if entry.created_at < datetime.datetime.utcnow()-datetime.timedelta(seconds=60):
                    break
                if entry.action==discord.AuditLogAction.kick and entry.target==member:
                    await self.add_points(self.table['kick'])
                    break
                elif entry.action==discord.AuditLogAction.ban and entry.target==member:
                    await self.add_points(self.table['ban'])
                    break
        except Exception as e:
            print("[check_user_left] {} (user {}/server {})".format(e,member.id,member.guild.id))
            return


def setup(bot):
    bot.add_cog(Events(bot))