import discord
from discord.ext import commands


import time, importlib, sys, traceback, datetime, os, shutil, asyncio, inspect, typing, io, textwrap, copy
from contextlib import redirect_stdout
from fcts import  reloads
importlib.reload(reloads)



async def check_admin(ctx):
        if type(ctx) == commands.Context:
            user = ctx.author
        else:
            user = ctx
        if type(user) == str and user.isnumeric():
            user = int(user)
        elif type(user) != int:
            user = user.id
        return user in reloads.admins_id

def cleanup_code(content):
    """Automatically removes code blocks from the code."""
    # remove ```py\n```
    if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])
    # remove `foo`
    return content.strip('` \n')

class AdminCog:
    """Here are listed all commands related to the internal administration of the bot. Most of them are not accessible to users, but only to ZBot administrators."""
        
    def __init__(self, bot):
        self.bot = bot
        self.file = "admin"
        self.emergency_time = 5.0
        try:
            self.translate = self.bot.cogs["LangCog"].tr
            self.print = self.bot.cogs["UtilitiesCog"].print2
            self.utilities = self.bot.cogs["UtilitiesCog"]
        except:
            pass
        self._last_result = None
        
    async def on_ready(self):
        self.translate = self.bot.cogs["LangCog"].tr
        self.print = self.bot.cogs["UtilitiesCog"].print2
        self.utilities = self.bot.cogs["UtilitiesCog"]

    async def check_if_admin(self,ctx):
        return await check_admin(ctx)

    
    @commands.command(name='admins')
    async def admin_list(self,ctx):
        """Get the list of ZBot administrators"""
        l  = list()
        for u in reloads.admins_id:
            l.append(str(self.bot.get_user(u)))
        await ctx.send("Les administrateurs de ce bot sont : {}".format(", ".join(l)))

    @commands.group(name='admin')
    @commands.check(check_admin)
    async def main_msg(self,ctx):
        #if not await self.check_if_admin(ctx.author):
            #return
        """Commandes réservées aux administrateurs de ZBot"""
        if ctx.invoked_subcommand is None:
            text = "Liste des commandes disponibles :"
            for cmd in self.main_msg.commands:
                text+="\n- {} *({})*".format(cmd.name,cmd.help)
                if type(cmd)==commands.core.Group:
                    for cmds in cmd.commands:
                        text+="\n        - {} *({})*".format(cmds.name,cmds.help)
            await ctx.send(text)

    @main_msg.command(name="cogs",hidden=True)
    @commands.check(check_admin)
    async def cogs_list(self,ctx):
        """Voir la liste de tout les cogs"""
        text = str()
        for k,v in self.bot.cogs.items():
            text +="- {} ({}) \n".format(v.file,k)
        await ctx.send(text)

    @main_msg.command(name="guilds",aliases=['servers'],hidden=True)
    @commands.check(check_admin)
    async def send_guilds_list(self,ctx):
        """Obtenir la liste de tout les serveurs"""
        text = str()
        for x in self.bot.guilds:
            text += "- {} (`{}` - {} membres)\n".format(x.name,x.owner,len(x.members))
        await ctx.send(text)

    @main_msg.command(name='shutdown')
    @commands.check(check_admin)
    async def shutdown(self,ctx,arg=""):
        """Eteint le bot"""
        if arg != "no-backup":
            m = await ctx.send("Création de la sauvegarde...")
            #await backup_auto(client)
            await m.edit(content="Bot en voie d'extinction")
        else:
            await ctx.send("Bot en voie d'extinction")
        await self.bot.change_presence(status=discord.Status('offline'))
        await self.print("Bot en voie d'extinction")
        await self.bot.close()

    @main_msg.command(name='reload')
    @commands.check(check_admin)
    async def cog_reload(self, ctx, *, cog: str):
        """Recharge un module"""
        cogs = cog.split(" ")
        await self.bot.cogs["ReloadsCog"].reload_cogs(self.bot,ctx,cogs)
        
    @main_msg.command(name="check_tr")
    @commands.check(check_admin)
    async def check_tr(self,ctx,lang='en'):
        """Vérifie si un fichier de langue est complet"""
        await self.bot.cogs["LangCog"].check_tr(ctx.channel,lang)

    @main_msg.command(name="backup")
    @commands.check(check_admin)
    async def adm_backup(self,ctx):
        """Exécute une sauvegarde complète du code"""
        await self.backup_auto(ctx)

    @main_msg.command(name="membercounter")
    @commands.check(check_admin)
    async def membercounter(self,ctx):
        """Recharge tout ces salons qui contiennent le nombre de membres, pour tout les serveurs"""
        for x in self.bot.guilds:
            await self.bot.cogs["ServerCog"].update_memberChannel(x)
        await ctx.send(":ok_hand:")

    @main_msg.command(name="get_invites",aliases=['invite'])
    @commands.check(check_admin)
    async def adm_invites(self,ctx,*,server=None):
        """Cherche une invitation pour un serveur, ou tous"""
        if server != None:
            guild = discord.utils.get(self.bot.guilds, name=server)
            if guild == None and server.isnumeric():
                guild = discord.utils.get(self.bot.guilds, id=int(server))
            await ctx.author.send(await self.search_invite(guild,server))
        else:
            liste = list()
            for guild in self.bot.guilds:
                liste.append(await self.search_invite(guild,guild))
            msg = "\n".join(liste)
            await ctx.author.send(msg)
        await self.bot.cogs['UtilitiesCog'].suppr(ctx.message)

    async def search_invite(self,guild,string):
        if guild==None:
            return "Le serveur `{}` n'a pas été trouvé".format(string)
        try:
            inv = await guild.invites()
            if len(inv)>0:
                msg = "`{}` - {} ({} membres) ".format(guild.name,inv[0],len(guild.members))
            else:
                msg = "`{}` - Le serveur ne possède pas d'invitation".format(guild.name)
        except discord.Forbidden:
            msg = "`{}` - Impossible de récupérer l'invitation du serveur (Forbidden)".format(guild.name)
        except Exception as e:
            msg = "`ERROR:` "+str(e)
            await self.bot.cogs['ErrorsCog'].on_error(e,None)
        return msg

    @main_msg.command(name="config")
    @commands.check(check_admin)
    async def admin_sconfig_see(self,ctx,*,server):
        """Affiche les options d'un serveur"""
        if server.isnumeric():
            guild = discord.utils.get(self.bot.guilds,id=int(server))
        else:
            guild = discord.utils.get(self.bot.guilds,name=server)
        if guild != None:
            await self.bot.cogs["ServerCog"].send_see(guild,ctx.channel,None,ctx.message,None)
        else:
            await ctx.send("Serveur introuvable")

    @main_msg.command(name="emergency")
    @commands.check(check_admin)
    async def emergency_cmd(self,ctx):
        """Déclenche la procédure d'urgence
        A N'UTILISER QU'EN CAS DE BESOIN ABSOLU ! Le bot quittera tout les serveurs après avoir envoyé un mp à chaque propriétaire"""
        await ctx.send(await self.emergency())

    async def emergency(self,level=100):
        for x in reloads.admins_id:
            try:
                user = self.bot.get_user(x)
                print(type(user),user)
                if user.dm_channel==None:
                    await user.create_dm()
                time = round(self.emergency_time - level/100,1)
                msg = await user.dm_channel.send("{} La procédure d'urgence vient d'être activée. Si vous souhaitez l'annuler, veuillez cliquer sur la réaction ci-dessous dans les {} secondes qui suivent l'envoi de ce message.".format(self.bot.cogs['EmojiCog'].customEmojis['red_warning'],time))
                await msg.add_reaction('🛑')
            except Exception as e:
                await self.bot.cogs['ErrorsCog'].on_error(e,None)

        def check(reaction, user):
            return user.id in reloads.admins_id
        try:
            await self.bot.wait_for('reaction_add', timeout=time, check=check)
        except asyncio.TimeoutError:
            owners = list()
            servers = 0
            for server in self.bot.guilds:
                if server.id==500648624204808193:
                    continue
                try:
                    if server.owner not in owners:
                        await server.owner.send(await self.translate(server,"admin","emergency"))
                        owners.append(server.owner)
                    await server.leave()
                    servers +=1
                except:
                    continue
            chan = await self.bot.get_channel(500674177548812306)
            await chan.send("{} Prodédure d'urgence déclenchée : {} serveurs quittés - {} propriétaires prévenus".format(self.bot.cogs['EmojiCog'].customEmojis['red_alert'],servers,len(owners)))
            return "{}  {} propriétaires de serveurs ont été prévenu ({} serveurs)".format(self.bot.cogs['EmojiCog'].customEmojis['red_alert'],len(owners),servers)
        for x in reloads.admins_id:
            try:
                user = self.bot.get_user(x)
                await user.send("La procédure a été annulée !")
            except Exception as e:
                await self.bot.cogs['ErrorsCog'].on_error(e,None)
        return "Qui a appuyé sur le bouton rouge ? :thinking:"

    @main_msg.command(name="code")
    async def show_code(self,ctx,cmd):
        cmds = self.bot.commands
        obj = await self.bot.cogs['UtilitiesCog'].set_find(cmds,cmd)
        if obj != None:
            await ctx.send("```py\n{}\n```".format(inspect.getsource(obj.callback)))
        else:
            await ctx.send("Commande `{}` introuvable".format(cmd))
    
    @main_msg.command(name="logs")
    @commands.check(check_admin)
    async def show_last_logs(self,ctx,lines:typing.Optional[int]=5,match=''):
        """Affiche les <lines> derniers logs ayant <match> dedans"""
        try:
            with open('debug.log','r',encoding='utf-8') as file:
                #try:
                    #file.seek(-300*lines,2)
                #except:
                    #pass
                text = file.read().split("\n")
            msg = str()
            liste = list()
            i = 2
            while len(liste)<=lines and i<len(text) and i<2000:
                i+=1
                if (not match in text[-i]) or ctx.message.content in text[-i]:
                    continue
                liste.append(text[-i].replace('`',''))
            for i in liste:
                if len(msg+i)>1900:
                    await ctx.send("```\n{}\n```".format(msg))
                    msg = ""
                if len(i)<1900:
                    msg += "\n"+i.replace('`','')
            await ctx.send("```\n{}\n```".format(msg))
        except Exception as e:
            await self.bot.cogs['ErrorsCog'].on_error(e,ctx)

    @main_msg.group(name="server")
    @commands.check(check_admin)
    async def main_botserv(self,ctx):
        """Quelques commandes liées au serveur officiel"""
        if ctx.invoked_subcommand is None or ctx.invoked_subcommand==self.main_botserv:
            text = "Liste des commandes disponibles :"
            for cmd in self.main_botserv.commands:
                text+="\n- {} *({})*".format(cmd.name,cmd.help)
            await ctx.send(text)

    @main_botserv.command(name="owner_reload")
    @commands.check(check_admin)
    async def owner_reload(self,ctx):
        """Ajoute le rôle Owner à tout les membres possédant un serveur avec le bot"""
        server = self.bot.get_guild(356067272730607628)
        for r in server.roles:
            if r.id == 486905171738361876:
                role = r
        owner_list = list()
        for guild in self.bot.guilds:
            await self.print("guild "+guild.name)
            if len(guild.members)>9:
                owner_list.append(guild.owner.id)
        for member in server.members:
            if member.id in owner_list and role not in member.roles:
                await ctx.send("Rôle ajouté à "+str(member))
                await member.add_roles(role,reason="This user support me")
            elif (member.id not in owner_list) and role in member.roles:
                await ctx.send("Rôle supprimé à "+str(member))
                await member.remove_roles(role,reason="This user doesn't support me anymore")

    @main_botserv.command(name="best_ideas")
    @commands.check(check_admin)
    async def best_ideas(self,ctx,number:int=10):
        """Donne la liste des 10 meilleures idées"""
        bot_msg = await ctx.send("Chargement des idées...")
        server = self.bot.get_guild(356067272730607628)
        channel = server.get_channel(488769306524385301)
        liste = list()
        async for msg in channel.history(limit=500):
            if len(msg.reactions) > 0:
                up = 0
                down = 0
                for x in msg.reactions:
                    users = await x.users().flatten()
                    if x.emoji == '👍':
                        up = x.count
                        if ctx.guild.me in users :
                            up -= 1
                    elif x.emoji == '👎':
                        down = x.count
                        if ctx.guild.me in users:
                            down -= 1
                liste.append((up-down,msg.content,up,down))
        liste.sort(reverse=True)
        count = len(liste)
        liste = liste[:number]
        text = "Liste des {} meilleures idées (sur {}) :".format(len(liste),count)
        for x in liste:
            text += "\n- {} ({} - {})".format(x[1],x[2],x[3])
        await bot_msg.edit(content=text)

    @commands.command(name="activity")
    @commands.check(check_admin)
    async def change_activity(self,ctx, Type: str, * act: str):
        """Change l'activité du bot (play, watch, listen, stream)"""
        act = " ".join(act)
        if Type in ['game','play']:
            await self.bot.change_presence(activity=discord.Game(name=act))
        elif Type in ['watch','see']:
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,name=act,timestamps={'start':time.time()}))
        elif Type in ['listen']:
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,name=act,timestamps={'start':time.time()}))
        elif Type in ['stream']:
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming,name=act,timestamps={'start':time.time()}))
        else:
            await ctx.send(await self.translate(ctx.guild.id,"admin","change_game-0"))
        await ctx.message.delete()
    

    @commands.command(name='eval')
    @commands.check(check_admin)
    async def _eval(self, ctx, *, body: str):
        """Evaluates a code
        Credits: Rapptz (https://github.com/Rapptz/RoboDanny/blob/rewrite/cogs/admin.py)"""
        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result
        }
        env.update(globals())

        body = cleanup_code(body)
        stdout = io.StringIO()
        try:
            to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'
        except Exception as e:
            await self.bot.cogs['ErrorsCog'].on_error(e,ctx)
            return
        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')
    
    @commands.command(name='execute',hidden=True)
    @commands.check(check_admin)
    async def sudo(self, ctx, who: typing.Union[discord.Member, discord.User], *, command: str):
        """Run a command as another user
        Credits: Rapptz (https://github.com/Rapptz/RoboDanny/blob/rewrite/cogs/admin.py)"""
        msg = copy.copy(ctx.message)
        msg.author = who
        msg.content = ctx.prefix + command
        new_ctx = await self.bot.get_context(msg)
        #new_ctx.db = ctx.db
        await self.bot.invoke(new_ctx)

    async def backup_auto(self,ctx=None):
        """Crée une backup du code"""
        t = time.time()
        await self.print("("+str(await self.bot.cogs['TimeCog'].date(datetime.datetime.now(),digital=True))+") Backup auto en cours")
        message = await ctx.send(":hourglass: Sauvegarde en cours...")
        try:
            os.remove('../backup.tar')
        except:
            pass
        try:
            archive = shutil.make_archive('backup','tar','..')
        except FileNotFoundError:
            await self.print("Impossible de trouver le dossier de sauvegarde")
            await message.edit("{} Impossible de trouver le dossier de sauvegarde".format(self.bot.cogs['EmojiCog'].customEmojis['red_cross']))
            return
        try:
            shutil.move(archive,'..')
        except shutil.Error:
            os.remove('../backup.tar')
            shutil.move(archive,'..')
        try:
            os.remove('backup.tar')
        except:
            pass
        msg = ":white_check_mark: Sauvegarde terminée en {} secondes !".format(round(time.time()-t,3))
        await self.print(msg)
        if ctx != None:
            await message.edit(content=msg)
            

        
# The setup function below is necessary. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(AdminCog(bot))
