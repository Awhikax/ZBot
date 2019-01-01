#!/usr/bin/env python
#coding=utf-8

import time
t1=time.time()


#Here we import some libs
count = 0
for m in ["timeout_decorator","mysql","discord","frmc_lib","requests","re","asyncio","feedparser","datetime","time","importlib","traceback","sys","logging","sympy","psutil","platform","subprocess"]:
    try:
        exec("import "+m)
        exec("del "+m)
    except ModuleNotFoundError:
        print("Library {} manquante".format(m))
        count +=1
if count>0:
    raise
del count

import discord, sys, traceback, asyncio, time, logging, os
from signal import SIGTERM
from platform   import system as system_name  # Returns the system/OS name
from subprocess import call   as system_call  # Execute a shell command

from discord.ext import commands

def get_prefix(bot,msg):
    if database_online:
        l = [bot.cogs['UtilitiesCog'].find_prefix(msg.guild)]
    else:
        l = ['!']
    if msg.guild != None:
        return l+[msg.guild.me.mention+" "]
    else:
        return l+[bot.user.mention+" "]

client = commands.Bot(command_prefix=get_prefix,case_insensitive=True,status=discord.Status('online'))


param = '-n' if system_name().lower()=='windows' else '-c'
command = ['ping', param, "2",'-i',"0.3",'-q', "37.44.236.84"]
r = system_call(command)
database_online = r == 1 or r==0
if not database_online:
    print(r)
    print("\nERROR: UNABLE TO PING THE DATABASE\n\n")

initial_extensions = ['fcts.admin',
                      'fcts.utilities',
                      'fcts.reloads',
                      'fcts.language',
                      'fcts.server',
                      'fcts.errors',
                      'fcts.perms',
                      'fcts.aide',
                      'fcts.mc',
                      'fcts.infos',
                      'fcts.timeclass',
                      'fcts.fun',
                      'fcts.rss',
                      'fcts.moderation',
                      'fcts.cases',
                      'fcts.bvn',
                      'fcts.emoji',
                      'fcts.embeds',
                      'fcts.events'
  ]


# Suppression du fichier debug.log s'il est trop volumineux
if os.path.exists("debug.log"):
    s = os.path.getsize('debug.log')/1.e9
    if s>10:
        print("Taille de debug.log supérieure à 10Gb ({}Gb)\n   -> Suppression des logs".format(s))
        os.remove('debug.log')
    del s

#Seting-up logs
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='debug.log', encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


def load_cogs():
    """Here we load our extensions(cogs) listed above in [initial_extensions]."""
    global database_online, client
    count = 0
    for extension in initial_extensions:
        if not database_online:
            extension = extension.replace('fcts','fctshl')
        try:
            client.load_extension(extension)
        except:
            print(f'\nFailed to load extension {extension}', file=sys.stderr)
            traceback.print_exc()
            count += 1
    if count >0:
        if not database_online:
            raise Exception("\n{} modules not loaded".format(count))
        else:
            count = 0
            database_online = False
        for extension in initial_extensions:
            try:
                client.unload_extension(extension)
            except Exception as e:
                print("••••• ",e)
            try:
                client.load_extension(extension.replace('fcts','fctshl'))
            except:
                print(f'\nFailed to load extension {extension}', file=sys.stderr)
                traceback.print_exc()
                count += 1
        if count >0:
            raise Exception("\n{} modules not loaded".format(count))

load_cogs()


@client.check_once
async def check_once(ctx):
    try:
        return await client.cogs['UtilitiesCog'].global_check(ctx)
    except:
        return True

utilities = client.cogs["UtilitiesCog"]

#@client.event
async def on_ready():
    global r
    await utilities.print2('\nBot connecté')
    await utilities.print2("Nom : "+client.user.name)
    await utilities.print2("ID : "+str(client.user.id))
    serveurs = []
    for i in client.guilds:
        serveurs.append(i.name)
    ihvbsdi="Connecté sur ["+str(len(client.guilds))+"] "+", ".join(serveurs)
    await utilities.print2(ihvbsdi)
    await utilities.print2(time.strftime("%d/%m  %H:%M:%S"))
    await utilities.print2("Prêt en "+str(t1+(time.time()-t2))+" sec")
    await utilities.print2('------')
    await asyncio.sleep(3)
    if not database_online:
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,name="for a signal"))
    elif r=='1':
        await client.change_presence(activity=discord.Game(name="entrer !help"))
    elif r=='2':
        await client.change_presence(activity=discord.Game(name="SNAPSHOOT"))
    emb = client.cogs["EmbedCog"].Embed(desc="Bot **{} is launching** !".format(client.user.name),color=8311585).update_timestamp()
    await client.cogs["EmbedCog"].send([emb])

#@client.event
async def on_member_join(member):
    await client.cogs['WelcomerCog'].new_member(member)
    return

#@client.event
async def on_member_remove(member):
    await client.cogs['WelcomerCog'].bye_member(member)
    return

async def on_guild_join(guild):
    await client.cogs["Events"].on_guild_add(guild)
    return

async def on_guild_remove(guild):
    await client.cogs["Events"].on_guild_del(guild)
    return

async def on_message(msg):
    await client.cogs["Events"].on_new_message(msg)


async def sigterm_handler(bot):
    print("SIGTERM received. Disconnecting...")
    await bot.logout()

# à mettre avant de lancer le bot
asyncio.get_event_loop().add_signal_handler(SIGTERM, lambda: asyncio.ensure_future(sigterm_handler(client)))


if database_online:
    try:
        from fcts import tokens
    except:
        database_online = False
        t1=time.time()-t1
if database_online:
    r=input("Quel bot activer ? (1 release, 2 snapshot) ")
    if r=='1':
        token = tokens.get_token(486896267788812288)
    elif r=='2':
        token = tokens.get_token(436835675304755200)
    else:
        sys.exit()
    if r in ['1','2']:
        r2=input("Lancement de la boucle rss ? (o/n) ")
        if r2=='o':
            client.loop.create_task(client.cogs["RssCog"].loop())
else:
    token = input("Token?\n> ")
t2=time.time()


client.add_listener(on_ready)
client.add_listener(on_member_join)
client.add_listener(on_member_remove)
client.add_listener(on_message)
client.add_listener(on_guild_join)
client.add_listener(on_guild_remove)

client.run(token)
