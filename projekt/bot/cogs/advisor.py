import discord
from discord.ext import commands
from discord import app_commands

from bot.checks.permissions import admin_required

from services.rag import RAGService

from services.ai_service import AIService

from services.database import Database

from config import GUILD_SERVER_ID

from bot.views.moderation_buttons import ModerationButtons

GUILD_ID = GUILD_SERVER_ID


class AdvisorCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.rag = bot.rag
        self.ai = AIService()
        self.db = Database()

    @app_commands.guild_only()
    @app_commands.command(
        name="ask",
        description="Zapytaj AI o sytuację"
    )
    @admin_required()
    async def ask(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        question: str
    ):
        try:
            context = self.rag.search(question)

        except Exception as e:
            print("RAG ERROR:", e)

            await interaction.followup.send(
                "❌ Błąd podczas analizy regulaminu."
            )

            return
        
        penalty = context["kara"]

        await interaction.response.defer()
        
        print("REGULAMIN:")
        print(context["regulamin"])

        print("TARYFIKATOR:")
        print(context["taryfikator"])

        print("KARA:")
        print(context["kara"])
        
        try:
            response = self.ai.generate_response(
                question,
                context["regulamin"],
                context["taryfikator"],
                context["kara"]
            )
        except Exception as e:
            print(e)
            raise
        
        if len(response) > 1900:

            response = response[:1900]
        
        view = ModerationButtons(
            self.bot,
            member,
            penalty
        )


        await interaction.followup.send(
            response,
            view=view
        )
        
        self.db.save_decision(
            interaction.user.name,
            question,
            response
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

    @app_commands.command(
        name="reload_documents",
        description="Przeładowuje regulamin i taryfikator"
    )
    @admin_required()
    async def reload_documents(
            self,
            interaction: discord.Interaction
    ):

        try:

            self.rag.reload()

        except Exception as e:

            await interaction.response.send_message(
                f"❌ Nie udało się przeładować dokumentów:\n{e}",
                ephemeral=True
            )

            return

        await interaction.response.send_message(
            "✅ Regulamin i taryfikator zostały przeładowane."
        )


async def setup(bot):
    
    guild = discord.Object(id=GUILD_ID)
    
    await bot.add_cog(
        AdvisorCog(bot),
        guild=guild
    )