#!/usr/bin/env python
#coding=utf-8

current_lang = {'current':'lolcat'}

activity={"rien":"nothin",
"play":"playin",
"stream":"streamin",
"listen":"listenin",
"watch":"watching"}

admin={
    "change_game-0":"Slect *play*, *watch*, *listen* or *stream* followd by teh naym",
    "msg_2-0":"Operashun in progres '-'",
    "msg_2-1":"No affected members",
    "msg_2-2":"1 affected memberé",
    "msg_2-3":"affectd mEmber",
    "bug-0":"Bug #{} not found",
    "emergency":"An emergency situation has just been declared for the bot. This may be the case when someone tries to take control of my code.\n\
To limit the damage, I was forced to leave all the servers I was on immediately, hoping it wasn't too late.\n\
For more information on the current state of the crisis, go to my official server: https://discord.me/z_bot (check the link from the documentation if it no longer works: https://zbot.rtfd.io)"
    }

bvn={"aide":"""__**Welcome 2 teh join & leef msg modul**__

Dis modul is usd 2 configur a' automatic mesage each tiem membr enters or exits ur servr.

__** Configuration**__

`1-` To configure teh channel wer thees mesagez 're writtn, entr `!config change welcome_channel` followd by teh channl ID (rite clik -> "Copy ID" 4 computer, or keep pressin on teh channel -> "Copy ID" 4 phone, but you w'll nede to have enabld teh developer mode to get dis optn).
`2-` To configure a msg, entr `!config change <welcome|leave> <message>`. 4 dis mesage u can uz somm variabl':
 - `{user}` mentionz teh member
 - `{server}` displayz the servr nayme
 - `{owner}` displayz teh servr ownr nam
 - `{member_count}` showz the current nbr oof memberz
"""}

cases={"no-user":"Unable to find dis usr :eyes:",
    "not-found":"Dis caze was not fund :upside_down:",
    "reason-edited":"Teh ryson for case #{} has been changd!",
    "deleted":"The caze #{} has byn deletd!",
    "cases-0":"{} cases fund: ({}-{})"}

find={"user-0":"naym: {}\nID: {}",
"user-1":"Naym: {}\nID: {}\nServers: {}\nPremium ? {}",
"user-2":"Usr not findz",
"guild-0":"Servr not findz",
"guild-1":"Name: {}\nID: {}\nOwnr: {} ({})",
"chan-0":"Channel not foundz",
"chan-1":"Nayme : {}\nID: {}\nServr: {} ({})",
"help":"Dis commnd allowz 2 find a servr or a chnnel among all the servers on which'z teh bot. U can so search 4 a Discord usr's info, no mater if he sharez servr wif me!\
Teh syntax'z `!find <user|channel|guild> <ID>`"}

fun={"count-0":"Countng in progrez...",
    "count-1":"On teh last {} posts, U has postd {} msgs ({}%)",
    "count-2":"You wanna blow up Discord! {e} For obvious performance reasons, I'm gonna impose limit ov {l} msgz.",
    "count-3":"Oops, Im unable to reed dis channel ystory. Pls check mah perms...",
    "fun-list":"Her iz the list ov available fun commandz:",
    "no-fun":"Fun commands haz been disabld on dis server. 2 C their list, look at https://zbot.rtfd.io/en/v3/fun.html",
    "react-0":"Unable 2 find teh correspondin mssage. U must giv teh mesage ID in da furst argumnt, an teh emoji in da secondz :upside_down:\n Also check dat I haz permishun 2 reed msgs hystory!",
    "thanos":["{0} wus spard by Thanos","Thanos decidd 2 reduce {0} to ashes. 4 the gud ov humanity...."],
    "piece-0":["Tails!","Heads!"],
    "piece-1":"Faild, 't fell on teh edge!",
    "calc-0":"Nope, result takz too looooooong to load :rofl:",
    "calc-1":"Teh solushuns of the calculation `{}` are `{}`",
    "calc-2":"The solutions of teh calculz `{c}` R `{l[0]}` and `{l[1]}`",
    "calc-3":"The solushun to the calculation `{}` 'z `{}`",
    "calc-4":"Teh calculation `{}` haz nope solushun",
    "calc-5":"Oooops, an error appeared :upside_down: \n `{}`",
    "no-reaction":"Unable 2 add reactions. Plz check mah perms...",
    "cant-react":"I doan haz enough perms 2 send reactions!",
    "vote-0":"U can't put moar than 20 choicez, an' even lesss negativ numbr of choicesz!",
    "blame-0":"Lizt ov availabl namz 4 **{}**"
    }

