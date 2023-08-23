import sys
sys.dont_write_bytecode = True
import discord, sqlite3
from discord.ext import commands
db = sqlite3.connect("db.db")

class Kick_Dropdown(discord.ui.Select):
    def __init__(self, abc: list):
        options = []
        
        for member in abc:
            member: discord.Member
            options.append(discord.SelectOption(label=f'{member.name}', description=f'', emoji='❌'),)

        super().__init__(placeholder='Wähle eine Person die du Kicken Möchtest', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        for member in interaction.channel.members:
            if self.values[0] == member.name:
                await member.move_to(None)
                await interaction.response.edit_message(content=f"Du hast den Benutzer {member.mention} Gekickt", view=None)

class Ban_Dropdown(discord.ui.Select):
    def __init__(self, abc: list):
        options = []
        
        for member in abc:
            member: discord.Member
            options.append(discord.SelectOption(label=f'{member.name}', description=f'', emoji='❌'),)

        super().__init__(placeholder='Wähle eine Person die du Kicken Möchtest', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        for member in interaction.channel.members:
            if self.values[0] == member.name:
                r = db.execute("SELECT * FROM tempvc_channel_create_ban",).fetchall()
                if r is None:
                    pass
                else:
                    db.execute("INSERT INTO tempvc_channel_create_ban (channel_id, banned_user_id) VALUES (?, ?)", (interaction.channel.id, member.id,))
                    db.commit()
                    await interaction.channel.set_permissions(member, connect=False)
                    await member.move_to(None)
                    await interaction.response.edit_message(content=f"Du hast den Benutzer {member.mention} gekickt Gebannt", view=None)

class Unban_Dropdown(discord.ui.Select):
    def __init__(self, abc: list):
        options = []
        
        for member in abc:
            member: discord.Member
            options.append(discord.SelectOption(label=f'{member.name}', description=f'', emoji='✅'),)

        super().__init__(placeholder='Wähle eine Person die du Endbannen Möchtest', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        r1 = db.execute("SELECT banned_user_id FROM tempvc_channel_create_ban").fetchall()
        for member in r1:
            mm = await interaction.guild.fetch_member(int(member[0]))
            if self.values[0] == mm.name:
                db.execute("DELETE FROM tempvc_channel_create_ban WHERE banned_user_id = ?", (mm.id,))
                db.commit()
                await interaction.channel.set_permissions(mm, overwrite=None)
                await interaction.response.edit_message(content=f"Der Benutzer {mm.mention} wurde erfolgreich Endbannt", view=None)

class Option_Dropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label=f'Kicke einen User', description=f'', emoji='❌', value="1"),
            discord.SelectOption(label=f'Banne einen User', description=f'', emoji='❌', value="2"),
        ]
    

        super().__init__(placeholder='Wähle eine Option', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "1":
            r = db.execute("SELECT * FROM tempvc_channel_create WHERE owner = ?", (interaction.user.id,)).fetchall()
            if r:
                if interaction.user.id == int(r[0][1]) and interaction.channel.id == int(r[0][0]):
                    mm = interaction.channel.members
                    mm.remove(interaction.user)
                    if mm:
                        await interaction.response.edit_message(view=KickView(members=mm))
                    else:
                        await interaction.response.edit_message(content="Es Müssen erst ein paar leute in deinem Voice sein", view=None)

                else:
                    await interaction.response.send_message(f"Du Bist leider nicht berichtigt dies zu tun {interaction.user.mention}", ephemeral=True)
            else:
                await interaction.response.send_message(f"Du Bist leider nicht berichtigt dies zu tun {interaction.user.mention}", ephemeral=True)

        elif self.values[0] == "2":
            r = db.execute("SELECT * FROM tempvc_channel_create WHERE owner = ?", (interaction.user.id,)).fetchall()
            if r:
                if interaction.user.id == int(r[0][1]) and interaction.channel.id == int(r[0][0]):
                    mm = interaction.channel.members
                    mm.remove(interaction.user)
                    if mm:
                        await interaction.response.edit_message(view=BanView(members=mm))
                    else:
                        await interaction.response.edit_message(content="Es Müssen erst ein paar leute in deinem Voice sein", view=None)
                else:
                    await interaction.response.send_message(f"Du Bist leider nicht berichtigt dies zu tun {interaction.user.mention}", ephemeral=True)
            else:
                await interaction.response.send_message(f"Du Bist leider nicht berichtigt dies zu tun {interaction.user.mention}", ephemeral=True)#

class Option_Dropdown2(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label=f'Kicke einen User', description=f'', emoji='❌', value="1"),
            discord.SelectOption(label=f'Banne einen User', description=f'', emoji='❌', value="2"),
            discord.SelectOption(label=f'Endbanne einen User', description=f'', emoji='❌', value="3"),
        ]
    

        super().__init__(placeholder='Wähle eine Option', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "1":
            r = db.execute("SELECT * FROM tempvc_channel_create WHERE owner = ?", (interaction.user.id,)).fetchall()
            if r:
                if interaction.user.id == int(r[0][1]) and interaction.channel.id == int(r[0][0]):
                    mm = interaction.channel.members
                    mm.remove(interaction.user)
                    if mm:
                        await interaction.response.edit_message(view=KickView(members=mm))
                    else:
                        await interaction.response.edit_message(content="Es Müssen erst ein paar leute in deinem Voice sein", view=None)

                else:
                    await interaction.response.send_message(f"Du Bist leider nicht berichtigt dies zu tun {interaction.user.mention}", ephemeral=True)
            else:
                await interaction.response.send_message(f"Du Bist leider nicht berichtigt dies zu tun {interaction.user.mention}", ephemeral=True)

        elif self.values[0] == "2":
            r = db.execute("SELECT * FROM tempvc_channel_create WHERE owner = ?", (interaction.user.id,)).fetchall()
            if r:
                if interaction.user.id == int(r[0][1]) and interaction.channel.id == int(r[0][0]):
                    mm = interaction.channel.members
                    mm.remove(interaction.user)
                    if mm:
                        await interaction.response.edit_message(view=BanView(members=mm))
                    else:
                        await interaction.response.edit_message(content="Es Müssen erst ein paar leute in deinem Voice sein", view=None)
                else:
                    await interaction.response.send_message(f"Du Bist leider nicht berichtigt dies zu tun {interaction.user.mention}", ephemeral=True)
            else:
                await interaction.response.send_message(f"Du Bist leider nicht berichtigt dies zu tun {interaction.user.mention}", ephemeral=True)#

        elif self.values[0] == "3":
            r = db.execute("SELECT * FROM tempvc_channel_create WHERE owner = ?", (interaction.user.id,)).fetchall()
            if r:
                if interaction.user.id == int(r[0][1]) and interaction.channel.id == int(r[0][0]):
                    r1 = db.execute("SELECT * FROM tempvc_channel_create_ban").fetchall()
                    memb = []
                    for channel_id, banned_user in r1:
                        member = await interaction.guild.fetch_member(banned_user)
                        memb.append(member)
                    await interaction.response.edit_message(view=UnBanView(members=memb))
                else:
                    await interaction.response.send_message(f"Du Bist leider nicht berichtigt dies zu tun {interaction.user.mention}", ephemeral=True)
            else:
                await interaction.response.send_message(f"Du Bist leider nicht berichtigt dies zu tun {interaction.user.mention}", ephemeral=True)


class BanView(discord.ui.View):
    def __init__(self, members: list):
        super().__init__()
        self.add_item(Ban_Dropdown(abc=members))

class UnBanView(discord.ui.View):
    def __init__(self, members: list):
        super().__init__()
        self.add_item(Unban_Dropdown(abc=members))

class KickView(discord.ui.View):
    def __init__(self, members: list):
        super().__init__()
        self.add_item(Kick_Dropdown(abc=members))

class OptionView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Option_Dropdown())

class OptionView2(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Option_Dropdown2())