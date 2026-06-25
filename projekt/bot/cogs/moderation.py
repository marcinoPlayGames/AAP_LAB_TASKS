import discord

from discord.ext import commands
from discord import app_commands

from datetime import timedelta

from bot.checks.permissions import admin_required

from services.moderation_service import ModerationService

from config import GUILD_SERVER_ID

GUILD_ID = GUILD_SERVER_ID



class ModerationCog(commands.Cog):


    def __init__(self, bot):

        self.bot = bot
        self.service = ModerationService()


    @app_commands.command(
        name="mute",
        description="Wycisza użytkownika"
    )
    @app_commands.describe(
        member="Użytkownik",
        minutes="Czas mute w minutach"
    )
    @admin_required()
    async def mute(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        minutes: int
    ):


        duration = timedelta(
            minutes=minutes
        )


        await self.service.mute(
            member,
            duration
        )


        await interaction.response.send_message(
            f"🔇 Wyciszono {member.mention} na {minutes} minut"
        )
    
    
    
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