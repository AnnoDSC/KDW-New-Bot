import sys
sys.dont_write_bytecode = True

import discord, config
from discord.ext import commands
from discord import app_commands
from src.interface.dropdown.Hilfemenu_dropdown import Spielsuche_view

class HilfeMenu(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name="set_hilfemenu", description="Setze das Hilfemenu")
    @app_commands.checks.has_permissions(administrator=True)
    async def _set_hilfemenu(self, ctx: discord.Interaction, channel: discord.TextChannel):
        await channel.send(embed=discord.Embed(
            colour=config.BOT_EMBED_COLOUR,
        ).add_field(name="Reaktionsrollen", value="Im Textkanal <#822089238962634822> kannst du auf die angegebenen Nachrichten reagieren, zum Beispiel mit der Rolle FSK 🔞 oder Video-Chat 📸 Schaltest du die dementsprechenden Kanäle frei!", inline=False
        ).add_field(name="\u200b", value="\u200b", inline=False
        ).add_field(name="Du suchst nach Hilfe oder willst eine Beschwerde einreichen? ⚠️", value="Wähle in dem Menü: ´´´Ticket/Ansprechpartner´´´ aus"
        ).add_field(name="\u200b", value="\u200b", inline=False
        ).add_field(name="Du Möchtest dich bei uns Bewerben? ✉️", value="Wenn du dich bei uns bewerben möchtest benötigen wir eine Bewerbung von dir und ein Mindestalter von 16 Jahren, um deine Bewerbung einzureichen wähle im Menü ´´´Ticket/Ansprechpartner´´´ aus und erstelle ein Ticket mit der Auswahl ´´´Sonstiges´´´", inline=False
        ).add_field(name="\u200b", value="\u200b", inline=False
        ).add_field(name="Neu hier und Suchst nach Spielern? 🔍", value="Wähle im Menü ´´´Spielersuche´´´ aus dort findest du Die Spielersuche für PC und Konsole", inline=False
        ).add_field(name="\u200b", value="\u200b", inline=False
        ).add_field(name="Du suchst nach SOTF News und Patchnotes? 🚨", value="Wähle im Menü ´´´Neuigkeiten´´´ aus um Nichts mehr zu Verpassen!", inline=False
        ).set_image(url="https://cdn.discordapp.com/attachments/1029833877402951710/1087113531796750526/Unbenannt-17.png"
        ).set_thumbnail(url="https://cdn.discordapp.com/attachments/1029833877402951710/1087104954067603578/test_5555.png"), view=Spielsuche_view())

    @_set_hilfemenu.error
    async def _set_hilfemenu_error(self, ctx: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingRole):
            await ctx.response.send_message("Du hast keine Bereichtigung !!!", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(HilfeMenu(bot))