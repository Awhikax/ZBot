import importlib, sys
from discord.ext import commands

admins_id = [279568324260528128,281404141841022976]

class ReloadsCog:
    """Cog to manage the other cogs. Even if all are disabled, this is the last one left."""

    def __init__(self,bot):
        self.bot = bot
        self.file = "reloads"
        self.ignored_guilds = [471361000126414848,513087032331993090,500648624204808193,264445053596991498]
    
    async def reload_cogs(self,bot,ctx,cogs):
        errors_cog = bot.cogs["ErrorsCog"]
        for cog in cogs:
            backup = None
            if not cog.startswith("fctshl."):
                fcog = "fctshl."+cog
            try:
                try:
                    backup = eval("self.bot.cogs['{}']".format(cog))
                except:
                    pass
                bot.unload_extension(fcog)
                bot.load_extension(fcog)
            except ModuleNotFoundError:
                await ctx.send("Module {} can't be found".format(cog))
            except Exception as e:
                await errors_cog.on_error(e,ctx)
                await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
                if backup!=None:
                    self.bot.cogs[cog] = backup
            else:
                await self.bot.cogs["UtilitiesCog"].print2("Module {} rechargé".format(cog))
                await ctx.send('Reloaded {} module'.format(cog))

    @commands.command(name="add_cog",hidden=True)
    async def add_cog(self,ctx,name):
        """Ajouter un cog au bot"""
        if not ctx.author.id in admins_id:
            return
        try:
            self.bot.load_extension('fctshl.'+name)
            await ctx.send("Cog '{}' ajouté !".format(name))
        except Exception as e:
            await ctx.send(str(e))

    @commands.command(name="del_cog",aliases=['remove_cog'],hidden=True)
    async def rm_cog(self,ctx,name):
        """Enlever un cog au bot"""
        if not ctx.author.id in admins_id:
            return
        try:
            self.bot.unload_extension('fctshl.'+name)
            await ctx.send("Cog '{}' désactivé !".format(name))
        except Exception as e:
            await ctx.send(str(e))
            self.bot.unload_extension('fctshl.admin')
            self.bot.load_extension('fctshl.admin')


def setup(bot):
    bot.add_cog(ReloadsCog(bot))
