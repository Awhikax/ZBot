import discord
from discord.ext import commands

class PermsCog:
    """Cog with a single command, allowing you to see the permissions of a member or a role in a channel."""

    def __init__(self,bot):
        self.bot = bot
        self.file = "perms"
        try:
            self.translate = self.bot.cogs["LangCog"].tr
        except:
            pass

    async def on_ready(self):
        self.translate = self.bot.cogs["LangCog"].tr

    @commands.command(name='perms', aliases=['perms_for', 'permissions'])
    @commands.guild_only()
    async def check_permissions(self, ctx, *, member=None):
        """Permissions assigned to a member/role (the user by default)
        The channel used to view permissions is the channel in which the command is entered."""
        if not member:
            memb = ctx.author
            perms = memb.guild_permissions
            col = memb.color
            avatar = memb.avatar_url_as(format='png',size=256)
            name = str(memb)
            del memb
        else:
            try:
                memb = await commands.MemberConverter().convert(ctx,member)
                perms = memb.guild_permissions
                col = memb.color
                avatar = memb.avatar_url_as(format='png',size=256)
                name = str(memb)
                del memb
            except commands.errors.BadArgument:
                try:
                    if member == "everyone":
                        member = "@everyone"
                    role = await commands.RoleConverter().convert(ctx,member)
                    perms = role.permissions
                    col = role.color
                    avatar = ctx.guild.icon_url_as(format='png',size=256)
                    name = str(role)
                    del role
                except commands.errors.BadArgument:
                    msg = await self.translate(ctx.guild.id,"perms","perms-0")
                    await ctx.send(msg.format(member))
                    return
        permsl = list()
        # Here we check if the value of each permission is True.
        for perm, value in perms:
            if value:
                permsl.append(self.bot.cogs['EmojiCog'].customEmojis['green_check']+perm)
            else:
                permsl.append(self.bot.cogs['EmojiCog'].customEmojis['red_cross']+perm)
        if ctx.channel.permissions_for(ctx.guild.me).embed_links:
            # And to make it look nice, we wrap it in an Embed.
            embed = discord.Embed(colour=col)
            embed.set_author(icon_url=avatar, name=name)
            # \uFEFF is a Zero-Width Space, which basically allows us to have an empty field name.
            sep = int(len(permsl)/2)
            if len(permsl)%2 == 1:
                sep+=1
            embed.add_field(name='\uFEFF', value="\n".join(permsl[:sep]))
            embed.add_field(name='\uFEFF', value="\n".join(permsl[sep:]))
            embed = await self.bot.cogs['UtilitiesCog'].create_footer(embed,ctx.author)
            await ctx.send(embed=embed)
            # Thanks to Gio for the Command.
        else:
            try:
                await ctx.send(str(await self.translate(ctx.guild.id,"perms","perms-1")).format(name.replace('@','')) + "\n".join(permsl))
            except:
                pass


def setup(bot):
    bot.add_cog(PermsCog(bot))