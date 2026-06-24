from discord import app_commands


def admin_required():

    async def predicate(interaction):

        allowed_roles = {
            "Administrator",
            "Moderator"
        }

        if any(
            role.name in allowed_roles
            for role in interaction.user.roles
        ):
            return True

        raise app_commands.CheckFailure(
            "Brak uprawnień"
        )

    return app_commands.check(predicate)