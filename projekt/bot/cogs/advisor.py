from discord.ext import commands
from discord import app_commands

from bot.checks.permissions import admin_required


class AdvisorCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

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
    await bot.add_cog(
        AdvisorCog(bot)
    )