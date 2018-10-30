===
Rss
===

More and more bots offer the feature to follow news feeds, sometimes `rss atom feeds <https://en.wikipedia.org/wiki/RSS>`_,but most often Twitter or YouTube profiles. ZBot allows you to track any rss/atom feed, as well as any Twitter/YouTube channel. For Reddit feeds, you can search for the url of the rss feed, but a command will be created to make your life easier!

With this bot you have two possibilities to follow a feed: manually request the last post, or configure an automatic follow-up in a text channel. In the case of automatic tracking, ZBot will scan all feeds every ten minutes to check for new posts, sending them in if there are any. Just be careful: this automatic tracking costs a lot of resources to the bot, so you are limited to a certain number of automatic feeds (same for rss, twitter, youtube or minecraft) !


-----------------
See the last post
-----------------

**Syntax:** :code:`rss <youtube|twitter|web> <name|link>`

This command allows you to see the last post of a youtube channel, a user on Twitter, or an rss feed. You can enter :code:`rss <type> help` to get a more complex guide to this command.

To go faster, aliases such as 'yt' or 'tw' are available! YouTube channel names or frequently used web links are already listed in the bot database. Remember to check it out!

.. note:: No specific permission is required for this command. Remember to allow the use of external emojis to get a prettier look.


-------------
Follow a feed
-------------

**Syntax:** :code:`rss add <link>`

If you want to automatically track an rss feed, this command should be used. You can only track a maximum feeds, which will be reloaded every 10 minutes. Note that Minecraft server tracing also counts as an rss feed, and therefore will cost you a place.

For Twitter and YouTube channels, simply give the link of the channel, so that the bot automatically detects the type and name of the channel. If no type is recognized, the 'web' type will be selected.

.. note:: To post a message, the bot does not need any specific permission. But if it is a Minecraft server flow (see the `corresponding section <minecraft.html>`_), don't forget the "`Read message history <perms.html#read-message-history>`_" permission!


--------------
See every feed
--------------

**Syntax:** :code:`rss list`

If you want to keep an eye on the number of rss/Minecraft feeds registered on your server, this is the command to use. The bot will search in the depths of its incomprehensible files to bring back the list of all the flows, and summarize them for you in a nice embed.

.. warning:: The bot needs "`Embed Links <perms.html#embed-links>`_" permission!