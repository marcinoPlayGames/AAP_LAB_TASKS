import discord
from discord.ext import commands
from discord import app_commands

from bot.checks.permissions import admin_required

from services.rag import RAGService

GUILD_ID = 1123368740134862938

class AdvisorCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.rag = RAGService()

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
        context = self.rag.search(question)


        await interaction.response.send_message(
            f"""
        Kontekst z dokumentów:

        {context}

        Twoje pytanie:

        {question}
        """
        )
    
    @ask.error
    async def ask_error(
        self,
        interaction,
        error
    ):

        if isinstance(
            error,
            app_commands.CheckFailure
        ):
            await interaction.response.send_message(
                "Nie masz uprawnień do tej komendy.",
                ephemeral=True
            )


async def setup(bot):
    
    guild = discord.Object(id=GUILD_ID)
    
    await bot.add_cog(
        AdvisorCog(bot),
        guild=guild
    )