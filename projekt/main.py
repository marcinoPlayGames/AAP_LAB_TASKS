print("PLIK MAIN ZOSTAŁ URUCHOMIONY")

import discord
from discord.ext import commands

from config import DISCORD_TOKEN

from config import GUILD_SERVER_ID

GUILD_ID = GUILD_SERVER_ID

class DiscordBot(commands.Bot):

    def __init__(self):

        print("INIT START")
        
        intents = discord.Intents.default()
        intents.members = True

        super().__init__(
            command_prefix="!",
            intents=intents
        )
        
        print("INIT END")

    async def setup_hook(self):
        
        print("SETUP_HOOK START")
        
        print("Ładowanie Cogów...")
        
        await self.load_extension(
            "bot.cogs.advisor"
        )

        print("ADVISOR LOADED")
        
        await self.load_extension(
            "bot.cogs.moderation"
        )
        
        print("MODERATION LOADED")
        
        await self.load_extension(
            "bot.cogs.history"
        )
        
        print("HISTORY LOADED")

        synced = await self.tree.sync()
        
        guild = discord.Object(id=GUILD_ID)

        #self.tree.clear_commands(guild=guild)

        synced = await self.tree.sync(
            guild=guild
        )
        
        print(
            f"Zsynchronizowano {len(synced)} komend"
        )
        
        print("GLOBAL:")
        for cmd in self.tree.get_commands():
            print(cmd.name)
        
        print("GUILD:")
        for cmd in self.tree.get_commands(guild=guild):
            print(cmd.name)
        
        for command in self.tree.get_commands():
            print(command.name)
        
    async def on_ready(self):
        print("ON_READY")
        print(f"Zalogowano jako {self.user}")


bot = DiscordBot()

bot.run(DISCORD_TOKEN)