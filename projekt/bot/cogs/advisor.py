import discord
from discord.ext import commands
from discord import app_commands

from bot.checks.permissions import admin_required

GUILD_ID = 1123368740134862938

class AdvisorCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.guild_only()
    @app_commands.command(
        name="ask",
        description="Zapytaj AI o sytuację"
    )
    @admin_required()
    async def ask(
        self,
        interaction,
        question: str
    ):
        await interaction.response.send_message(
            f"Otrzymano pytanie: {question}"
        )


async def setup(bot):
    
    guild = discord.Object(id=GUILD_ID)
    
    await bot.add_cog(
        AdvisorCog(bot),
        guild=guild
    )