infos={"text-0":"""Hello! I'm {0} !

I'm a bot that allows you to do a lot of things: moderation, mini-games, an xp system, statistics and many other super useful commands (and totally pointless ones)! 
You can start by typing `!help` in this chat to see the list of available commands, then `!config see` will let you see the configuration options (a website is in preparation). 

For helping me in the creation of the bot, my owner and I would like to thank reddemoon for his support during the various crises, Aragorn1202 for all his ideas and sentences full of good sense, Adri526 for all these beautiful logos, emojis and profile pics, and Pilotnick54 to review and correct my English!

:globe_with_meridians: Some links may be useful: 
:arrow_forward: My Discord server : http://discord.gg/N55zY88
:arrow_forward: A link to invite me to another server : <https://bot.discord.io/zbot>
:arrow_forward: The bot documentation : <https://zbot.rtfd.io/>

Have a nice day!""",
"docs":"Her'z teh link 2 the bot doc:",
"stats":"""**Baut vershun:** {} \n**Nbr ov serverz:** {} \n**Nbr ov visible memberz:** {} \n**Python vershun :** {} \n**Vershun ov teh `discord.py` lyb:** {} \n**Loadin on teh RAM:** {} GB \n**Loadin on the CPU:** {} % \n**API latency timz:** {} ms"""}

infos_2={"membercount-0":"Total nmber of membrz",
"membercount-1":"Numbr ov botz",
"membercount-2":"Numbr ov good people",
"membercount-3":"Numbr ov good online people"}

keywords={"depuis":"since",
          "nom":"nayme",
          "online":"on-line",
          "idle":"idle",
          "dnd":"don't disturb me",
          "offline":"oofline",
          "oui":"yup",
          "non":"nop",
          "none":"none",
          "low":"low",
          "medium":"medium",
          "high":"high",
          "extreme":"Xtrem",
          "aucune":"none",
          "membres":"memberz"
          }

mc={"contact-mail":"If U notice an error in da info providd, plz contact me personally, or report teh error directly [on the nice website](https://fr-minecraft.net).",
    "serv-title":"Servr info {}",
    "serv-0":"Numbr of playerz",
    "serv-1":"List ov teh first 20 connected playerz",
    "serv-2":"List of nice online people",
    "serv-3":"Latency",
    "serv-error":"Oops, an unknown error occurrd. Plz try again latr :smirk_cat:",
    "no-api":"Error: Unable 2 connect to API",
    "no-ping":"Error: Unable 2 ping dis servr",
    "success-add":"A nice message wif servr details {} has been addd to teh channel {} !",
    "cant-embed":"Cannot send embd. Plz make sure the \"Embed linkz\" perm is enabld.",
    "entity-help":"Dis cmd allows U to obtain info 'bout any Minecraft entity. U can giv itz full or partial naym, in French or English, or even itz identifir. Just enter `!mc entity <name>`",
    "no-entity":"Unable 2 find this entity",
    "no-block":"Unable 2 find dis block",
    "no-item":"Unable to find dis item",
    "block-help":"This command allows U to obtain information on any Minecraft block. U can give itz full or partial name, in French r English, or evn itz identifier. Just enter `!mc block <name>`",
    "item-help":"Dis command allowz you to obtain info 'bout any Minecraft item. You can give its full or partial name, in French r English, r even its identifier. Just entr `!mc item <name>`",
    "mojang_desc":{'minecraft.net':'Offishul Block Site',
      'session.minecraft.net':'Many-People-Together sessions (obsolete)',
      'account.mojang.com':"Mojang 'ccount managmnt site",
      'authserver.mojang.com': "Authentication servr",
      'sessionserver.mojang.com':'Many-People-Together sessions',
      'api.mojang.com': "API service givn bay Mojang",
      'textures.minecraft.net':'Texture servr (nice skin & capes)',
      'mojang.com':'Official Ex Website'},
    "lol":"""mdr""",
    "dimensions":"Width: {d[0]}\nLenght: {d[1]}\nHeight: {d[2]}",
    "item-fields":('ID',"Size ov stack",'Creativ mod tab','Damge points',"Durability points","Tool able 2 destroy it","Mobs able to drop dis item","Added in da vershun"),
    "entity-fields":('ID','Type','Life Points','Attack Points','Nice green XP Releasd to Death','Preferrd Biomz','Added in da vershun')
      }

