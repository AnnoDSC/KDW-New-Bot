import sys
sys.dont_write_bytecode = True

import discord, config
from discord.ext import commands
from discord import app_commands
from discord.utils import format_dt
from src.Utils.database import DatabaseUtils as dbb
from src.interface.modal.Warn_Modal import Add_Warn
from src.interface.dropdown.Del_Warns_dropdown import Del_Warns_view


class ProfielViewer(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.warn = dbb("db.db")
        self.add_warn = app_commands.ContextMenu(
            name="Add Warn",
            callback=self._c_user_add_warn
        )
        self.del_warn = app_commands.ContextMenu(
            name="Del Warn",
            callback=self._c_user_del_warn
        )
        self.show = app_commands.ContextMenu(
            name="Show",
            callback=self._c_user_show
        )
        self.bot.tree.add_command(self.add_warn)
        self.bot.tree.add_command(self.del_warn)
        self.bot.tree.add_command(self.show)

    user = app_commands.Group(name="user", description="Sehe alle Infomationen ueber den Nutzer / Fuege oder loeche warnungen")

    @user.command(name="show", description="Sehe alle Infomationen ueber den Nutzer")
    @app_commands.checks.has_role(957420338524860426)
    async def _user_show(self, ctx: discord.Interaction, user: discord.Member):
        check = self.warn.get_warn(user.id)
        roles = []
        warns = ""
        count = 0
        for role in user.roles:
            if not role.is_default():
                roles.append(role.mention)
        try:
            for warn in check:
                count += 1
                warns += f"{count}. {warn[0]}\n"
        except:
            warns = "None"

        roles_mention = ',\n'.join(roles)
        mm = await ctx.response.send_message(embed=discord.Embed(
            title=f"Profil von {user.name}",
            colour=config.BOT_EMBED_COLOUR
        ).add_field(name=":bust_in_silhouette: Name", value=f"{user.name} / {user.mention}"
        ).add_field(name=":id: ID", value=user.id
        ).add_field(name=":calendar: Erstellt am", value=format_dt(user.created_at)
        ).add_field(name="\u200b", value="", inline=False
        ).add_field(name=":medal: Rollen", value=roles_mention
        ).add_field(name="❌ Verwarnungen", value=warns
        ).set_thumbnail(url=user.avatar.url), ephemeral=True)
    
    @_user_show.error
    async def _user_show_error(self, ctx: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingRole):
            await ctx.response.send_message("Du hast keine Bereichtigung !!!", ephemeral=True)

    @user.command(name="add_warn", description="Fuege einen warn zu einem nuzter hinzu")
    @app_commands.checks.has_role(957420338524860426)
    async def _user_add_warn(self, ctx: discord.Interaction, user: discord.Member, grund: str):
        check = self.warn.add_warn(user.id, grund)
        if check:
            await ctx.response.send_message(embed=discord.Embed(
                title="Warn System",
                description=f"Der Nutzer {user.mention} hat einen Warn bekommen mit dem Grund {grund}",
                colour=config.BOT_EMBED_COLOUR
            ), ephemeral=True)
        else:
            await ctx.response.send_message(embed=discord.Embed(
                title="Error System",
                description="Ein Fehler ist aufgetreten bitte wende dich an den Admin",
                colour=config.BOT_EMBED_COLOUR
            ), ephemeral=True)
    
    @user.command(name="del_warn", description="Loeche einen warn von einem Nuzter ")
    @app_commands.checks.has_role(957420338524860426)
    async def _user_del_warn(self, ctx: discord.Interaction, user: discord.Member):
        if ctx.user.guild_permissions.administrator:
            warn_list = self.warn.get_warn(user.id)
            if warn_list:
                await ctx.response.send_message(embed=discord.Embed(
                    title="Loeche einen Warn",
                    description="Benutze das auswahlfeld um einen warn zu loechen",
                    colour=config.BOT_EMBED_COLOUR
                ), view=Del_Warns_view(user), ephemeral=True)
            else:
                await ctx.response.send_message("Dieser User hat keine Warns fuege ihm welche hinzu", ephemeral=True)
        else:
            await ctx.response.send_message("Du hast keine Bereichtigung !!!", ephemeral=True)
        

    @_user_add_warn.error
    async def _user_add_warn_error(self, ctx: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingRole):
            await ctx.response.send_message("Du hast keine Bereichtigung !!!", ephemeral=True)

    async def _c_user_add_warn(self, ctx: discord.Interaction, user: discord.Member):
        if ctx.user.guild_permissions.administrator:
            await ctx.response.send_modal(Add_Warn(user))
        else:
            await ctx.response.send_message("Du hast keine Bereichtigung !!!", ephemeral=True)

    async def _c_user_del_warn(self, ctx: discord.Interaction, user: discord.Member):
        if ctx.user.guild_permissions.administrator:
            warn_list = self.warn.get_warn(user.id)
            if warn_list:
                await ctx.response.send_message(embed=discord.Embed(
                    title="Loeche einen Warn",
                    description="Benutze das auswahlfeld um einen warn zu loechen",
                    colour=config.BOT_EMBED_COLOUR
                ), view=Del_Warns_view(user), ephemeral=True)
            else:
                await ctx.response.send_message("Dieser User hat keine Warns fuege ihm welche hinzu", ephemeral=True)
        else:
            await ctx.response.send_message("Du hast keine Bereichtigung !!!", ephemeral=True)
    
    async def _c_user_show(self, ctx: discord.Interaction, user: discord.Member):
        check = self.warn.get_warn(user.id)
        roles = []
        warns = ""
        count = 0
        for role in user.roles:
            if not role.is_default():
                roles.append(role.mention)
        try:
            for warn in check:
                count += 1
                warns += f"{count}. {warn[0]}\n"
        except:
            warns = "None"

        roles_mention = ',\n'.join(roles)
        mm = await ctx.response.send_message(embed=discord.Embed(
            title=f"Profil von {user.name}",
            colour=config.BOT_EMBED_COLOUR
        ).add_field(name=":bust_in_silhouette: Name", value=f"{user.name} / {user.mention}"
        ).add_field(name=":id: ID", value=user.id
        ).add_field(name=":calendar: Erstellt am", value=format_dt(user.created_at)
        ).add_field(name="\u200b", value="", inline=False
        ).add_field(name=":medal: Rollen", value=roles_mention
        ).add_field(name="❌ Verwarnungen", value=warns
        ).set_thumbnail(url=user.avatar.url), ephemeral=True)



async def setup(bot: commands.Bot):
    await bot.add_cog(ProfielViewer(bot))