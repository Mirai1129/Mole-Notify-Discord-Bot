from nextcord.ext.commands import Bot, Cog


class BotCogs(Cog, name="bot"):
    def __init__(self, bot: Bot):
        self.bot = bot