modo={"slowmode-0":"Teh very-cold-mode is now disabld in this nize place.",
    "slowmode-1":"Impossible to set a frequency higher than two minutes",
    "slowmode-2":"The {} channl iz naw in very-cold-mode. Wait {} secondz be4 sending a mesage.",
    "slowmode-3":"Nope, dis valu iz invalid",
    "cant-slowmode":"Ooops, I dont haz permishun 2 `Manage dis channel` :rolling_eyes:",
    "clear-0":"{} messagz deletd!",
    "cant-kick":"Perm 'Kick memberz' needed :confused:",
    "kick":"Membr {} haz been kick from dis servr. Just 'cause **{}**",
    "staff-kick":"Yolo NOPE ! U can't kick a-other nice staff mmber!",
    "kick-noreason":"U have just been kicked from the servr {} :confused:",
    "kick-reason":"U haz just been kicked from the servr {} :confused:\nReason : {}",
    "kick-1":"Seemz that this membr iz tooooo high 4 me to kick him out :thinking:",
    "error":"Oooooops, unknown error :scream: Just waiiiit, 'r contact sport",
    "warn-mp":"U haz receivd 'warnung from *{}* servr: \n{}",
    "staff-warn":"Hey NOPE ! U cant warn 'nother staff nice member!",
    "warn-1":"Nice, membr `{}` haz beeen warnd 4 reezon `{}`",
    "warn-bot":"Nope, cant warn another cool bot ^^",
    "staff-mute":"U cant prevent another cool staff member frm speek'ng ",
    "mute-1":"Teh mmber {} haz been silencd for the reezon `{}`!",
    "no-mute":"Oooops, seemz dat teh nice `muted` role doznt exist :rofl: Creat'it nd assign perms yourself",
    "cant-mute":"Ooops, 't seemz dat I dont haz enough perms for that.... Plz give me perm `Manage roles` :eyes:",
    "mute-high":"Ooops, 't seems dat `muted` rol iz tooo high 4 me to give it... Plz fiX dis problem by plac'ng my role higher than this nice `muted` role.",
    "already-mute":"Dis membr iz 'lready mute!",
    "already-unmute":"This mber iznt muted!",
    "unmute-1":"Teh mmber {} canow speek 'gain",
    "cant-ban":"Perm 'Ban members' needd :confused:",
    "staff-ban":"NOPE, U can't ban another cool staff guy!",
    "ban-noreason":"U haz just been bannd fr0m the servr {} :confused:",
    "ban-reason":"You haz just been bannd from teh server {} :confused:\nReason : {}",
    "ban":"Mber {} has been banned fr0m dis cool servr. Just 'cause this : **{}**",
    "ban-1":"Maaaw... 'seems dat dis member iz too high 4 me to ban him :thinking:",
    "ban-list-title":"List of bannd membrs ov this nice place '{}'",
    "no-bans":"No mmber seems to be bannd from here",
    "unban":"Mmber {} iz no langer bannd fr0m this servr",
    "cant-find-user":"Ooops, no way 2 find dis usr **{}**",
    "ban-user-here":"Dis nice guy iz not part of teh bannd members list :upside_down:",
    "caps-lock":"Heyz {}, beware of too big letters!",
    "emoji-valid":"Teh emojy {} haz been modified 2 allow only teh roles `{}`",
    "cant-emoji":"Oooops, I'm missng teh perm `Manage emojis` <:owo:499661437589913621>",
    "wrong-guild":"Oooops, it seemz dis emoji dont belang dis server <:owo:499661437589913621>",
    "emoji-renamed":"The emoji {} has been renamed!"
    }

perms={"perms-0":"Membr/role {} not findz",
        "perms-1":"**'{}' permissung:**\n\n"
       }


