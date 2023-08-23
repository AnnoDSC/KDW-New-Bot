import sys
sys.dont_write_bytecode = True
from discord.ext import commands, tasks
import discord, sqlite3, random
from src.interface.button.SettingTempVc import Confirm
from discord.utils import get

db = sqlite3.connect('db.db')

class Tempvoices(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.check_if_channel_exst.start()
        self.check_if_channel_delete_for_ban.start()

    def cog_unload(self):
        self.check_if_channel_exst.cancel()
        self.check_if_channel_delete_for_ban.stop()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        possible_channel_name = f"{member.name}'s Raum"
        if after.channel:
            cc = db.execute("SELECT * FROM tempvc_channel WHERE channel_id = ?", (after.channel.id,))
            r = cc.fetchone()
            if r:
                if after.channel.id == int(r[0]):
                    temp_channel = await after.channel.clone(name=possible_channel_name)
                    await member.move_to(temp_channel)

                    embed = discord.Embed(
                        title="Temp Voice System",
                        color=discord.Color.red()
                    )
                    embed.add_field(
                        name=f"Dies Ist nun dein eigener Voice. Drücke auf Slots/Name Um das userlimit umzustellen oder den namen zu wecheln", 
                        value="", 
                        inline=False)

                    msg = await temp_channel.send(f"{member.mention}", embed=embed, view = Confirm())
                    db.execute("INSERT INTO tempvc_channel_create (channel_id, owner, message_id) VALUES (?, ?, ?)", (temp_channel.id, member.id, msg.id,))
                    db.commit()

        if before.channel:
            cc1 = db.execute("SELECT * FROM tempvc_channel_create WHERE channel_id = ?", (before.channel.id,))
            r1 = cc1.fetchone()
            if r1:
                if before.channel.id == int(r1[0]):
                    if len(before.channel.members) == 0:
                        db.execute("DELETE FROM tempvc_channel_create WHERE channel_id = ?", (before.channel.id,))
                        db.commit()
                        await before.channel.delete()
                    elif member.id == int(r1[1]):
                        new_owner = random.choice(before.channel.members)
                        await before.channel.send(f"Der Neue Owner des Channels ist {new_owner.mention}")
                        db.execute("update tempvc_channel_create set owner = ? where channel_id = ?", (new_owner.id, before.channel.id))
                        db.commit()

        if before.channel:
            cc1 = db.execute("SELECT channel_id FROM tempvc_channel_create WHERE channel_id = ?", (before.channel.id,)).fetchone()
            cc2 = db.execute("SELECT channel_id FROM tempvc_channel_create_ban WHERE banned_user_id = ?", (member.id,)).fetchone()
            if cc1 and cc2 is None:
                if before.channel.id == int(r1[0]):
                    await before.channel.set_permissions(member, overwrite=None)

    @tasks.loop(seconds=2)
    async def check_if_channel_exst(self):
        get_channel = db.execute("SELECT * FROM tempvc_channel_create").fetchall()
        for channel_id, owner, msg_id in get_channel:
            try:
                channel = get(self.bot.get_all_channels(), id=channel_id)
                if channel is None:
                    db.execute("delete from tempvc_channel_create WHERE channel_id = ?", (channel_id,))
                    db.commit()
                    return
            except discord.NotFound:
                continue
            else:
                if len(channel.members) == 0:
                    db.execute("delete from tempvc_channel_create WHERE channel_id = ?", (channel_id,))
                    db.commit()
                    await channel.delete()

    @tasks.loop(seconds=2)
    async def check_if_channel_delete_for_ban(self):
        get_channel = db.execute("SELECT * FROM tempvc_channel_create_ban").fetchall()
        for channel_id, ban in get_channel:
            try:
                channel = await self.bot.fetch_channel(channel_id)
            except:
                db.execute("delete from tempvc_channel_create_ban WHERE channel_id = ?", (channel_id,))
                db.commit()


async def setup(bot):
    await bot.add_cog(Tempvoices(bot))