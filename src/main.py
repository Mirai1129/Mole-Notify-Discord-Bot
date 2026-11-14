import logging

import nextcord
from nextcord.ext import commands

from src.core.config import DISCORD_BOT_TOKEN
from src.utils.extensions import walk_extensions
from .log import log

intents = nextcord.Intents.all()
bot = commands.Bot(intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")


def load_extensions() -> None:
    """Load every extension discovered under src/commands/, isolating failures."""
    for extension in walk_extensions():
        try:
            bot.load_extension(extension)
            log.info(f"Loaded extension: {extension}")
        except commands.ExtensionError:
            log.exception(f"Failed to load extension: {extension}")


if __name__ == "__main__":
    load_extensions()
    bot.run(DISCORD_BOT_TOKEN)  # type: ignore
