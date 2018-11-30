#!/usr/bin/env python
#coding=utf-8

import time
t1=time.time()


#Here we import some libs
count = 0
for m in ["timeout_decorator","mysql","discord","frmc_lib","requests","re","asyncio","feedparser","datetime","time","importlib","traceback","sys","logging","sympy","psutil"]:
    try:
        exec("import "+m)
        exec("del "+m)
    except ModuleNotFoundError:
        print("Library {} manquante".format(m))
        count +=1
if count>0:
    raise
del count

import discord, sys, traceback, asyncio, time, logging


from discord.ext import commands

def get_prefix(bot,msg):
    try:
        p = bot.cogs['UtilitiesCog'].find_prefix(msg.guild)
    except:
        p = '!'
    if p == '':
        p = '!'
    return p

client = commands.Bot(command_prefix=get_prefix,case_insensitive=True,status=discord.Status('online'))


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

#Seting-up logs
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='debug.log', encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


# Here we load our extensions(cogs) listed above in [initial_extensions].
if __name__ == '__main__':
    count = 0
    for extension in initial_extensions:
        try:
            client.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}', file=sys.stderr)
            traceback.print_exc()
            count += 1
    if count >0:
        raise Exception("{} modules not loaded".format(count))
    del count


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
    if r=='1':
        await client.change_presence(activity=discord.Game(name="entrer !help"))
    elif r=='2':
        await client.change_presence(activity=discord.Game(name="SNAPSHOOT"))
    elif r=='3':
        await client.change_presence(activity=discord.Game(name="Gunivers !"))
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

from fcts import tokens
t1=time.time()-t1
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
    #r3=input("Lancement de la boucle hunting ? (o/n) ")
    #if r3=='o':
        #client.loop.create_task(hunter.loop(client))
    #r4=input("Lancement de la boucle backup ? (o/n) ")
    #if r4=='o':
        #client.loop.create_task(admin.backup_loop(client))
t2=time.time()


client.add_listener(on_ready)
client.add_listener(on_member_join)
client.add_listener(on_member_remove)
client.add_listener(on_message)
client.add_listener(on_guild_join)
client.add_listener(on_guild_remove)

client.run(token)
