import discord

from discord.ext import commands

from discord import app_commands

from services.database import Database

from bot.checks.permissions import admin_required


GUILD_ID = 1123368740134862938



class HistoryCog(commands.Cog):


    def __init__(self, bot):

        self.bot = bot

        self.db = Database()



    @app_commands.guild_only()
    @app_commands.command(
        name="history",
        description="Pokazuje historię decyzji AI"
    )
    @admin_required()
    async def history(
        self,
        interaction
        limit: int = 5
    ):


        decisions = self.db.get_history(limit)


        if not decisions:

            await interaction.response.send_message(
                "Brak historii decyzji."
            )

            return



        message = "📚 **Historia decyzji:**\n\n"


        for decision in decisions:

            decision_id, moderator, question, response, date = decision


            message += (
                f"#{decision_id}\n"
                f"👤 **{moderator}**\n"
                f"❓ {question}\n"
                f"🕒 {date}\n"
                f"{response[:300]}\n"
                f"----------------\n"
            )
            
        message = message[:1900]

        await interaction.response.send_message(
            message
        )



    @history.error
    async def history_error(
        self,
        interaction,
        error
    ):

        if isinstance(
            error,
            app_commands.CheckFailure
        ):

            await interaction.response.send_message(
                "Nie masz uprawnień.",
                ephemeral=True
            )



async def setup(bot):

    guild = discord.Object(
        id=GUILD_ID
    )


    await bot.add_cog(
        HistoryCog(bot),
        guild=guild
    )