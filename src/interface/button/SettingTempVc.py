import sys
sys.dont_write_bytecode = True
import discord, sqlite3
from src.interface.modal.ChangeTempVc import Slots, Name
from discord.ext import commands
from src.interface.dropdown.DropDown import OptionView, OptionView2

db = sqlite3.connect('db.db')

class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label='👥 Slots', style=discord.ButtonStyle.green, custom_id="Slots_TempVc")
    async def _slots(self, interaction: discord.Interaction, button: discord.ui.Button):
        member_id = interaction.user.id
        cc = db.execute("SELECT channel_id, owner FROM tempvc_channel_create WHERE owner = ?", (member_id,))
        r = cc.fetchall()
        if r:
            if member_id == int(r[0][1]) and interaction.channel.id == int(r[0][0]):
                await interaction.response.send_modal(Slots())
            else:
                await interaction.response.send_message(f"Du Bist leider nicht berichtigt dies zu tun {interaction.user.mention}", ephemeral=True)
        else:
            await interaction.response.send_message(f"Du Bist leider nicht berichtigt dies zu tun {interaction.user.mention}", ephemeral=True)

    @discord.ui.button(label='✏️ Namen', style=discord.ButtonStyle.green, custom_id="Name_TempVc")
    async def _name(self, interaction: discord.Interaction, button: discord.ui.Button):
        member_id = interaction.user.id
        cc = db.execute("SELECT channel_id, owner FROM tempvc_channel_create WHERE owner = ?", (member_id,))
        r = cc.fetchall()
        if r:
            if member_id == int(r[0][1]) and interaction.channel.id == int(r[0][0]):
                await interaction.response.send_modal(Name())
            else:
                await interaction.response.send_message(f"Du Bist leider nicht berichtigt dies zu tun {interaction.user.mention}", ephemeral=True)
        else:
            await interaction.response.send_message(f"Du Bist leider nicht berichtigt dies zu tun {interaction.user.mention}", ephemeral=True)

    @discord.ui.button(label='🔒 Schließen \ 🔓 Öffnen', style=discord.ButtonStyle.red, custom_id="Close_TempVc")
    async def _close(self, interaction: discord.Interaction, button: discord.ui.Button):
        member_id = interaction.user.id
        r = db.execute("SELECT * FROM tempvc_channel_create WHERE owner = ?", (member_id,)).fetchall()
        if r:
            if member_id == int(r[0][1]) and interaction.channel.id == int(r[0][0]):
                permissions = interaction.channel.permissions_for(interaction.guild.default_role)
                if permissions.connect == True:
                    self._close.style = discord.ButtonStyle.green
                    ch = interaction.guild.get_channel(r[0][0])
                    msg = await ch.fetch_message(r[0][2])
                    await msg.edit(view=self) 
                    await interaction.channel.set_permissions(interaction.guild.default_role, connect=False)
                    for member in interaction.channel.members:
                        await interaction.channel.set_permissions(member, connect=True)
                    await interaction.response.send_message(f'Der Kanal {interaction.channel.mention} ist für alle Benutzer unsichtbar.', ephemeral=True) 

                elif permissions.connect == False or None:
                    self._close.style = discord.ButtonStyle.red
                    ch = interaction.guild.get_channel(r[0][0])
                    msg = await ch.fetch_message(r[0][2])
                    await msg.edit(view=self) 
                    await interaction.channel.set_permissions(interaction.guild.default_role, connect=True)
                    for member in interaction.channel.members:
                        await interaction.channel.set_permissions(member, overwrite=None)
                    await interaction.response.send_message(f'Der Kanal {interaction.channel.mention} ist für alle Benutzer sichtbar.', ephemeral=True)
   

            else:
                await interaction.response.send_message(f"Du Bist leider nicht berichtigt dies zu tun {interaction.user.mention}", ephemeral=True)
        else:
            await interaction.response.send_message(f"Du Bist leider nicht berichtigt dies zu tun {interaction.user.mention}", ephemeral=True)

    @discord.ui.button(label='❌ Ban \ ❌ Unban \ ❌ Kicken', style=discord.ButtonStyle.red, custom_id="Ban_TempVc")
    async def _ban(self, interaction: discord.Interaction, button: discord.ui.Button):
        member_id = interaction.user.id
        r = db.execute("SELECT * FROM tempvc_channel_create WHERE owner = ?", (member_id,)).fetchall()
        if r:
            if member_id == int(r[0][1]) and interaction.channel.id == int(r[0][0]):
                cc2 = db.execute("SELECT banned_user_id FROM tempvc_channel_create_ban WHERE channel_id = ?", (interaction.channel.id,)).fetchone()
                if cc2 is None:
                    await interaction.response.send_message(view=OptionView(), ephemeral=True)
                else:
                    await interaction.response.send_message(view=OptionView2(), ephemeral=True)
            else:
                await interaction.response.send_message(f"Du Bist leider nicht berichtigt dies zu tun {interaction.user.mention}", ephemeral=True)
        else:
            await interaction.response.send_message(f"Du Bist leider nicht berichtigt dies zu tun {interaction.user.mention}", ephemeral=True)