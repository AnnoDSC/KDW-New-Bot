import sys

sys.dont_write_bytecode = True
from discord.ext import commands
from discord import app_commands
import discord, sqlite3

db = sqlite3.connect('db.db')


class AddVoice(commands.Cog):

  def __init__(self, bot: commands.Bot):
    self.bot = bot

  @app_commands.commands.command(name="add_voice", description="Fügt einen TempVC zu der datenbank hinzu")
  async def _addvoice(self, interaction: discord.Interaction, channel: discord.VoiceChannel):
    if interaction.user.guild_permissions.administrator:
      cc = db.execute("SELECT channel_id FROM tempvc_channel where channel_id = ?",(channel.id, ))
      r = cc.fetchone()
      if r:
        if channel.id == int(r[0]):
          emb = discord.Embed(
            title="Ticket System", colour=discord.Color.red()).add_field(
              name=f"Der Channel {channel.mention} ist bereits im system",
              value="",
              inline=False)
          await interaction.response.send_message(embed=emb)
      else:
        db.execute("INSERT INTO tempvc_channel (channel_id) VALUES (?)",(channel.id, ))
        db.commit()
        emb2 = discord.Embed(
          title="Ticket System", colour=discord.Color.green()).add_field(
            name=f"ID: {channel.mention} wurde zum System hinzugefügt",
            value="",
            inline=False)
        await interaction.response.send_message(embed=emb2)
    else:
      emb_error2 = discord.Embed(
        title="Counting System",
        description="Du hast keine Rechte Dies zu tun",
        colour=discord.Color.red())
      await interaction.response.send_message(embed=emb_error2)

  @app_commands.commands.command(name="del_voice", description="Entferne einen TempVC aus der datenbank")
  async def _delvoice(self, interaction: discord.Interaction, channel: discord.VoiceChannel):
    if interaction.user.guild_permissions.administrator:
      cc = db.execute("SELECT channel_id FROM tempvc_channel where channel_id = ?",(channel.id, ))
      r = cc.fetchone()
      if r:
        if channel.id == int(r[0]):
          cc = db.execute("DELETE FROM tempvc_channel where channel_id = ?",(channel.id, ))
          db.commit()
          await interaction.response.send_message(f"Channel: {channel.mention}/{channel.id}\nwurde aus der Datenbank endfernt"
          )
      else:
        await interaction.response.send_message(f"Channel: {channel.mention}/{channel.id}\nist nicht in der Datenbank"
        )
    else:
      emb_error2 = discord.Embed(
        title="Counting System",
        description="Du hast keine Rechte Dies zu tun",
        colour=discord.Color.red())
      await interaction.response.send_message(embed=emb_error2)


async def setup(bot: commands.Bot):
  await bot.add_cog(AddVoice(bot))
