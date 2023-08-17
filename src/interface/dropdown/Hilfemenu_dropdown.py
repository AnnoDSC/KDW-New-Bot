from typing import Optional
import discord, config
from discord.ext import commands

class Spielersuche(discord.ui.Select):
    def __init__(self):
        option = [
            discord.SelectOption(label="Spielersuche", description="Hier findest du die Channel yur Spielersuche.", emoji="🎮", value="1"),
            discord.SelectOption(label="Ansprechpartner/Ticket erstellen", description="Du hast ein Anliegen? Wende dich an uns!", emoji="📬", value="2"),
            discord.SelectOption(label="Neuigkeiten", description="Verpasse keine Soft News.", emoji="🚨", value="3")
        ]
        super().__init__(placeholder="", min_values=1, max_values=1, options=option, custom_id="Spielersuche")
    
    async def callback(self, ctx: discord.Interaction):
        if self.values[0] == "1":
            await ctx.response.send_message(embed=discord.Embed(
                title="Spielersuche",
                description="Hier sind die Kanäle für die Spielersuche:",
                colour=config.BOT_EMBED_COLOUR,
            ).add_field(name="Spielersuche PC", value="<#790974814738448465>", inline=False
            ).add_field(name="Spielersuche Konsole", value="<#805875400357314652>", inline=False
            ).set_thumbnail(url="https://cdn.discordapp.com/attachments/1029833877402951710/1087104954067603578/test_5555.png"
            ).set_image(url="https://cdn.discordapp.com/attachments/1029833877402951710/1087124165573755011/spielersuche.png"), ephemeral=True)
        elif self.values[0] == "2":
            await ctx.response.send_message(embed=discord.Embed(
                title="Ticket und Ansprechpartner",
                description="Du hast ein Anliegen? Wende dich an uns!",
                colour=config.BOT_EMBED_COLOUR,
            ).add_field(name="Ticket erstellen 📬", value="Klicke hier <#821335849412591616> um ein Ticket zu erstellen!", inline=False
            ).add_field(name="Ansprechpartner", value="Unsere Wächter des Waldes regieren auf jeden Hilferuf der Community!", inline=False
            ).set_thumbnail(url="https://cdn.discordapp.com/attachments/1029833877402951710/1087104954067603578/test_5555.png"
            ).set_image(url="https://cdn.discordapp.com/attachments/1029833877402951710/1087124165783453746/ansprechpartner.png"), ephemeral=True)
        elif self.values[0] == "3":
            await ctx.response.send_message(embed=discord.Embed(
                title="Neuigkeiten",
                description="Hier findest du unsere Sotf-News und Events:",
                colour=config.BOT_EMBED_COLOUR,
            ).add_field(name="Sons Of The Forest News und Updates!", value="<#790892997603885076>", inline=False
            ).add_field(name="Hier findest du neuen und anstehenden Events!", value="<#1082389844912771183>", inline=False
            ).set_thumbnail(url="https://cdn.discordapp.com/attachments/1029833877402951710/1087104954067603578/test_5555.png"
            ).set_image(url="https://cdn.discordapp.com/attachments/1029833877402951710/1087124165783453746/ansprechpartner.png"), ephemeral=True)


class Spielsuche_view(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Spielersuche())