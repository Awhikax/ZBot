import discord, random, operator, string, importlib, timeout_decorator, re, typing, datetime
import emoji as emojilib
from discord.ext import commands
from fcts import emoji
from sympy import Symbol, simplify
from sympy.solvers import solve
from math import *
importlib.reload(emoji)

cmds_list = ['count_msg','ragequit','pong','run','nope','blame','party','bigtext','shrug','gg','money','pibkac','osekour','me','kill','cat','rekt','thanos','nuke','pikachu','pizza','lmgtfy','loading','piece']

numbers_emojis = {"0":':zero:',
                  "1":':one:',
                  "2":':two:',
                  "3":':three:',
                  "4":':four:',
                  "5":':five:',
                  "6":':six:',
                  "7":':seven:',
                  "8":':eight:',
                  "9":':nine:',
                  "10":':keycap_ten: '
                  }

async def is_fun_enabled(ctx):
    self = ctx.bot.cogs["FunCog"]
    if ctx.guild == None:
        return True
    ID = ctx.guild.id
    if str(ID) not in self.fun_opt.keys():
        fun = await ctx.bot.cogs["ServerCog"].find_staff(ID,"enable_fun")
        self.fun_opt[str(ID)] = fun
    else:
        fun = self.fun_opt[str(ID)]
    return fun == 1 or fun == True

