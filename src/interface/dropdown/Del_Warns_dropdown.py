from typing import Optional
import discord, config
from discord.ext import commands
from src.Utils.database import DatabaseUtils as db

warns = db("db.db")

class Del_Warns(discord.ui.Select):
    def __init__(self, user: discord.Member):
        self.user = user

        emoji_list = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        warn_list = warns.get_warn(self.user.id)

        options = []
        for index, x in enumerate(warn_list, start=1):
            if index > len(emoji_list):
                break
            emoji = emoji_list[index - 1]
            options.append(discord.SelectOption(label=f"{x[0]}", description=f"", emoji=emoji, value=f"{index}"))

        super().__init__(placeholder="", options=options, custom_id="Spielersuche")
    
    async def callback(self, ctx: discord.Interaction):
        warns.del_warn(self.user.id, self.values[0])
        ctx.response.send_message(embed=discord.Embed(
                title="Warn System",
                description=f"Der Nutzer {self.user.mention} hat einen Warn verloren",
                colour=config.BOT_EMBED_COLOUR
        ), ephemeral=True)

class Del_Warns_view(discord.ui.View):
    def __init__(self, user: discord.User):
        super().__init__(timeout=None)
        self.add_item(Del_Warns(user))