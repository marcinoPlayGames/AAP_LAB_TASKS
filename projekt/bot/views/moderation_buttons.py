import discord

from datetime import timedelta

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

        parts = penalty.lower().split()

        if len(parts) != 2:
            return None

        action, value = parts

        if action != "mute":
            return None

        if value.endswith("m"):

            minutes = int(
                value[:-1]
            )

            return timedelta(
                minutes=minutes
            )

        if value.endswith("h"):

            hours = int(
                value[:-1]
            )

            return timedelta(
                hours=hours
            )

        if value.endswith("d"):

            days = int(
                value[:-1]
            )

            return timedelta(
                days=days
            )

        return None
    
    def get_penalty_type(self):

        if not self.penalty:
            return None

        return self.penalty.split()[0].lower()
    
    def get_penalty_duration(self):

        if not self.penalty:
            return None

        return self.parse_penalty(
            self.penalty
        )
    
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
        
        penalty_type = self.get_penalty_type()
        
        if penalty_type == "mute":

            duration = self.get_penalty_duration()
            
            if duration is None:
                await interaction.response.send_message(
                    "❌ Niepoprawny format kary.",
                    ephemeral=True
                )
                return

            if duration > timedelta(days=28):
                await interaction.response.send_message(
                    "❌ Discord pozwala wyciszyć maksymalnie na 28 dni.",
                    ephemeral=True
                )
                return

            try:
                await self.member.timeout(
                    duration,
                    reason="AI Moderator"
                )

            except discord.HTTPException as e:
                await interaction.response.send_message(
                    f"❌ Nie udało się nałożyć kary:\n{e}",
                    ephemeral=True
                )
                return
            
            for item in self.children:
                item.disabled = True

            await interaction.message.edit(
                view=self
            )

            await interaction.response.send_message(
                f"🔇 Wyciszono {self.member.mention}"
            )

            return


        elif penalty_type == "ban":

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


        elif penalty_type == "kick":

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