class FunCog:
    """Add some fun commands, no obvious use. You can disable this module with the 'enable_fun' option (command 'config')"""

    def __init__(self,bot):
        self.bot = bot
        self.fun_opt = dict()
        self.file = "fun"
        try:
            self.translate = self.bot.cogs["LangCog"].tr
        except:
            pass
        try:
            self.utilities = self.bot.cogs["UtilitiesCog"]
        except:
            pass

    async def cache_update(self,id,value):
        self.fun_opt[str(id)] = value

    async def on_ready(self):
            self.translate = self.bot.cogs["LangCog"].tr
            self.utilities = self.bot.cogs["UtilitiesCog"]

    async def is_on_frm(self,user):
        if self.bot.user.id == 436835675304755200:
            return True
        server = self.bot.get_guild(391968999098810388)
        if user.id in [279568324260528128,392766377078816789]:
            return True
        if server != None:
            return user in server.members
        return False

    

    @commands.command(name='fun')
    async def main(self,ctx):
        """Get a list of all fun commands"""
        if not await is_fun_enabled(ctx):
            await ctx.send(await self.translate(ctx.guild,"fun","no-fun"))
            return
        text = await self.translate(ctx.guild,"fun","fun-list")
        for cmd in sorted(self.bot.get_cog_commands('FunCog'),key=operator.attrgetter('name')):
            if cmd.name in cmds_list and cmd.enabled:
                if cmd.help != None:
                    text+="\n- {} *({})*".format(cmd.name,cmd.help.split('\n')[0])
                else:
                    text+="\n- {}".format(cmd.name)
                if type(cmd)==commands.core.Group:
                    for cmds in cmd.commands:
                        text+="\n    - {} *({})*".format(cmds.name,cmds.help)
        await ctx.send(text)

    @commands.command(name="cookie",hidden=True)
    @commands.check(is_fun_enabled)
    async def cookie(self,ctx):
        """COOKIE !!!"""
                            #Z_runner           neil3000            reddemoon           Adri526         Theventreur         Catastrophix        Platon_Neutron
        if ctx.author.id in [279568324260528128,278611007952257034,281404141841022976,409470110131027979,229194747862843392,438372385293336577,286827468445319168]:
            await ctx.send("{} a offert une boîte de cookies à <@375598088850505728> ! {}".format(ctx.author.mention,self.bot.cogs['EmojiCog'].customEmojis['cookies_eat']))
        elif ctx.author.id == 375598088850505728:
            await ctx.send(file=await self.utilities.find_img("cookie_target.png"))
        else:
            return

    @commands.command(name="count_msg",hidden=True)
    @commands.check(is_fun_enabled)
    async def count(self,ctx,limit:int=1000):
        """Count the number of messages sent by the user
You can specify a verification limit by adding a number in argument"""
        l = 100000
        if limit > l:
            await ctx.send(str(await self.translate(ctx.guild,"fun","count-2")).format(l=l,e=self.bot.cogs['EmojiCog'].customEmojis['wat']))
            return
        if not ctx.channel.permissions_for(ctx.guild.me).read_message_history:
            await ctx.send(str(await self.translate(ctx.guild,"fun","count-3")).format(l))
            return
        counter = 0
        tmp = await ctx.send(await self.translate(ctx.guild,'fun','count-0'))
        m = 0
        async for log in ctx.channel.history(limit=limit):
            m += 1
            if log.author == ctx.author:
                counter += 1
        r = round(counter*100/m,2)
        await tmp.edit(content = str(await self.translate(ctx.guild,'fun','count-1')).format(m,counter,r))

    @commands.command(name="ragequit",hidden=True)
    @commands.check(is_fun_enabled)
    async def ragequit(self,ctx):
        """To use when you get angry - limited to certain members"""
        await ctx.send(file=await self.utilities.find_img('ragequit{0}.gif'.format(random.randint(1,6))))

    @commands.command(name="run",hidden=True)
    @commands.check(is_fun_enabled)
    async def run(self,ctx):
        """"Just... run... very... fast"""
        await ctx.send("ε=ε=ε=┏( >_<)┛")

    @commands.command(name="pong",hidden=True)
    @commands.check(is_fun_enabled)
    async def pong(self,ctx):
        """Ping !"""
        await ctx.send("Ping !")

    @commands.command(name="nope",hidden=True)
    @commands.check(is_fun_enabled)
    async def nope(self,ctx):
        """Use this when you do not agree with your interlocutor"""
        c = await self.bot.cogs["ServerCog"].staff_finder(ctx.author,'say')
        await ctx.send(file=await self.utilities.find_img('nope.png'))
        if c:
            await self.utilities.suppr(ctx.message)

    @commands.command(name="blame",hidden=True)
    @commands.check(is_fun_enabled)
    async def blame(self,ctx,name):
        """Blame someone
        Use 'blame list' command to see every available name *for you*"""
        l1 = ['discord','mojang','zbot','google']
        l2 = ['zrunner','tronics','aragorn','patate','neil','reddemoon','aragorn1202']
        name = name.lower()
        if name in l1:
            await ctx.send(file=await self.utilities.find_img('blame-{}.png'.format(name)))
        elif name in l2:
            if await self.is_on_frm(ctx.author):
                await ctx.send(file=await self.utilities.find_img('blame-{}.png'.format(name)))
        elif name in ['help','list']:
            liste = l1
            if await self.is_on_frm(ctx.author):
                liste += l2
            txt = "- "+"\n- ".join(sorted(liste))
            title = str(await self.translate(ctx.guild,"fun","blame-0")).format(ctx.author)
            if ctx.channel.permissions_for(ctx.guild.me).embed_links:
                emb = self.bot.cogs["EmbedCog"].Embed(title=title,desc=txt,color=self.bot.cogs["HelpCog"].help_color).update_timestamp()
                await ctx.send(embed=emb.discord_embed())
            else:
                await ctx.send("__{}:__\n\n{}".format(title,txt))

    @commands.command(name="kill",hidden=True)
    @commands.guild_only()
    @commands.check(is_fun_enabled)
    async def kill(self,ctx,*,name=None):
        if name == None:
            victime = ctx.author.display_name
            ex = ctx.author.display_name.replace(" ","_")
        else:
            victime = name
            ex = name.replace(" ","_")
        author = ctx.author.mention
        liste = await self.translate(ctx.guild,"kill","list")
        msg = random.choice(liste)
        tries = 0
        while '{0}' in msg and name == None and tries<50:
            msg = random.choice(liste)
            tries += 1
        await ctx.send(msg.format(author,victime,ex))

    @commands.command(name="arapproved",aliases=['arapprouved'],hidden=True)
    @commands.check(lambda ctx: ctx.author.id in [375598088850505728,279568324260528128])
    async def arapproved(self,ctx):
        await ctx.send(file=await self.utilities.find_img("arapproved.png"))

    @commands.command(name='party',hidden=True)
    @commands.check(is_fun_enabled)
    async def party(self,ctx):
        """Sends a random image to make the server happier"""
        r = random.choice([1,2,3,4,5])
        if r == 1:
            await ctx.send(file=await self.utilities.find_img('cameleon.gif'))
        elif r == 2:
            await ctx.send(file=await self.utilities.find_img('discord_party.gif'))
        elif r == 3:
            await ctx.send(file=await self.utilities.find_img('parrot.gif'))
        elif r == 4:
            e = self.bot.cogs['EmojiCog'].customEmojis['blob_dance']
            await ctx.send(e*5)
        elif r == 5:
            await ctx.send(file=await self.utilities.find_img('cameleon.gif'))

    @commands.command(name="cat",hidden=True)
    @commands.check(is_fun_enabled)
    async def cat_gif(self,ctx):
        """Wow... So cuuuute !"""
        await ctx.send(random.choice(['http://images6.fanpop.com/image/photos/40800000/tummy-rub-kitten-animated-gif-cute-kittens-40838484-380-227.gif','http://25.media.tumblr.com/7774fd7794d99b5998318ebd5438ba21/tumblr_n2r7h35U211rudcwro1_400.gif','https://www.2tout2rien.fr/wp-content/uploads/2014/10/37-pestes-de-chats-mes-bonbons.gif',
        'https://snowchvojnica.eu/assets/cat.gif',
        'http://coquelico.c.o.pic.centerblog.net/chat-peur.gif']))
    
    @commands.command(name="bigtext",hidden=True)
    @commands.check(is_fun_enabled)
    async def big_text(self,ctx,*,text):
        """If you wish to write bigger"""
        text1 = []
        emojis = numbers_emojis
        contenu = str(await self.bot.cogs['UtilitiesCog'].anti_code(text)).split()
        for l in " ".join(contenu):
            if l in string.ascii_letters:
                text1.append(":regional_indicator_{0}:".format(l.lower()))
            elif l in string.digits:
                text1.append("{0}".format(emojis[l]))
            elif l == " ":
                text1.append(self.bot.cogs['EmojiCog'].customEmojis['nothing'])
            elif l == "#":
                text1.append(":hash:")
            elif l == "*":
                text1.append(":asterisk:")
            elif l == "?":
                text1.append(":grey_question:")
            elif l == "!":
                text1.append(":grey_exclamation:")
            elif l == '-':
                text1.append(":heavy_minus_sign:")
            elif l == "+":
                text1.append(":heavy_plus_sign:")
            elif l == "÷":
                text1.append(":heavy_division_sign:")
            elif l == ".":
                text1.append(":small_blue_diamond:")
            elif l in ["(",")",",","'","\"","=","/","¬"]:
                text1.append(l)
            caract = len("".join(text1))
            if caract>1970:
                await ctx.channel.send(str("".join(text1)).replace("¬¬","\n"))
                text1 = []
        if text1 != []:
            await ctx.channel.send(str("".join(text1)).replace("¬¬","\n"))
        if await self.bot.cogs["ServerCog"].staff_finder(ctx.author,'say'):
            await self.bot.cogs["UtilitiesCog"].suppr(ctx.message)
    
    @commands.command(name="shrug",hidden=True)
    @commands.check(is_fun_enabled)
    async def shrug(self,ctx):
        """Don't you know? Neither do I"""
        await ctx.send(file=await self.utilities.find_img('shrug.gif'))
    
    @commands.command(name="rekt",hidden=True)
    @commands.check(is_fun_enabled)
    async def rekt(self,ctx):
        await ctx.send(file=await self.utilities.find_img('rekt.jpg'))

    @commands.command(name="gg",hidden=True)
    @commands.check(is_fun_enabled)
    async def gg(self,ctx):
        await ctx.send(file=await self.utilities.find_img('gg.gif'))
    
    @commands.command(name="money",hidden=True)
    @commands.check(is_fun_enabled)
    async def money(self,ctx):
        await ctx.send(file=await self.utilities.find_img('money.gif'))
    
    @commands.command(name="pibkac",hidden=True)
    @commands.check(is_fun_enabled)
    async def pibkac(self,ctx):
        await ctx.send(file=await self.utilities.find_img('pibkac.png'))
    
    @commands.command(name="osekour",hidden=True)
    @commands.check(is_fun_enabled)
    async def osekour(self,ctx):
        l = await self.translate(ctx.guild,"fun","osekour")
        await ctx.send(random.choice(l))
    
    @commands.command(name="say")
    async def say(self,ctx,channel:typing.Optional[discord.TextChannel] = None,*,text):
        """Let the bot say something for you
        You can specify a channel where the bot must send this message. If channel is None, the current channel will be used"""
        await self.say_function(ctx,channel,text)
    
    async def say_function(self,ctx,channel,text):
        if not await self.bot.cogs["ServerCog"].staff_finder(ctx.author,"say"):
            return
        try:
            text = await self.bot.cogs["UtilitiesCog"].clear_msg(text,everyone = not ctx.channel.permissions_for(ctx.author).mention_everyone, ctx=ctx)
            if channel==None:
                channel = ctx.channel
        except Exception as e:
            await self.bot.cogs['ErrorsCog'].on_error(e,ctx)
            return
        try:
            await channel.send(text)
            await self.bot.cogs["UtilitiesCog"].suppr(ctx.message)
        except:
            pass

    @say.error
    async def say_error(self,ctx,error):
        await self.say_function(ctx,None,ctx.view.buffer.replace(ctx.prefix+ctx.invoked_with,""))

    @commands.command(name="me",hidden=True)
    @commands.check(is_fun_enabled)
    async def me(self,ctx,*,text):
        """No U"""
        await ctx.send("*{} {}*".format(ctx.author.display_name,text))
        if await self.bot.cogs["ServerCog"].staff_finder(ctx.author,"say"):
            await self.bot.cogs["UtilitiesCog"].suppr(ctx.message)
    
    @commands.command(name="react")
    async def react(self,ctx,ID:int,*,reactions):
        """Add reaction(s) to a message. Server emojis also work."""
        if not await self.bot.cogs["ServerCog"].staff_finder(ctx.author,"say"):
            return
        try:
            msg = await ctx.channel.get_message(ID)
        except discord.errors.HTTPException as e:
            await ctx.send(await self.translate(ctx.guild,"fun",'react-0'))
            return
        for r in reactions.split():
            try:
                e = await commands.EmojiConverter().convert(ctx,r)
                await msg.add_reaction(e)
            except:
                try:
                    await msg.add_reaction(r)
                except Exception as e:
                    await self.bot.cogs["ErrorsCog"].on_error(e,ctx)
                    continue
        await self.bot.cogs["UtilitiesCog"].suppr(ctx.message)
    
    @commands.command(name="nuke",hidden=True)
    @commands.check(is_fun_enabled)
    async def nuke(self,ctx):
        """BOOOM"""
        if not await self.bot.cogs["ServerCog"].staff_finder(ctx.author,"say"):
            return
        await ctx.send(file=await self.utilities.find_img('nuke.gif'))
    
    @commands.command(name="pikachu",hidden=True)
    @commands.check(is_fun_enabled)
    async def pikachu(self,ctx):
        """Pika-pika ?"""
        await ctx.send(file=await self.utilities.find_img(random.choice(['cookie-pikachu.gif','pika1.gif'])))
    
    @commands.command(name="pizza",hidden=True)
    @commands.check(is_fun_enabled)
    async def pizza(self,ctx):
        """Hey, do U want some pizza?"""

        await ctx.send(file=await self.utilities.find_img('pizza.gif'))
    
    @commands.command(name="lmgtfy",hidden=True)
    @commands.check(is_fun_enabled)
    async def lmgtfy(self,ctx,*,search):
        """How to use Google"""
        link = "http://lmgtfy.com/?q="+search.replace(" ","+")
        await ctx.send(link)
        await self.bot.cogs['UtilitiesCog'].suppr(ctx.message)
    
    @commands.command(name="loading",hidden=True)
    @commands.check(is_fun_enabled)
    async def loading(self,ctx):
        await ctx.send(file=await self.utilities.find_img('loading.gif'))
    
    @commands.command(name="thanos",hidden=True)
    @commands.check(is_fun_enabled)
    async def thanos(self,ctx):
        await ctx.send(random.choice(await self.translate(ctx.guild,"fun","thanos")).format(ctx.author.mention))
    
    @commands.command(name="piece",hidden=True)
    @commands.check(is_fun_enabled)
    async def piece(self,ctx):
        """Heads or tails?"""
        if random.random() < 0.04:
            await ctx.send(await self.translate(ctx.guild,"fun","piece-1"))
        else:
            await ctx.send(random.choice(await self.translate(ctx.guild,"fun","piece-0")))


    @commands.command(name="calc")
    async def calc(self,ctx,*,calcul):
        """Do some complicated math
        Use derivate() to derive functions"""
        if "ctx" in calcul and (await self.bot.cogs['AdminCog'].check_if_admin(ctx.author))==False:
            return
        try:
            s = self.calc_sth(calcul.replace("ln","log").replace("log","log10"),ctx)
        except timeout_decorator.timeout_decorator.TimeoutError:
            await ctx.send(await self.translate(ctx.guild,"fun","calc-0"))
            return
        except Exception as e:
            await ctx.send(str(await self.translate(ctx.guild,"fun","calc-5")).format(str(e).capitalize()))
            return
        if len(s)>2:
            text = str(await self.translate(ctx.guild,"fun","calc-1")).format(calcul,"`, `".join(s))
        elif len(s)==2:
            text = str(await self.translate(ctx.guild,"fun","calc-2")).format(c=calcul,l=s)
        elif len(s) == 1:
            text = str(await self.translate(ctx.guild,"fun","calc-3")).format(calcul,s[0])
        else:
            text = str(await self.translate(ctx.guild,"fun","calc-4")).format(calcul)
        await ctx.send(text)

    @timeout_decorator.timeout(10)
    def calc_sth(self,calcul,ctx):
        x = Symbol('x')
        r = re.search(r'derivate\(((?:\([^)]*\)+|[^)(])*)\)',calcul)
        if r != None:
            y = eval(r.group(1))
            c = calcul
            calcul = c.replace(r.group(0),str(y.diff()))
            if '=' not in calcul:
                return [simplify(calcul)]
        if 'x' in calcul and "ctx" not in calcul:
            if "=" in calcul:
                l = calcul.split('=')
            else:
                l = [calcul,0]
            s = solve("{l[0]} - {l[1]}".format(l=l),x)
            solution = list()
            for x in s:
                solution.append(str(x))
            return solution
        else:
            if "=" in calcul and "==" not in calcul:
                calcul = calcul.replace('=','==')
            return [eval(calcul)]
    
    async def add_vote(self,msg):
        emojiz = await self.bot.cogs["ServerCog"].find_staff(msg.guild,'vote_emojis')
        if emojiz == None or len(emojiz) == 0:
            await msg.add_reaction('👍')
            await msg.add_reaction('👎')
            return
        count = 0
        for r in emojiz.split(';'):
            if r.isnumeric():
                d_em = discord.utils.get(self.bot.emojis, id=int(r))
                if d_em != None:
                    await msg.add_reaction(d_em)
                    count +=1
            else:
                await msg.add_reaction(emojilib.emojize(r, use_aliases=True))
                count +=1
            if count==0:
                await msg.add_reaction('👍')
                await msg.add_reaction('👎')

    @commands.command(name="vote")
    @commands.cooldown(4, 30, type=commands.BucketType.guild)
    async def vote(self,ctx,number:typing.Optional[int] = 0,*,text):
        """Send a message on which anyone can vote through reactions. 
        A big thank to Adri526 for his emojis specially designed for the bot!
        
        If no number of choices is given, the emojis will be 👍 and 👎. Otherwise, it will be a series of numbers.
        The text sent by the bot is EXACTLY the one you give, without any more formatting."""
        text = text.replace('@everyone','@ everyone').replace('@here','@ here')
        if not (ctx.channel.permissions_for(ctx.guild.me).read_message_history or ctx.channel.permissions_for(ctx.guild.me).add_reaction):
            await ctx.send(await self.translate(ctx.guild,"fun","cant-react"))
            return
        if number==0:
            m = await ctx.send(text)
            try:
                await self.add_vote(m)
            except:
                await ctx.send(await self.translate(ctx.guild,"fun","no-reaction"))
                return
        else:
            #liste = ["1⃣","2⃣","3⃣","4⃣","5⃣","6⃣","7⃣","8⃣","9⃣","\U0001f51f"]
            liste = self.bot.cogs['EmojiCog'].numbEmojis
            if number>20 or number<0:
                await ctx.send(await self.translate(ctx.guild,"fun","vote-0"))
                return
            m = await ctx.send(text)
            for x in range(1,number+1):
                try:
                    await m.add_reaction(liste[x])
                except Exception as e:
                    await self.bot.cogs['ErrorsCog'].on_error(e,ctx)
        await self.bot.cogs['UtilitiesCog'].suppr(ctx.message)
        await self.utilities.print2(await self.bot.cogs['TimeCog'].date(datetime.datetime.now(),digital=True)+" Vote de {} : {}".format(ctx.author,ctx.message.content))


    async def check_suggestion(self,message):
        if message.guild==None:
            return
        try:
            channels = await self.bot.cogs['ServerCog'].find_staff(message.guild.id,'poll_channels')
            if channels==None or len(channels)==0:
                return
            if str(message.channel.id) in channels.split(';') and not message.author.bot:
                try:
                    await self.add_vote(message)
                except:
                    pass
        except Exception as e:
            await self.bot.cogs['ErrorsCog'].on_error(e,message)

def setup(bot):
    bot.add_cog(FunCog(bot))
