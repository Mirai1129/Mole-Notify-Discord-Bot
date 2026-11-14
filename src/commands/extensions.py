import logging

import nextcord
from nextcord.ext import commands

from src.core.core import BotCogs
from src.core.config import GUILD_IDS, ADMIN_IDS
from src.utils.extensions import walk_extensions

log = logging.getLogger(__name__)


class Extensions(BotCogs, name="Extensions"):
    """Load, unload, reload, and list extensions — bot owner only."""

    def __init__(self, bot):
        super().__init__(bot=bot)

    @staticmethod
    def _is_owner(interaction: nextcord.Interaction) -> bool:
        # Slash commands have no built-in owner check like prefix commands do,
        # so this is a manual guard. Checking against ADMIN_IDS directly
        # (rather than bot.is_owner(), which does an API lookup) keeps this
        # instant and avoids an extra round trip on every invocation.
        return interaction.user.id in ADMIN_IDS

    async def _deny_if_not_owner(self, interaction: nextcord.Interaction) -> bool:
        """Send a denial and return True if the caller is NOT the owner."""
        if not self._is_owner(interaction):
            await interaction.response.send_message(
                "❌ You're not allowed to use this command.", ephemeral=True
            )
            return True
        return False

    # The parent group. It has no body of its own — Discord requires a
    # callback, but it's never actually invoked once subcommands exist.
    @nextcord.slash_command(
        name="extensions",
        description="Manage bot extensions (owner only)",
        guild_ids=GUILD_IDS,
        default_member_permissions=nextcord.Permissions(administrator=True),
    )
    async def extensions_group(self, interaction: nextcord.Interaction) -> None:
        pass

    @extensions_group.subcommand(name="load", description="Load an extension")
    async def load_command(self, interaction: nextcord.Interaction, extension: str) -> None:
        if await self._deny_if_not_owner(interaction):
            return
        try:
            self.bot.load_extension(extension)
        except commands.ExtensionError as e:
            log.exception("Failed to load %s", extension)
            await interaction.response.send_message(
                f"❌ Failed to load `{extension}`: `{e}`", ephemeral=True
            )
        else:
            await interaction.response.send_message(f"✅ Loaded `{extension}`", ephemeral=True)

    @extensions_group.subcommand(name="unload", description="Unload an extension")
    async def unload_command(self, interaction: nextcord.Interaction, extension: str) -> None:
        if await self._deny_if_not_owner(interaction):
            return
        try:
            self.bot.unload_extension(extension)
        except commands.ExtensionError as e:
            await interaction.response.send_message(
                f"❌ Failed to unload `{extension}`: `{e}`", ephemeral=True
            )
        else:
            await interaction.response.send_message(f"✅ Unloaded `{extension}`", ephemeral=True)

    @extensions_group.subcommand(name="reload", description="Reload an extension")
    async def reload_command(self, interaction: nextcord.Interaction, extension: str) -> None:
        if await self._deny_if_not_owner(interaction):
            return
        try:
            self.bot.reload_extension(extension)
        except commands.ExtensionError as e:
            await interaction.response.send_message(
                f"❌ Failed to reload `{extension}`: `{e}`", ephemeral=True
            )
        else:
            await interaction.response.send_message(f"✅ Reloaded `{extension}`", ephemeral=True)

    @extensions_group.subcommand(name="list", description="List all discoverable extensions")
    async def list_command(self, interaction: nextcord.Interaction) -> None:
        if await self._deny_if_not_owner(interaction):
            return
        loaded = set(self.bot.extensions.keys())
        lines = [
            f"{'🟢' if ext in loaded else '🔴'} `{ext}`"
            for ext in walk_extensions()
        ]
        await interaction.response.send_message(
            "\n".join(lines) or "No extensions found.", ephemeral=True
        )


def setup(bot: commands.Bot) -> None:
    """Load the Extensions management cog."""
    bot.add_cog(Extensions(bot))
