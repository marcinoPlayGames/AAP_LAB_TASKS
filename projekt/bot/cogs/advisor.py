import discord
from discord.ext import commands
from discord import app_commands

from bot.checks.permissions import admin_required

from services.rag import RAGService

from services.ai_service import AIService

from services.database import Database

from datetime import timedelta

GUILD_ID = 1123368740134862938

class ModerationButtons(discord.ui.View):


    def __init__(
        self,
        bot,
        member,
        penalty
    ):
        super().__init__(timeout=60)

        self.bot = bot
        self.member = member
        self.penalty = penalty



    @discord.ui.button(
        label="Mute 2h",
        style=discord.ButtonStyle.red
    )
    async def mute(
        self,
        interaction,
        button
    ):

        duration = parse_penalty(
            self.penalty
        )

        if duration:

            await self.member.timeout(
                duration,
                reason="AI Moderator"
            )

        await self.member.timeout(
            duration,
            reason="AI Moderator"
        )

        await interaction.response.send_message(
            f"🔇 Wyciszono {self.member.mention} na 2h"
        )



    @discord.ui.button(
        label="Ban",
        style=discord.ButtonStyle.danger
    )
    async def ban(
        self,
        interaction,
        button
    ):

        await interaction.response.send_message(
            "Ban wykonany.",
            ephemeral=True
        )



    @discord.ui.button(
        label="Anuluj",
        style=discord.ButtonStyle.gray
    )
    async def cancel(
        self,
        interaction,
        button
    ):

        await interaction.response.send_message(
            "Anulowano.",
            ephemeral=True
        )
    
    def parse_penalty(penalty):

        if penalty.startswith("mute"):

            value = penalty.split()[1]

            if value.endswith("h"):

                hours = int(
                    value.replace("h", "")
                )

                return timedelta(
                    hours=hours
                )

        return None

class AdvisorCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.rag = RAGService()
        self.ai = AIService()
        self.db = Database()

    @app_commands.guild_only()
    @app_commands.command(
        name="ask",
        description="Zapytaj AI o sytuację"
    )
    async def ask(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        question: str
    ):
        context = self.rag.search(question)

        context_text = f"""
Regulamin:
{context["regulamin"]}

Taryfikator:
{context["taryfikator"]}
"""

        await interaction.response.defer()
        
        response = self.ai.generate_response(
            question,
            context_text
        )
        
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


async def setup(bot):
    
    guild = discord.Object(id=GUILD_ID)
    
    await bot.add_cog(
        AdvisorCog(bot),
        guild=guild
    )