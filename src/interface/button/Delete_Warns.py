from typing import Optional
import discord, config
from src.interface.dropdown.Del_Warns_dropdown import Del_Warns_view

class Del_Warns(discord.ui.View):
    def __init__(self, user: discord.Member):
        super().__init__(
            timeout=None,
        )
        self.user = user
        self.value = None
    
    @discord.ui.button(label="del warn", style=discord.ButtonStyle.red, custom_id="Warns_Del")
    async def _del_warn(self, ctx: discord.Interaction, button: discord.Button):
        if ctx.user.guild_permissions.administrator:
            await ctx.response.send_message(embed=discord.Embed(
                title="Loeche einen Warn",
                description="Benutze das auswahlfeld um einen warn zu loechen",
                colour=config.BOT_EMBED_COLOUR
            ), view=Del_Warns_view(self.user), ephemeral=True)
        else:
            await ctx.response.send_message("Du hast keine rechte xD")