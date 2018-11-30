===========
Information
===========

ZBot also allows you to retrieve information about the virtual world surrounding you. There you will find a single command that summarizes all the information about a channel/member/role/server/invitation/emoji, as well as a few other commands allowing you to study further.

-----
About
-----

**Syntax:** :code:`about` or :code:`botinfo`

This command sends a short presentation text of the bot, so that you know it a little better. It will also give you some links that may be useful to you (like the one to invite the bot, or to access its Discord server).

.. note:: For this command, ZBot doesn't need any specific permission! Good news, isn't it?

----
Ping
----

**Syntax:** :code:`ping [ip adress]`

The ping command allows you to get the bot latency. It's useful if you want to check why your command takes too long to be read. The number corresponds with the delay between the moment when your message reaches Discord and the moment when the bot's response is received by the API.

-------
Welcome
-------

**Syntax:** :code:`welcome` or :code:`bvn`

This command helps you to define a message sent automatically by ZBot when a member joins or leaves your server (see the `sconfig <sconfig.html>`_ command). You will find how to select the channel, as well as the variables that can be used in the messages.

------
Invite
------

**Syntax:** :code:`invite [channel]`

This command allows you to get an invitation belonging to the server, as well as some primary information about it. If you specify a channel, the invite will point to it. If no invitation is found, the bot will try to create one immediately for you. 

.. note:: When searching, ZBot favors invitations for unlimited use/duration, as well as the chat used (if no channel is specified)

.. warning:: For this command to work, the bot needs "Manage server" (get the invitation) and "Create instant invite" (create an invitation if needed) permission.

-----------
Membercount
-----------

**Syntax:** :code:`membercount`

With this command, you can get the number of members on your server, but also the number of bots, of humans, people connected, and probably other numbers that will be added later. This is a small basic command without much functionality, but it allows you to quickly keep up with these statistics. 

.. note:: Good news! The bot does not need any specific permissions for this command! Just keep in mind that the rendering is much prettier with "Embed Links" permission enabled.

----
Info
----

**Syntax:** :code:`info [type] <object>`

This command is probably the most powerful in the information module. It allows you to find information on any item on your server: members, roles, chat rooms, voice rooms, categories, emojis, invitations, as well as the server itself. Some information is even available about users who are not on your server! 

You can enter the name, the mention, or the `identifier <https://support.discordapp.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID->`_ of the object to be searched, and if the type of object (member, user, role...) is not specified, the bot will search itself to identify it. Note however that you are obliged to inform the type if your search includes spaces. 

.. note:: Some fields may not appear under certain conditions. No need to worry, it's just that Discord didn't send the requested information to the bot. And there's nothing we can do about it ¯\\_(ツ)_/¯

.. warning:: The necessary permissions for the bot depend on the desired result: for example "Manage webhook" is required to get the list of webhooks of a channel. 

----
Find 
----

**Syntax:** :code:`find (channel|guild|user) <ID>`

This command is a very light version of the `info <#info>`_ command. It allows the bot to obtain the primary information concerning any user, server, or salon, only from its `ID <https://support.discordapp.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID->`_ . Here is a list of the displayed parameters: 

* guild: name, ID, server owner
* channel: server name, ID, name and ID
* user: name, ID, common servers with bot

.. note:: No permission is required for this command, except "Send messages". Moreover, it is impossible to prevent your server from being included in this command; if this feature is enough requested it will be added later.

-----------
Permissions
-----------

**Syntax:** :code:`perms [user|role]` or :code:`perms_for [user|role]` or :code:`permissions [user|role]`

This small command allows you to see the list of permissions assigned to a member/role in a particular room. The channel is automatically the one where the command is entered. To inform a member or a role, it is only necessary to enter his exact name, his `ID <https://support.discordapp.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID->`_ , or to mention it. If no name is given the targeted member will be the one who enters the order.

.. warning:: The only permission needed to grant the bot is "Embed links".