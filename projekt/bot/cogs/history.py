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

    def cog_unload(self):

        self.db.close()

    @app_commands.guild_only()
    @app_commands.command(
        name="history",
        description="Pokazuje historię decyzji AI"
    )
    @app_commands.describe(
        limit="Ilość wyników (1-20)",
        page="Numer strony",
        search="Szukana fraza"
    )
    @admin_required()
    async def history(
        self,
        interaction
        limit: int = 5
        page: int = 1,
        search: str = None
    ):
        
        if limit < 1:
            limit = 1


        if limit > 20:
            limit = 20



        if page < 1:
            page = 1


        if search:

            decisions = self.db.search_history(
                search,
                limit
            )

        else:

            decisions = self.db.get_history(
                limit,
                page
            )


        if not decisions:

            await interaction.response.send_message(
                "Brak wyników."
            )

            return



        message = (
            "📚 **Historia decyzji:**\n\n"
        )


        for decision in decisions:

            decision_id, moderator, question, response, date = decision


            entry = (

                f"#{decision_id}\n"

                f"👤 **{moderator}**\n"

                f"❓ {question}\n"

                f"🕒 {date}\n"

                f"{response[:300]}\n"

                "----------------\n"

            )


            if len(message + entry) > 1900:
                break


            message += entry

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