rss={"yt-help":"To search for a youtube channel, you must enter the channel ID. You will find it at the end of the string url, it can be either the name, or a string of random characters. \
*Tip: some channels are already filled in my code. Sometimes you can just put `neil3000` or `Oxisius`* :wink:",
"tw-help":"To search for a twitter channel, you must enter the identifier of that channel. You will find it at the end of the string url, it usually corresponds to the user's name. \
For example, for %https://twitter.com/Mc_AsiliS*, you must enter `Mc_AsiliS`.",
"web-help":"To search for an rss feed from any website, simply enter the rss/atom feed url as a parameter. If the feed is valid, I will send you the last article posted on this site. \
*Tip: some rss feeds are already filled in my code. Sometimes you can just put `fr-minecraft` or `minecraft.net`* :wink:",
"web-invalid":"Oops, this url address is invalid :confused:",
"nothing":"I found nothing on this search :confused:",
"success-add":"The rss feed of type '{}' with link <{}> has been properly added in the channel {} !",
"invalid-link":"Oops, this url address is invalid or incomplete :confused:",
"fail-add":"An error occurred while processing your response. Please try again later, or contact bot support (enter the command `botinfo` for server link)",
"flow-limit":"For performance reasons, you cannot track more than {} rss feeds per server.",
"yt-form-last":"""{logo}  | Here is the last video of {author}:
{title}
Published on {date}
Link : {url}
""",
"tw-form-last":"""{logo}  |  Here is the last tweet of {author}:
Written on {date}

{title}

Link : {url}
""",
"web-form-last":"""{logo}  |  Here is the last post of {author}:
**{title}**
*Written on {date}*
Link : {link}""",
"yt-default-flow":"{logo}  | New video of {author} : **{title}**\nPublished on {date}\nLink : {link}\n{mentions}",
"tw-default-flow":"{logo}  | New tweet of {author} ! ({date})\n\n{title}\n\nLink : {link}\n\n{mentions}",
"web-default-flow":"{logo}  | New post on {author} ({date}) :\n    {title}\n\n{link}\n\n{mentions}",
"list":"*Type the number of the flow to modify*\n\n**Link - Type - Channel - Mentions**\n",
'tw':'Twitter',
'yt':'YouTube',
'web':'Web',
'mc':'Minecraft',
'choose-mentions-1':"Please choose the flow to modify",
"too-long":"You waited too long, sorry :hourglass:",
"no-roles":"No role has been configured yet.",
"roles-list":"Here is the list of roles already indicated: {}",
"choose-roles":"What roles will be mentioned?",
"not-a-role":"The role `{}` is not found. Try again:",
"roles-0":"This feed has been modified to mention the roles {}",
"roles-1":"This feed has been modified to not mention any role",
"no-feed":"Oops, you don't have any rss feeds to manage!"
}

server={"config-help": "Dis cmd is mainly usd 2 configur ur srver. By doin `!config see [option]` u will get \
overview ov teh currnt configuraishun, and supr cool servr masters can enter `!config change <option> role1, role2, role3...` \
to modify configuraishun, or `!config del <option>` 2 reset teh option (`!config change <option>` works same).",
        "change-0": "Dis option doz not exist :confused:",
        "change-1": "Oops, an internal error occurrd...\nBut doan worry, we'r on teh place: http://asset-5.soupcdn.com/asset/3247/3576_5092_600.jpeg",
        "change-2": "The '{}' opshun value haz been deleted",
        "change-3": "Teh role '{}' waz not findz :innocent: (Check upper caze and special characters)",
        "change-4": "Teh '{}' opshun expects a boolean (True/False) parameter in value :innocent:",
        "change-5": "Teh channel '{}' waz not found :confused: (Enter the exact mention, name 'r identifier of teh channel(s)",
        "change-6": "Teh '{}' option expects a numbr in parameter :innocent:",
        "change-7": "Dis language is not available. Here is the list of currently supported languages: {}",
        "change-8": "Ups, dis lvl doz nope exist. Heer iz da list ov currrently availaible levelz: {}",
        "change-9": "Ups, da emoji `{}` wasnt findz",
        "change-role": "The '{}' option haz been modified with teh following rolz: {}",
        "change-bool": "The '{}' option haz been modified wif the value *{}*",
        "change-textchan": "The '{}' opshun has been modifid wif teh channelz {}",
        "change-text": "Teh opshun '{}' haz been replacd by the followin txt: \n```\n{}\n```",
        "change-prefix":":cat: The prefiX has been nicely replaced by `{}`",
        "change-lang": "Teh bot lang is naw in `{}`",
        "change-raid":"Teh anti-rayd security lvl iz naw set 2 **{}** ({})",
        "change-emojis":"Teh emojiz 4 the opshun '{}' are naw {}",
        "new_server": "Ur server haz just been written for da furst time in r database. Congratulashuns :tada:",
        "see-0":"Enter `!config help` 4 more details",
        "see-1":"{} server configurashun",
        "change-prefix-1":"Dis prefix iz too long 2 be used!",
        "wrong-prefix":"Oooops, it seemz dis prefix is no valid :thinking: If teh problem persists, plz choose a' other one",
        "opt_title":"Option '{}' of srver {}"
    }

