#!/usr/bin/env python
#coding=utf-8

import mysql.connector, time, datetime, emoji
import discord
from discord.ext import commands


class ServerCog:
    """"Cog in charge of all the bot configuration management for your server. As soon as an option is searched, modified or deleted, this cog will handle the operations."""

    def __init__(self,bot):
        self.bot = bot
        self.default_language = 'en'
        self.file = "server"
        try:
            self.translate = self.bot.cogs["LangCog"].tr
        except:
            pass

    async def on_ready(self):
        self.translate = self.bot.cogs["LangCog"].tr

    @commands.group(name='config')
    @commands.guild_only()
    @commands.cooldown(1,2,commands.BucketType.guild)
    async def sconfig_main(self,ctx):
        """Function for setting the bot on a server"""
        if ctx.invoked_subcommand is None:
            msg = await self.translate(ctx.guild,"server","config-help")
            await ctx.send(msg.format(ctx.guild.owner.name))
        elif ctx.invoked_subcommand not in ["help","see","change","del"]:
            return None

    @sconfig_main.command(name="help")
    async def sconfig_help(self,ctx):
        """Displays a help message"""
        msg = await self.translate(ctx.guild,"server","config-help")
        await ctx.send(msg)

    @sconfig_main.command(name="del",hidden=True)
    async def sconfig_del(self,ctx,option):
        """Reset an option to zero"""
        if not (ctx.channel.permissions_for(ctx.author).administrator or await self.bot.cogs["AdminCog"].check_if_admin(ctx)):
            return
        await ctx.send("Unable to do this, our database is currently offline :confused:")
    
    @sconfig_main.command(name="change",hidden=True)
    async def sconfig_change(self,ctx,option,*,value):
        """Allows you to modify an option"""
        await ctx.send("Unable to do this, our database is currently offline :confused:")
    
    @sconfig_main.command(name="see",hidden=True)
    @commands.cooldown(1,10,commands.BucketType.guild)
    async def sconfig_see(self,ctx,option=None):
        """Displays the value of an option, or all options if none is specified"""
        await ctx.send("Unable to do this, our database is currently offline :confused:")

            
    @sconfig_main.command(name="delete",hidden=True)
    @commands.is_owner()
    async def admin_delete(self,ctx,ID:int):
        await ctx.send("Impossible de faire ceci, la base de donnée est inatteignable :confused:")



    async def update_memberChannel(self,guild):
        return None
    
    
def setup(bot):
    bot.add_cog(ServerCog(bot))
