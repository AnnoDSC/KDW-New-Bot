import sys
sys.dont_write_bytecode = True

import discord, config, os, sqlite3
from discord import app_commands
from discord.ext import commands
from src.interface.dropdown.Hilfemenu_dropdown import Spielsuche_view


class Bot(commands.Bot):
    def __init__(self, intents: discord.Intents):
        super().__init__(
            command_prefix = config.BOT_PREFIX, 
            intents=intents,
            status=discord.Status.idle,
            activity=discord.Game(name=f"/help | {config.BOT_VERSION}")
        )
        self.db = sqlite3.connect("db.db")
    
    async def setup_hook(self):
        print("----------------------")
        for file in os.listdir("./src/commands"):
            if file.endswith(".py"):
                await self.load_extension(f'src.commands.{file[:-3]}')
                print(file[:-3] + " Loaded ✅")
        for file in os.listdir("./src/tasks"):
            if file.endswith(".py"):
                await self.load_extension(f'src.tasks.{file[:-3]}')
                print(file[:-3] + " Loaded ✅")
        print("----------------------")
        self.add_view(Spielsuche_view())
        await self.tree.sync()

    async def on_ready(self):
        print("----------------------")
        print(f"Logged in as {self.user.name}/{self.user.id}")
        print("----------------------")

intentse = discord.Intents.all()
bot = Bot(intents=intentse)

bot.run(config.BOT_TOKEN)