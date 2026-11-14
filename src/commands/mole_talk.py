import nextcord

from src.core.config import GUILD_IDS
from src.core.core import BotCogs


class MoleTalkCommand(BotCogs):
    def __init__(self, bot):
        super().__init__(bot=bot)

    @nextcord.slash_command(description="摩爾對話", guild_ids=GUILD_IDS)
    async def mole_talk(self, interaction: nextcord.Interaction):
        await interaction.response.send_message("對不起，不行")


def setup(bot):
    bot.add_cog(MoleTalkCommand(bot))

