from discord import app_commands


def admin_required():

    async def predicate(interaction):

        allowed_roles = {
            "Administrator",
            "Moderator"
        }

        return any(
            role.name in allowed_roles
            for role in interaction.user.roles
        )

    return app_commands.check(predicate)