server_desc={"clear": "List of roles that can use the 'clear' command: {}",
             "slowmode": "List of roles that can use 'slowmode' and 'freeze' commands: {}",
             "mute": "List of roles that can use the 'mute' command: {}",
             "kick": "List of roles that can use the 'kick' command: {}",
             "ban": "List of roles that can use the command 'ban': {}",
             "warn": "List of roles that can use commands 'warn' and 'cases': {}",
             "say": "List of roles that can use the command 'say' : {}",
             "gived_roles": "List of roles automatically given to new members: {}",
             "save_roles": "Should roles be saved when a member leaves, in case he returns? {}",
             "enable_xp": "Should the xp system be enabled? {}",
             "anti_caps_lock": "Should the bot send a message when a member sends too many capital letters? {}",
             "enable_fun": "Are the commands listed in the `!fun` command enabled? {}",
             "hunter": "List of all chat rooms in which the game *Hunter* is active: {}",
             "welcome_channel": "List of channels where to send welcome/leave messages: {}",
             "bot_news": "List of channels where to send bot news: {}",
             "poll_channels": "List of channels where :thumbsup: and :thumbsdown: reactions will be automatically added to each message : {}",
             "welcome": "Message sent when a member arrives: {}",
             "leave": "Message sent when a member leaves: {}",
             "language": "Current bot language for this server: **{}**",
             "prefix":"Current bot prefix: {}",
             "membercounter":"Channel displaying number of members in its name: {}",
             "anti_raid":"Level of anti-raid protection: {} \n*([Documentation](https://zbot.rtfd.io/en/latest/moderator.html#anti-raid))*"}


stats_infos={"not-found":"Unable 2 find {}",
            "member-0":"Little name",
            "member-1":"Born at",
            "member-2":"New since",
            "member-3":"Arrival position",
            "member-4":"Status",
            "member-5":"Activity",
            "member-6":"Cat Master",
            "role-0":"ID",
            "role-1":"Colorr",
            "role-2":"Mentionable",
            "role-3":"Nmber ov members",
            "role-4":"Lonely role",
            "role-5":"Hierarchical posishun",
             "role-6":"Lonely user",
            "user-0":"On dis servr?",
            "emoji-0":"Animated",
            "emoji-1":"Managd by Twitch",
            "emoji-2":"String (4 robots)",
            "textchan-0":"Category",
            "textchan-1":"Descripshun",
            "textchan-2":"NSFW",
            "textchan-3":"Numbr ov webhooks",
            "textchan-4":":warning: Missing perms !",
            "textchan-5":"Channel",
            "voicechan-0":"Singing channel",
            "guild-0":"Guild",
            "guild-1":"Auwner",
            "guild-2":"Region",
            "guild-3":"Text : {} | Vocal : {} ({} categoreez)",
            "guild-4":"Green people",
            "guild-5":"Numbr ov emojis",
            "guild-6":"Numbr ov chats",
            "guild-7":"{} including {} nice robots ({} connected)",
            "guild-8":"2F authentificashun",
            "guild-9":"Security lvl",
            "guild-10":"Time be4 being AFK",
            "guild-11.1":"20 first roles (total {})",
            "guild-11.2":"Rol list (total {})",
            "inv-0":"URL link",
            "inv-1":"Inviter",
            "inv-2":"Uzz",
            "inv-3":"Time left be4 explosion",
            "inv-4":"Invite",
            "inv-5":"If info seems missing, it is sadly cuz Discord didnt send them",
            "categ-0":"Category",
            "categ-1":"Posishun",
            "categ-2":"Text : {} | Vocal : {}",
             }
