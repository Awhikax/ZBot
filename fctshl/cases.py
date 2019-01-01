import discord, mysql.connector
from discord.ext import commands


async def can_edit_case(ctx):
       return False

class CasesCog:
    """This part of the bot allows you to manage all your members' cases, to delete or edit them"""

    def __init__(self,bot):
        self.bot = bot
        self.file = "cases"
        try:
            self.translate = self.bot.cogs["LangCog"].tr
        except:
            pass
    
    async def on_ready(self):
        self.translate = self.bot.cogs["LangCog"].tr


    @commands.group(name="cases",hidden=True)
    @commands.guild_only()
    @commands.cooldown(5, 15, commands.BucketType.user)
    @commands.check(can_edit_case)
    async def case_main(self,ctx):
        """Do anything with any user cases"""
        return

    @case_main.command(name="list")
    @commands.guild_only()
    @commands.cooldown(5, 30, commands.BucketType.user)
    async def see_case(self,ctx,user,guild:int=None):
        """Get every case of a user
        This user can have left the server"""
        await ctx.send("Unable to do that: our database is currently offline :confused:")
    

    @case_main.command(name="reason",hidden=True)
    @commands.guild_only()
    async def reason(self,ctx,case:int,*,reason):
        """Edit the reason of a case"""
        await ctx.send("Unable to do that: our database is currently offline :confused:")
    
    @case_main.command(name="search")
    @commands.guild_only()
    async def search_case(self,ctx,case:int):
        """Search for a specific case in your guild"""
        await ctx.send("Unable to do that: our database is currently offline :confused:")
        

    @case_main.command(name="remove",aliases=["clear","delete"],hidden=True)
    @commands.guild_only()
    async def remove(self,ctx,case:int):
        """Delete a case forever
        Warning: "Forever", it's very long. And no backups are done"""
        await ctx.send("Unable to do that: our database is currently offline :confused:")


def setup(bot):
    bot.add_cog(CasesCog(bot))