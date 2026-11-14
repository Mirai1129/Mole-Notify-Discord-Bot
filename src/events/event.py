from datetime import datetime, timezone
import time

import nextcord
from nextcord.ext import commands

from src.core.core import BotCogs
from src.core import config
from src.log import log


class Event(BotCogs):
    def __init__(self, bot):
        super().__init__(bot=bot)

    @commands.Cog.listener()
    async def on_voice_state_update(
            self,
            member: nextcord.Member,
            before: nextcord.VoiceState,
            after: nextcord.VoiceState,
    ):
        if before.channel == after.channel:
            return

        channel = self.bot.get_channel(config.VOICE_EVENT_CHANNEL_ID)

        if not isinstance(channel, nextcord.TextChannel):
            log.warning("Voice event text channel not found")
            return

        if before.channel is None:
            description = f"進入 {after.channel.mention}"
            color = nextcord.Color.green()

        elif after.channel is None:
            description = f"離開 {before.channel.mention}"
            color = nextcord.Color.red()

        else:
            description = (
                f"{before.channel.mention} → "
                f"{after.channel.mention}"
            )
            color = nextcord.Color.blue()

        embed = nextcord.Embed(
            description=description,
            color=color,
            timestamp=datetime.now(timezone.utc),
        )

        embed.set_author(
            name=member.display_name,
            icon_url=member.display_avatar.url,
        )

        try:
            await channel.send(embed=embed)
        except nextcord.HTTPException:
            log.exception("Failed to send voice event embed")


def setup(bot):
    bot.add_cog(Event(bot))
