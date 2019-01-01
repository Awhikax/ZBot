#!/usr/bin/env python
#coding=utf-8

from importlib import reload as m_reload
from fcts.lang import fr, en, lolcat
import discord
m_reload(fr)
m_reload(en)
m_reload(lolcat)


class LangCog:

    def __init__(self,bot):
        m_reload(fr)
        m_reload(en)
        self.bot = bot
        self.file = "language"
        self.serv_opts = dict()
        self.languages = ['fr','en','lolcat']
        try:
            self.salon = bot.get_channel(491370492561981474)
        except:
            pass
            
    async def on_ready(self):
        self.salon = self.bot.get_channel(491370492561981474)

    async def tr(self,serverID,moduleID,messageID):
        """Renvoie le texte en fonction de la langue"""
        try:
            return eval("en."+moduleID+"[\""+messageID+"\"]")
        except:
            try:
                return eval("fr."+moduleID+"[\""+messageID+"\"]")
            except:
                await self.msg_not_found(moduleID,messageID,"fr")
                return ""

    async def msg_not_found(self,moduleID,messageID,lang):
        try:
            await self.salon.send("Le message {}.{} n'a pas été trouvé dans la base de donnée! (langue {})".format(moduleID,messageID,lang))
        except:
            pass


    async def check_tr(self,channel,lang):
        liste = list()
        if lang not in self.languages:
            await channel.send("La langue `{}` n'est pas disponible".format(lang))
            return
        count = 0
        for dic in fr.__dict__:
            if not dic.startswith("__"):
                for i in eval("fr."+dic).keys():
                    try:
                        eval(lang+"."+str(dic)+"[\""+str(i)+"\"]")
                    except KeyError:
                        liste.append("module "+dic+" - "+i)
                        count += 1
                    except AttributeError:
                        await channel.send("Le module {} n'existe pas en `{}`".format(str(dic),lang))
                        count += len(eval("fr."+dic).keys())
                        break
        if count==0:
            await channel.send("Tout les messages ont correctement été traduits en `{}` !".format(lang))
        else:
            if len(liste)>0:
                await channel.send("{} messages non traduits en `{}` :\n- {}".format(count,lang,"\n- ".join(liste)))
            else:
                await channel.send(">> {} messages non traduits en `{}`".format(count,lang))


def setup(bot):
    bot.add_cog(LangCog(bot))
