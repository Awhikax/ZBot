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
        await self.bot.cogs["ServerCog"].update_memberChannel(member.guild)
        await self.send_msg(member,"welcome")
        self.bot.loop.create_task(self.give_roles(member))
        await self.send_log(member,"welcome")
        
    
    async def bye_member(self,member):
        """Fonction principale appelée lorsqu'un membre quitte un serveur"""
        await self.bot.cogs["ServerCog"].update_memberChannel(member.guild)
        await self.send_msg(member,"leave")
        await self.send_log(member,"leave")
        await self.bot.cogs['Events'].check_user_left(member)


    async def send_msg(self,member,Type):
        msg = await self.bot.cogs['ServerCog'].find_staff(member.guild.id,Type)
        if await self.raid_check(member) or member.id in self.no_message:
            return
        if await self.bot.cogs['UtilitiesCog'].check_any_link(member.name) != None:
            return
        if msg not in ['',None]:
            ch = await self.bot.cogs['ServerCog'].find_staff(member.guild.id,'welcome_channel')
            if ch == None:
                return
            ch = ch.split(';')
            for channel in ch:
                if not channel.isnumeric():
                    continue
                channel = member.guild.get_channel(int(channel))
                if channel == None:
                    continue
                try:
                    msg = msg.format(user=member.mention if Type=='welcome' else member.name,server=member.guild.name,owner=member.guild.owner.name,member_count=len(member.guild.members))
                    msg = await self.bot.cogs["UtilitiesCog"].clear_msg(msg,everyone=False)
                    await channel.send(msg)
                except Exception as e:
                    await self.bot.cogs["ErrorsCog"].on_error(e,None)

    async def kick(self,member,reason):
        try:
            await member.guild.kick(member,reason=reason)
        except:
            pass
    
    async def ban(self,member,reason):
        try:
            await member.guild.ban(member,reason=reason)
        except:
            pass

    async def raid_check(self,member):
        if member.guild == None:
            return False
        level = str(await self.bot.cogs['ServerCog'].find_staff(member.guild.id,"anti_raid"))
        if not level.isnumeric() or member.guild.channels[0].permissions_for(member.guild.me).kick_members == False:
            return
        c = False
        level = int(level)
        can_ban = member.guild.get_member(self.bot.user.id).guild_permissions.ban_members
        if level == 0:
            return c
        if level >= 1:
            if await self.bot.cogs['UtilitiesCog'].check_discord_invite(member.name) != None:
                await self.kick(member,"Automod (Discord invite)")
                c = True
        if level >= 2:
            if (datetime.datetime.now() - member.created_at).seconds <= 1*60:
                await self.kick(member,"Automod (too young account)")
                c = True
        if level >= 3 and can_ban:
            if await self.bot.cogs['UtilitiesCog'].check_discord_invite(member.name) != None:
                await self.ban(member,"Automod (Discord invite)")
                c = True
            if (datetime.datetime.now() - member.created_at).seconds <= 5*60:
                await self.kick(member,"Automod (too young account)")
                c = True
        if level >= 4:
            if (datetime.datetime.now() - member.created_at).seconds <= 10*60:
                await self.kick(member,"Automod (too young account)")
                c = True
            if (datetime.datetime.now() - member.created_at).seconds <= 3*60 and can_ban:
                await self.ban(member,"Automod (too young account)")
                c = True
        return c


    async def give_roles(self,member):
        """Give new roles to new users"""
        try:
            roles = str(await self.bot.cogs['ServerCog'].find_staff(member.guild.id,"gived_roles"))
            for r in roles.split(";"):
                if (not r.isnumeric()) or len(r)==0:
                    continue
                role = member.guild.get_role(int(r))
                if role != None:
                    await member.add_roles(role,reason="Automated action (config gived_roles)")
        except Exception as e:
            await self.bot.cogs["ErrorsCog"].on_error(e,None)


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