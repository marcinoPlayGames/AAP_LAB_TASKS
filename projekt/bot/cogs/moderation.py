import discord

from discord.ext import commands
from discord import app_commands

from bot.checks.permissions import admin_required

from services.moderation_service import ModerationService


GUILD_ID = 1123368740134862938



class ModerationCog(commands.Cog):


    def __init__(self, bot):

        self.bot = bot
        self.service = ModerationService()



    @app_commands.command(
        name="kick",
        description="Wyrzuca użytkownika"
    )
    @admin_required()
    async def kick(
        self,
        interaction: discord.Interaction,
        member: discord.Member
    ):

        await self.service.kick(member)


        await interaction.response.send_message(
            f"✅ Wyrzucono {member.mention}"
        )



    @app_commands.command(
        name="ban",
        description="Banuje użytkownika"
    )
    @admin_required()
    async def ban(
        self,
        interaction: discord.Interaction,
        member: discord.Member
    ):


        await self.service.ban(member)


        await interaction.response.send_message(
            f"🔨 Zbanowano {member.mention}"
        )



async def setup(bot):

    guild = discord.Object(
        id=GUILD_ID
    )


    await bot.add_cog(
        ModerationCog(bot),
        guild=guild
    )