import discord, config
from src.Utils.database import DatabaseUtils as db

warn = db("db.db")

class Add_Warn(discord.ui.Modal):
    def __init__(self, user: discord.Member):
        super().__init__(
            title="Test",
            timeout=None,
            custom_id="Add_Warn"
        )
        self.user = user
    
    grund = discord.ui.TextInput(
        label="Grund des Warn's",
        placeholder="Z.b Hat andere Member in den Dm's beleidigt"
    )

    async def on_submit(self, ctx: discord.Interaction):
        check = warn.add_warn(self.user.id, self.grund.value)
        if check:
            await ctx.response.send_message(embed=discord.Embed(
                title="Warn System",
                description=f"Der Nutzer {self.user.mention} hat einen Warn bekommen mit dem Grund {self.grund.value}",
                colour=config.BOT_EMBED_COLOUR
            ))
        else:
            await ctx.response.send_message(embed=discord.Embed(
                title="Error System",
                description="Ein Fehler ist aufgetreten bitte wende dich an den Admin",
                colour=config.BOT_EMBED_COLOUR
            ))
