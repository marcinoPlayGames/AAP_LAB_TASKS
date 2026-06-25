class ModerationService:


    async def mute(
        self,
        member,
        duration
    ):

        await member.timeout(
            duration,
            reason="AI Moderator"
        )


    async def kick(
        self,
        member
    ):

        await member.kick(
            reason="AI Moderator"
        )


    async def ban(
        self,
        member
    ):

        await member.ban(
            reason="AI Moderator"
        )