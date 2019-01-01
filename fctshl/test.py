import discord, datetime, inspect, random
from discord.ext import commands

from docs import conf

class TestCog:
    """Hey, I'm a test cog! Happy to meet you :wave:"""

    def __init__(self, bot):
        self.bot = bot

    
    @commands.command(name="test")
    @commands.is_owner()
    async def test(self,ctx):
        await random.choice([self.bot.cogs['Events'].on_guild_add(ctx.guild), self.bot.cogs['Events'].on_guild_del(ctx.guild)])

    def change_all(self,text):
        return "Test: {} <3".format(text)
    

def setup(bot):
    bot.add_cog(TestCog(bot))
