import nextcord

from src.core.core import BotCogs
from src.core.config import GUILD_IDS, VOICE_EVENT_CHANNEL_ID


class GeneralCommand(BotCogs, name="General"):
    """General-purpose commands."""

    def __init__(self, bot):
        super().__init__(bot=bot)

    @nextcord.slash_command(guild_ids=GUILD_IDS)
    async def ping(self, interaction: nextcord.Interaction) -> None:
        await interaction.response.send_message(
            f"Pong! {self.bot.latency * 1000:.2f} ms", ephemeral=True
        )

    @nextcord.slash_command(guild_ids=GUILD_IDS)
    async def test_message(self, interaction: nextcord.Interaction):
        await interaction.response.send_message(type(VOICE_EVENT_CHANNEL_ID), ephemeral=True)

    @nextcord.slash_command(description="對不起，不行", guild_ids=GUILD_IDS)
    async def sorry(self, interaction: nextcord.Interaction) -> None:
        await interaction.response.send_message("對不起，不行")


def setup(bot) -> None:
    """Load the General cog."""
    bot.add_cog(GeneralCommand(bot))
