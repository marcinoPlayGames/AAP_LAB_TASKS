import discord
from discord.ext import commands
from discord import app_commands

from bot.checks.permissions import admin_required

from services.rag import RAGService

from services.ai_service import AIService

from services.database import Database

from datetime import timedelta

from config import GUILD_SERVER_ID

GUILD_ID = GUILD_SERVER_ID

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

        self.create_buttons()

    async def cancel(
        self,
        interaction: discord.Interaction
    ):

        await interaction.response.send_message(
            "❌ Anulowano.",
            ephemeral=True
        )
    
    def parse_penalty(self, penalty):

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
    
    def create_buttons(self):

        if not self.penalty:
            return

        if self.penalty.startswith("mute"):

            button = discord.ui.Button(
                label="Nałóż karę",
                style=discord.ButtonStyle.red
            )

            button.callback = self.apply_penalty

            self.add_item(button)

        elif self.penalty == "ban":

            button = discord.ui.Button(
                label="Zbanuj",
                style=discord.ButtonStyle.danger
            )

            button.callback = self.apply_penalty

            self.add_item(button)

        elif self.penalty == "kick":

            button = discord.ui.Button(
                label="Wyrzuć",
                style=discord.ButtonStyle.blurple
            )

            button.callback = self.apply_penalty

            self.add_item(button)

        cancel_button = discord.ui.Button(
            label="Anuluj",
            style=discord.ButtonStyle.gray
        )

        cancel_button.callback = self.cancel

        self.add_item(cancel_button)
    
    async def apply_penalty(
        self,
        interaction: discord.Interaction
    ):
        
                    
        if not self.penalty:
            return
        
        if self.penalty.startswith("mute"):

            duration = self.parse_penalty(
                self.penalty
            )

            await self.member.timeout(
                duration,
                reason="AI Moderator"
            )
            
            for item in self.children:
                item.disabled = True

            await interaction.message.edit(
                view=self
            )

            await interaction.response.send_message(
                f"🔇 Wyciszono {self.member.mention}"
            )

            return


        if self.penalty == "ban":

            await self.member.ban(
                reason="AI Moderator"
            )
            
            for item in self.children:
                item.disabled = True

            await interaction.message.edit(
                view=self
            )

            await interaction.response.send_message(
                f"🔨 Zbanowano {self.member.mention}"
            )

            return


        if self.penalty == "kick":

            await self.member.kick(
                reason="AI Moderator"
            )
            
            for item in self.children:
                item.disabled = True

            await interaction.message.edit(
                view=self
            )

            await interaction.response.send_message(
                f"👢 Wyrzucono {self.member.mention}"
            )

            return

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
    @admin_required()
    async def ask(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        question: str
    ):
        context = self.rag.search(question)
        
        penalty = context["kara"]

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