import discord, datetime
from discord.ext import commands

class WelcomerCog:
    """Cog which manages the departure and arrival of members in the servers"""
    
    def __init__(self,bot):
        self.bot = bot
        self.file = "bvn"
        self.no_message = [392766377078816789]
    

    async def new_member(self,member):
        """Fonction principale appelée lorsqu'un membre rejoint un serveur"""
        await self.send_log(member,"welcome")
        
    
    async def bye_member(self,member):
        """Fonction principale appelée lorsqu'un membre quitte un serveur"""
        await self.send_log(member,"leave")
        await self.bot.cogs['Events'].check_user_left(member)


    async def send_log(self,member,Type):
        """Send a log to the logging channel"""
        if member.id in self.no_message or member.id==self.bot.user.id:
            return
        if member.guild.id in self.bot.cogs['ReloadsCog'].ignored_guilds:
            return
        try:
            t = "Bot" if member.bot else "Member"
            if Type == "welcome":
                desc = "{} {} joined the server {}".format(t,member,member.guild.name)
            else:
                desc = "{} {} left the server {}".format(t,member,member.guild.name)
            emb = self.bot.cogs["EmbedCog"].Embed(desc=desc,color=16098851).update_timestamp().set_author(self.bot.user)
            await self.bot.cogs["EmbedCog"].send([emb])
        except Exception as e:
            await self.bot.cogs["ErrorsCog"].on_error(e,None)

def setup(bot):
    bot.add_cog(WelcomerCog(bot))