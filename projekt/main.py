import discord
from discord.ext import commands

from config import DISCORD_TOKEN


class DiscordBot(commands.Bot):

    def __init__(self):

        intents = discord.Intents.default()
        intents.members = True

        super().__init__(
            command_prefix="!",
            intents=intents
        )

    async def setup_hook(self):

        print("Ładowanie Cogów...")
        
        await self.load_extension(
            "bot.cogs.advisor"
        )

        await self.load_extension(
            "bot.cogs.moderation"
        )

        await self.tree.sync()
        
        print(
            f"Zsynchronizowano {len(synced)} komend"
        )
        
    @bot.event
    async def on_ready():
        print(f"Zalogowano jako {bot.user}")


bot = DiscordBot()

bot.run(DISCORD_TOKEN)