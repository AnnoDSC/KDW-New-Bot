import sys
sys.dont_write_bytecode = True

import discord, config
from discord.ext import commands
from discord import app_commands
from discord.utils import format_dt
from src.Utils.database import DatabaseUtils as dbb
from src.interface.modal.Warn_Modal import Add_Warn
from src.interface.button.Delete_Warns import Del_Warns

class ProfielViewer(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.warn = dbb("db.db")
        self.add_warn = app_commands.ContextMenu(
            name="Add Warn",
            callback=self._c_user_add_warn
        )
        self.bot.tree.add_command(self.add_warn)

    user = app_commands.Group(name="user", description="Sehe alle Infomationen ueber den Nutzer / Fuege oder loeche warnungen")

    @user.command(name="show", description="Sehe alle Infomationen ueber den Nutzer")
    @app_commands.checks.has_role(957420338524860426)
    async def _user_show(self, ctx: discord.Interaction, user: discord.Member):
        check = self.warn.get_warn(user.id)
        if check:
            roles = []
            warns = ""
            count = 0
            for role in user.roles:
                if not role.is_default():
                    roles.append(role.mention)
            for warn in check:
                count += 1
                warns += f"{count}. {warn[0]}\n"

            roles_mention = ',\n'.join(roles)
            mm = await ctx.response.send_message(embed=discord.Embed(
                title=f"Profil von {user.name}",
                colour=config.BOT_EMBED_COLOUR
            ).add_field(name=":bust_in_silhouette: Name", value=user.name
            ).add_field(name=":id: ID", value=user.id
            ).add_field(name=":calendar: Erstellt am", value=format_dt(user.created_at)
            ).add_field(name="\u200b", value="", inline=False
            ).add_field(name=":medal: Rollen", value=roles_mention
            ).add_field(name="❌ Verwarnungen", value=warns
            ).set_thumbnail(url=user.avatar.url), view=Del_Warns(user))
        else:
            await ctx.response.send_message(embed=discord.Embed(
                title="Error System",
                description="Ein Fehler ist aufgetreten bitte wende dich an den Admin",
                colour=config.BOT_EMBED_COLOUR
            ))
    
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
            ))
        else:
            await ctx.response.send_message(embed=discord.Embed(
                title="Error System",
                description="Ein Fehler ist aufgetreten bitte wende dich an den Admin",
                colour=config.BOT_EMBED_COLOUR
            ))
        

    @_user_add_warn.error
    async def _user_add_warn_error(self, ctx: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingRole):
            await ctx.response.send_message("Du hast keine Bereichtigung !!!", ephemeral=True)

    async def _c_user_add_warn(self, ctx: discord.Interaction, user: discord.Member):
        await ctx.response.send_modal(Add_Warn(user))



async def setup(bot: commands.Bot):
    await bot.add_cog(ProfielViewer(bot))