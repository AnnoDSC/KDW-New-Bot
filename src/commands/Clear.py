import sys
sys.dont_write_bytecode = True

import discord, sqlite3
from discord.ext import commands
from discord import app_commands

class Clear(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name="clear", description="Cleare Messages in einem Channel")
    @app_commands.describe(anzahl="Die Anzahl der Messages die Geloecht werden sollen Nix = 100")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def _clear(self, ctx: discord.Interaction, anzahl: int = None):
        if anzahl == None: 
            anzahl = 100

        await ctx.channel.purge(limit=anzahl)
        await ctx.response.send_message(embed=discord.Embed(
            title="Clear System",
            description=f"Ich habe {anzahl} Nachichten geloecht",
            colour=discord.Color.green()
        ))
    
    @_clear.error
    async def _clear_error(self, ctx: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingRole):
            await ctx.response.send_message("Du hast keine Bereichtigung !!!", ephemeral=True)




async def setup(bot: commands.Bot):
    await bot.add_cog(Clear(bot))