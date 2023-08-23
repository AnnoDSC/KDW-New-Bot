import discord 
class Slots(discord.ui.Modal,  title='Slots'):

    name = discord.ui.TextInput(
        label='Plätze im Voice',
        placeholder='Deine Slotzahl bitte...',
    )

    async def on_submit(self, interaction: discord.Interaction):
        a = str(self.name)
        if int(a) >= 100:
            await interaction.response.send_message(f"Slots dürfen nur **99** sein deine angabe war {a}", ephemeral=True)
        else:
            await interaction.channel.edit(user_limit=a)
            await interaction.response.send_message(f"Slot anzahl zu **{a}** geändert", ephemeral=True)

class Name(discord.ui.Modal,  title='Name'):

    name1 = discord.ui.TextInput(
        label='Name des Voice',
        placeholder='Deinen Namen bitte...',
    )

    async def on_submit(self, interaction: discord.Interaction):
        a = str(self.name1)
        await interaction.channel.edit(name=a)
        await interaction.response.send_message(f"Name Des voices zu **{a}** geändert", ephemeral=True)